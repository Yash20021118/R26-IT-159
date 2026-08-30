# ==============================================================================
# 🌾 Sri Lanka Agricultural Trilingual Custom SLM (Small Language Model)
# 🚀 1-CLICK ALL-IN-ONE TRAINING SCRIPT FOR GOOGLE COLAB (Free T4 GPU)
# Languages: Sinhala (සිංහල), English, Tamil (தமிழ்)
# ==============================================================================

import os
import sys
import gc
import json
import random
import subprocess
import shutil

print("=" * 70)
print("  STEP 1: Installing Required AI Libraries & Cleaning Dependencies...")
print("=" * 70)

# Remove old pre-installed incompatible torchao to prevent PEFT collision
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "torchao"], capture_output=True)

# Install clean stable libraries
subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "transformers>=4.40.0", "peft>=0.10.0", "accelerate>=0.29.0", "datasets>=2.18.0"
])

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

# Clear any cached GPU memory
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"\nCUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Model     : {torch.cuda.get_device_name(0)}")
    print(f"Total VRAM    : {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# ------------------------------------------------------------------------------
# STEP 2: Automatic Trilingual Agricultural Dataset Generation
# ------------------------------------------------------------------------------
DATASET_FILE = "agricultural_chat_dataset_trilingual.jsonl"

if not os.path.exists(DATASET_FILE):
    print("\n" + "=" * 70)
    print("  STEP 2: Building 4,000+ Sample Trilingual Dataset...")
    print("=" * 70)
    
    CROP_TRANSLATIONS = {
        "rice": {"en": "Rice (Paddy)", "si": "වී ගොවිතැන", "ta": "நெல் / அரிசி"},
        "maize": {"en": "Maize (Corn)", "si": "බඩඉරිඟු", "ta": "மக்காச்சோளம்"},
        "chickpea": {"en": "Chickpea", "si": "කඩල", "ta": "கொண்டைக்கடலை"},
        "kidneybeans": {"en": "Kidney Beans", "si": "රාජ්මා බෝංචි", "ta": "பீன்ස්"},
        "mungbean": {"en": "Mung Bean", "si": "මුං ඇට", "ta": "பாசிப்பयறு"},
        "blackgram": {"en": "Black Gram (Undu)", "si": "උඳු", "ta": "உளுந்து"},
        "banana": {"en": "Banana", "si": "කෙසෙල්", "ta": "வாழை"},
        "grapes": {"en": "Grapes", "si": "මිදි", "ta": "திராட்சை"},
        "watermelon": {"en": "Watermelon", "si": "කොමඩු", "ta": "தர்பூசணி"},
        "coconut": {"en": "Coconut", "si": "පොල්", "ta": "தேங்காய்"},
        "coffee": {"en": "Coffee", "si": "කෝපි", "ta": "காப்பி"},
    }

    DISTRICT_DATA = {
        "Polonnaruwa": {
            "zone_si": "වියළි කලාපය", "zone_en": "Dry Zone", "zone_ta": "உலர் வலயம்",
            "soil_si": "රතු-දුඹුරු පස (RBE) සහ පහත් බිම් හියුමික් මැටි පස", "soil_en": "Reddish Brown Earths and Low Humic Gley", "soil_ta": "செம்பழுப்பு மண் மற்றும் களிமண்",
            "maha_si": "මහ කන්නයේදී ඊසානදිග මෝසම් වැසි ලැබෙන බැවින් කුඹුරු ගොවිතැනට ඉතා යහපත් ජල සම්පාදනයක් ලැබේ.",
            "maha_en": "Northeast monsoon brings abundant rainfall, ideal for extensive paddy farming.",
            "maha_ta": "வடகிழக்கு பருவமழை காரணமாக நெல் விவசாயத்திற்கு போதுமான நீர் கிடைக்கும்.",
            "yala_si": "යල කන්නයේදී අඩු ජල අවශ්‍යතාවක් ඇති බඩඉරිඟු, මුං ඇට, උඳු සහ කොමඩු වැනි බෝග වඩාත් සුදුසු වේ.",
            "yala_en": "Dry weather favors drought-hardy crops like maize, mungbean, and watermelon.",
            "yala_ta": "குறைந்த நீர் தேவைப்படும் மக்காச்சோளம், பாசிப்பயறு போன்ற பயிர்கள் சிறந்தது.",
            "crops": ["rice", "maize", "blackgram", "mungbean", "watermelon"]
        },
        "Anuradhapura": {
            "zone_si": "වියළි කලාපය", "zone_en": "Dry Zone", "zone_ta": "உலர் வலயம்",
            "soil_si": "රතු-දුඹුරු පස (Reddish Brown Earths)", "soil_en": "Reddish Brown Earths", "soil_ta": "செம்பழுப்பு மண்",
            "maha_si": "මහ වැසි ලැබෙන බැවින් කුඹුරු ගොවිතැනට සහ ධාන්‍ය බෝග වලට ඉතා හිතකරය.",
            "maha_en": "Maha rains strongly favor paddy and major field crops.",
            "maha_ta": "மழைக்காலத்தில் நெல் மற்றும் தானிய பயிர்களுக்கு சாதகமானது.",
            "yala_si": "යල කන්නයේදී ජල හිඟයක් ඇතිවිය හැකි බැවින් මුං ඇට සහ උඳු වඩාත් ප්‍රතිඵලදායකය.",
            "yala_en": "Drought-tolerant pulses like mungbean and blackgram perform best.",
            "yala_ta": "வறட்சியைத் தாங்கும் பாசிப்பயறு, உளுந்து பயிர்கள் உகந்தது.",
            "crops": ["rice", "maize", "blackgram", "mungbean"]
        },
        "Kurunegala": {
            "zone_si": "අන්තර්මැදි කලාපය", "zone_en": "Intermediate Zone", "zone_ta": "இடைநிலை வலயம்",
            "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ රතු-දුඹුරු ලැටොසොලික් පස", "soil_en": "Red-Yellow Podzolic soils", "soil_ta": "செம்மஞ்சள் பொட்சோලிக் மண்",
            "maha_si": "වර්ෂාපතනය ක්‍රමයෙන් වැඩිවන අතර පොල්, කෙසෙල් සහ වී වගාවට ඉතා යහපත් වේ.",
            "maha_en": "Steady rainfall supports coconut, banana, and paddy cultivation.",
            "maha_ta": "மழைப்பொழிவு தேங்காய், வாழை மற்றும் நெல் பயிர்ச்செய்கைக்கு நன்று.",
            "yala_si": "මධ්‍යස්ථ වර්ෂාපතනයක් පවතින බැවින් පළතුරු සහ එළවළු වගාවන්ට සුදුසුය.",
            "yala_en": "Moderate rainfall supports fruits and seasonal cash crops.",
            "yala_ta": "மிதமான மழை இருப்பதால் பழங்கள் மற்றும் காய்கறிகளுக்கு ஏற்றது.",
            "crops": ["coconut", "rice", "banana", "maize"]
        },
        "Kandy": {
            "zone_si": "තෙත් කලාපය", "zone_en": "Wet Zone", "zone_ta": "ஈர வலயம்",
            "soil_si": "රතු-කහ පොඩ්සොලික් පස", "soil_en": "Red-Yellow Podzolic", "soil_ta": "செம்மஞ்சள் பொட்சோලிக் மண்",
            "maha_si": "සිසිල් දේශගුණය සහ වැසි කුළුබඩු, කෝපි සහ එළවළු සඳහා විශිෂ්ටයි.",
            "maha_en": "Cool climate and steady rains are ideal for spices, coffee, and vegetables.",
            "maha_ta": "குளிர்ந்த காலநிலை காப்பி, மசாலா பயிர்களுக்கு சிறந்தது.",
            "yala_si": "නිරිතදිග මෝසමෙන් නිරන්තර තෙතමනයක් පවතී.",
            "yala_en": "Southwest monsoon provides consistent moisture.",
            "yala_ta": "தென்மேற்கு பருவமழை காரணமாக எப்போதும் ஈரப்பதம் இருக்கும்.",
            "crops": ["coffee", "banana", "rice"]
        },
        "Jaffna": {
            "zone_si": "වියළි කලාපය", "zone_en": "Dry Zone", "zone_ta": "உலர் வலயம்",
            "soil_si": "කැල්සික් රතු-කහ ලැටොසොල් පස", "soil_en": "Calcic Red Yellow Latosols", "soil_ta": "சுண்ணாம்பு செம்மஞ்சள் மண்",
            "maha_si": "ඊසානදිග මෝසම් වැසි වගාවන්ට ප්‍රධාන ජල මූලාශ්‍රය වේ.",
            "maha_en": "Northeast monsoon provides essential water for seasonal crops.",
            "maha_ta": "வடகிழக்கு பருவமழை விவசாயத்திற்கு முக்கிய நீர் ஆதாரமாகும்.",
            "yala_si": "වියළි කාලගුණයක් ඇති බැවින් බිංදු ජල සම්පාදනය යොදා මිදි සහ කොමඩු වගා කරන්න.",
            "yala_en": "Use drip irrigation for cultivating grapes and watermelon.",
            "yala_ta": "சொட்டு நீர் பாசனம் மூலம் திராட்சை, தர்பூசணி பயிரிடலாம்.",
            "crops": ["grapes", "watermelon", "banana", "blackgram"]
        }
    }

    MONTHS = [
        ("January", "ජනවාරි", "ஜனவரி", True), ("February", "පෙබරවාරි", "பிப்ரவரி", True),
        ("March", "මාර්තු", "மார்ச்", True), ("April", "අප්‍රේල්", "ஏப்ரல்", False),
        ("May", "මැයි", "மே", False), ("June", "ජූනි", "ஜூன்", False),
        ("July", "ජූලි", "ஜூலை", False), ("August", "අගෝස්තු", "ஆகஸ்ட்", False),
        ("September", "සැප්තැම්බර්", "செப்டம்பர்", True), ("October", "ඔක්තෝබර්", "அக்டோபர்", True),
        ("November", "නොවැම්බර්", "நவம்பர்", True), ("December", "දෙසැම්බර්", "டிசம்பர்", True),
    ]

    all_samples = []
    
    for district, d in DISTRICT_DATA.items():
        for m_en, m_si, m_ta, is_maha in MONTHS:
            weather_si = d["maha_si"] if is_maha else d["yala_si"]
            weather_en = d["maha_en"] if is_maha else d["yala_en"]
            weather_ta = d["maha_ta"] if is_maha else d["yala_ta"]
            crops_si = ", ".join([CROP_TRANSLATIONS[c]["si"] for c in d["crops"]])
            crops_en = ", ".join([CROP_TRANSLATIONS[c]["en"] for c in d["crops"]])
            crops_ta = ", ".join([CROP_TRANSLATIONS[c]["ta"] for c in d["crops"]])

            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"ඉදිරියට එන {m_si} මාසයේ {district} ප්‍රදේශයේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?"},
                    {"role": "assistant", "content": f"{m_si} මාසයේ {district} ප්‍රදේශය {d['zone_si']}ට අයත් වේ. එහි ප්‍රධාන වශයෙන් {d['soil_si']} දක්නට ලැබේ. {weather_si} මෙම කාලසීමාව තුළ {crops_si} වැනි බෝග සාර්ථකව වගා කළ හැකි අතර, නිසි පාංශු කළමනාකරණය මගින් ඉහළ අස්වැන්නක් ලබාගත හැක."}
                ]
            })
            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"How is the agricultural and crop condition in {district} during {m_en}? What should I grow?"},
                    {"role": "assistant", "content": f"In {m_en}, {district} belongs to the {d['zone_en']} characterized by {d['soil_en']}. {weather_en} Recommended high-yielding crops include {crops_en}. Maintaining proper soil conditioning and nutrient balance will ensure maximum output."}
                ]
            })
            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"{m_ta} மாதத்தில் {district} பகுதியில் பயிர்ச்செய்கை நிலைமை எவ்வாறு இருக்கும்? என்ன பயிரிடலாம்?"},
                    {"role": "assistant", "content": f"{m_ta} மாதத்தில் {district} பகுதி {d['zone_ta']}க்கு உட்பட்டது. இங்கு பிரதானமாக {d['soil_ta']} காணப்படுகிறது. {weather_ta} இக்காலத்தில் {crops_ta} போன்ற பயிர்களை வெற்றிகரமாக பயிரிடலாம். முறையான பராமரிப்பு மூலம் சிறந்த விளைச்சலை பெறலாம்."}
                ]
            })

    soil_cases = [
        (90, 45, 40, 6.5, "Rice (Paddy)", "වී ගොවිතැන", "நெல் / அரிசி"),
        (105, 42, 22, 6.2, "Maize (Corn)", "බඩඉරිඟු", "மக்காச்சோளம்"),
        (40, 65, 80, 5.8, "Banana", "කෙසෙල්", "வாழை"),
        (25, 140, 200, 5.5, "Grapes", "මිදි", "திராட்சை"),
        (100, 15, 50, 5.5, "Coconut", "පොල්", "தேங்காய்"),
        (45, 60, 20, 6.8, "Mung Bean", "මුං ඇට", "பாசிப்பయறு"),
        (20, 55, 25, 7.2, "Black Gram (Undu)", "උඳු", "உளுந்து"),
        (100, 18, 50, 6.5, "Watermelon", "කොමඩු", "தர்பூசணி"),
    ]

    for n, p, k, ph, c_en, c_si, c_ta in soil_cases:
        for _ in range(50):
            n_j = max(5, int(n + random.randint(-5, 5)))
            p_j = max(5, int(p + random.randint(-4, 4)))
            k_j = max(5, int(k + random.randint(-4, 4)))
            ph_j = round(ph + random.uniform(-0.3, 0.3), 1)

            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"My soil test shows N={n_j}, P={p_j}, K={k_j}, and pH={ph_j}. What is the most recommended crop for high yield?"},
                    {"role": "assistant", "content": f"Based on your soil test values (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}) and favorable agro-climatic dynamics, the highest recommended crop with maximum yield potential is **{c_en}**. Apply recommended basal fertilizers and maintain optimum soil moisture."}
                ]
            })
            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"මගේ පසේ පරීක්ෂණ දත්ත N={n_j}, P={p_j}, K={k_j}, සහ pH={ph_j} වේ. වැඩිම අස්වැන්නක් සඳහා නිර්දේශිත බෝගය කුමක්ද?"},
                    {"role": "assistant", "content": f"ඔබගේ පස් පරීක්ෂණ දත්ත (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}) අනුව, මෙම පෝෂක මට්ටම් වලට වඩාත්ම ගැළපෙන සහ ඉහළම අස්වැන්නක් ලබාගත හැකි බෝගය වන්නේ **{c_si} ({c_en})** ය. නියමිත වේලාවට පොහොර යොදමින් තෙතමනය නිසි ලෙස කළමනාකරණය කරන්න."}
                ]
            })
            all_samples.append({
                "messages": [
                    {"role": "user", "content": f"மண் பரிசோதனையில் N={n_j}, P={p_j}, K={k_j}, pH={ph_j} என உள்ளது. அதிக விளைச்சல் தரும் சிறந்த பயிர் எது?"},
                    {"role": "assistant", "content": f"உங்கள் மண் பரிசோதனை தரவுகளின்படி (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}), இந்த நிலைக்கு மிகவும் பொருத்தமான அதிக மகசூல் தரும் பயிர் **{c_ta} ({c_en})** ஆகும். பரிந்துரைக்கப்பட்ட உரங்களை இட்டு சிறந்த விளைச்சலை பெறுங்கள்."}
                ]
            })

    random.seed(42)
    random.shuffle(all_samples)

    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        for s in all_samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"Generated {len(all_samples)} samples into '{DATASET_FILE}'!")
else:
    print(f"Dataset '{DATASET_FILE}' found ready.")

# ------------------------------------------------------------------------------
# STEP 3: Load Model & Tokenizer in Pure Float16 (Tesla T4 GPU)
# ------------------------------------------------------------------------------
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
print("\n" + "=" * 70)
print(f"  STEP 3: Loading Base Model {MODEL_ID}...")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto" if torch.cuda.is_available() else None,
    trust_remote_code=True
)
model.config.use_cache = False

# ------------------------------------------------------------------------------
# STEP 4: Attach LoRA Adapter
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  STEP 4: Attaching LoRA (Low-Rank Adaptation) Layers...")
print("=" * 70)

model.enable_input_require_grads()
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# ------------------------------------------------------------------------------
# STEP 5: Tokenize with Completion-Only Loss Masking
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  STEP 5: Formatting Dataset & Masking Prompt Loss...")
print("=" * 70)

raw_dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

def tokenize_with_response_masking(example):
    user_prompt = tokenizer.apply_chat_template(example["messages"][:-1], tokenize=False, add_generation_prompt=True)
    full_prompt = tokenizer.apply_chat_template(example["messages"], tokenize=False, add_generation_prompt=False)
    
    user_tokens = tokenizer(user_prompt, add_special_tokens=False)["input_ids"]
    full_tokens = tokenizer(full_prompt, max_length=384, truncation=True, add_special_tokens=False)
    
    input_ids = full_tokens["input_ids"]
    labels = list(input_ids)
    
    prompt_len = min(len(user_tokens), len(labels))
    for i in range(prompt_len):
        labels[i] = -100
        
    return {
        "input_ids": input_ids,
        "attention_mask": full_tokens["attention_mask"],
        "labels": labels
    }

tokenized_dataset = raw_dataset.map(tokenize_with_response_masking, remove_columns=raw_dataset.column_names)
print(f"Tokenized samples ready: {len(tokenized_dataset)}")

# ------------------------------------------------------------------------------
# STEP 6: Execute Memory-Optimized Fine-Tuning
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  STEP 6: Starting Supervised Fine-Tuning (Trainer)...")
print("=" * 70)

# Memory optimization: batch_size=2 with grad_accum=8 uses < 5 GB VRAM!
training_args = TrainingArguments(
    output_dir="./soil_crop_qwen_slm",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    warmup_steps=20,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=torch.cuda.is_available(),
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="adamw_torch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    train_dataset=tokenized_dataset,
    args=training_args,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, pad_to_multiple_of=8)
)

trainer.train()
print("\n🎉 Fine-Tuning Completed Successfully!")

# ------------------------------------------------------------------------------
# STEP 7: Live Inference Testing (Trilingual)
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  STEP 7: Testing Trilingual Inference...")
print("=" * 70)

model.eval()
model.config.use_cache = True

def ask_agri_bot(query: str):
    messages = [
        {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka soil analysis and crop recommendations."},
        {"role": "user", "content": query}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    im_end_id = tokenizer.convert_tokens_to_ids("<|im_end|>")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=[tokenizer.eos_token_id, im_end_id]
        )
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    print(f"\nQ: {query}")
    print(f"A: {response.strip()}")
    print("-" * 70)

# Tests in Sinhala, English, Tamil
ask_agri_bot("ඉදිරියට එන සැප්තැම්බර් මාසයේ පොළොන්නරුවේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?")
ask_agri_bot("My soil test shows N=90, P=45, K=40, and pH=6.5. What is the most recommended crop for high yield?")
ask_agri_bot("செப்டம்பர் மாதத்தில் பொலன்னறுவையில் பயிர்ச்செய்கை நிலைமை எவ்வாறு இருக்கும்?")

# ------------------------------------------------------------------------------
# STEP 8: Save & Download Adapter Zip
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  STEP 8: Packaging Model for Local Backend...")
print("=" * 70)

SAVE_DIR = "./fine_tuned_agri_qwen_lora"
trainer.model.save_pretrained(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

shutil.make_archive("fine_tuned_agri_qwen_lora", "zip", SAVE_DIR)
print("🎉 Packaged successfully into 'fine_tuned_agri_qwen_lora.zip'!")

try:
    from google.colab import files
    files.download("fine_tuned_agri_qwen_lora.zip")
    print("✅ Download triggered in your browser!")
except Exception:
    print("Download 'fine_tuned_agri_qwen_lora.zip' from Colab left files panel.")
