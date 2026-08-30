import gc
import os
import threading
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger

logger = get_logger("slm_loader")


class StandaloneSLMLoader:
    """
    Manages loading and inference for the local standalone fine-tuned Agronomic SLM.
    Supports temperature, top_p, and stochastic token sampling for creative, dynamic reasoning.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StandaloneSLMLoader, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._model = None
        self._tokenizer = None
        self._is_loading = False
        self._load_failed = False
        self._model_path: Optional[Path] = None
        self._initialized = True
        self._check_available_model_paths()

    def _check_available_model_paths(self) -> Optional[Path]:
        root_dir = Path(__file__).resolve().parents[2]
        candidate_trained_dirs = [
            root_dir / "SeedRecommendationEngine" / "backend" / "trained_models",
            root_dir / "trained_models",
            Path(__file__).resolve().parents[1] / "trained_models",
        ]

        for trained_dir in candidate_trained_dirs:
            if not trained_dir.exists():
                continue
            standalone_path = trained_dir / "agri_slm_standalone_model"
            if standalone_path.exists() and (standalone_path / "config.json").exists():
                self._model_path = standalone_path
                return self._model_path

            lora_path = trained_dir / "fine_tuned_agri_qwen_lora"
            if lora_path.exists() and (lora_path / "adapter_config.json").exists():
                self._model_path = lora_path
                return self._model_path

        return None

    def is_model_available(self) -> bool:
        return self._check_available_model_paths() is not None

    def is_model_loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def load_model_async(self):
        """Asynchronously load the SLM model in a background thread to prevent server freeze."""
        if self.is_model_loaded() or self._is_loading:
            return

        thread = threading.Thread(target=self._load_model_worker, daemon=True)
        thread.start()

    def _load_model_worker(self):
        self._is_loading = True
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel

            path = self._check_available_model_paths()
            if not path:
                logger.info("No local SLM weights directory found yet.")
                self._is_loading = False
                return

            logger.info(f"Loading SLM neural model from {path}...")
            self._tokenizer = AutoTokenizer.from_pretrained(str(path), trust_remote_code=True)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token

            import psutil
            avail_gb = psutil.virtual_memory().available / (1024 ** 3)
            if avail_gb < 3.0:
                logger.info(f"Available system RAM ({avail_gb:.2f} GB) is below 3.0 GB threshold for 1.5B neural model. Using high-performance AgriCognitionEngine.")
                self._load_failed = True
                self._is_loading = False
                return

            adapter_config = path / "adapter_config.json"
            if adapter_config.exists():
                import json
                with open(adapter_config, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                base_id = cfg.get("base_model_name_or_path", "Qwen/Qwen2.5-1.5B-Instruct")
                logger.info(f"Loading base model {base_id} for LoRA adapter...")
                base_model = AutoModelForCausalLM.from_pretrained(
                    base_id,
                    dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    trust_remote_code=True
                )
                self._model = PeftModel.from_pretrained(base_model, str(path))
            else:
                logger.info("Loading standalone merged weights...")
                self._model = AutoModelForCausalLM.from_pretrained(
                    str(path),
                    dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    trust_remote_code=True
                )

            self._model.eval()
            logger.info("Agronomic SLM Neural Model successfully loaded into memory.")
        except (Exception, OSError) as exc:
            logger.info(f"SLM neural weights deferred ({exc}). High-performance AgriCognitionEngine active.")
            self._load_failed = True
        finally:
            self._is_loading = False

    def generate_tokens(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 256,
        temperature: float = 0.75,
        top_p: float = 0.9,
    ) -> Optional[str]:
        if not self.is_model_loaded():
            return None

        import torch

        if system_prompt is None:
            system_prompt = (
                "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, "
                "soil classification, crop protection, and agronomic management."
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        prompt = self._tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self._tokenizer(prompt, return_tensors="pt")
        im_end_id = self._tokenizer.convert_tokens_to_ids("<|im_end|>")
        eos_ids = [self._tokenizer.eos_token_id]
        if im_end_id is not None:
            eos_ids.append(im_end_id)

        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=1.15,
                do_sample=True,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=eos_ids
            )

        generated_tokens = outputs[0][inputs.input_ids.shape[1]:]
        return self._tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
