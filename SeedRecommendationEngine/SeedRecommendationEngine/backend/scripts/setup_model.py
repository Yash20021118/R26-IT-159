import os
import shutil
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = ROOT_DIR / "SeedRecommendationEngine" / "backend"
TARGET_DIR = BACKEND_DIR / "trained_models" / "fine_tuned_agri_qwen_lora"
USER_DOWNLOADS = Path.home() / "Downloads"

def find_and_extract_model():
    print("=" * 65)
    print("  Setting Up Fine-Tuned Agri-Qwen SLM Model")
    print("=" * 65)
    
    # Check potential zip locations
    potential_zips = [
        USER_DOWNLOADS / "fine_tuned_agri_qwen_lora.zip",
        BACKEND_DIR / "fine_tuned_agri_qwen_lora.zip",
        ROOT_DIR / "fine_tuned_agri_qwen_lora.zip",
        Path("fine_tuned_agri_qwen_lora.zip").resolve()
    ]
    
    found_zip = None
    for p in potential_zips:
        if p.exists():
            found_zip = p
            break
            
    if not found_zip:
        print(f"⚠️ 'fine_tuned_agri_qwen_lora.zip' was not automatically found in Downloads.")
        print(f"Please copy your downloaded 'fine_tuned_agri_qwen_lora.zip' into:\n{BACKEND_DIR / 'trained_models'}")
        return

    print(f"Found model zip at: {found_zip}")
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting to: {TARGET_DIR} ...")
    with zipfile.ZipFile(found_zip, "r") as z:
        z.extractall(TARGET_DIR)
        
    # Check if files were extracted into a nested subfolder
    subfolders = [f for f in TARGET_DIR.iterdir() if f.is_dir()]
    if len(subfolders) == 1 and subfolders[0].name == "fine_tuned_agri_qwen_lora":
        nested = subfolders[0]
        for item in nested.iterdir():
            shutil.move(str(item), str(TARGET_DIR / item.name))
        nested.rmdir()
        
    print("[SUCCESS] Model extracted successfully!")
    print(f"Model files in {TARGET_DIR}:")
    for f in TARGET_DIR.iterdir():
        print(f"  - {f.name}")
        
    print("\n[READY] Your backend is now ready to infer from your fine-tuned SLM!")

if __name__ == "__main__":
    find_and_extract_model()
