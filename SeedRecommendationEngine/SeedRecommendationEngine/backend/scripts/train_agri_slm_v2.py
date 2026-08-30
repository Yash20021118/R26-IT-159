# ==============================================================================
# 🌾 Sri Lanka Agricultural Trilingual Generative SLM - Training Pipeline V2
# 🚀 1-CLICK ALL-IN-ONE TRAINING & FULL STANDALONE MODEL EXPORTER FOR GOOGLE COLAB
# Architecture: Qwen2.5-1.5B-Instruct (or 0.5B) + Pure FP16 LoRA + Automatic Weight Merging
# Output: Standalone Self-Contained Model (No Base Model Download Needed Locally)
# ==============================================================================

import os
import sys
import gc
import json
import random
import subprocess
import shutil

print("=" * 75)
print("  STEP 1: Installing Required AI Libraries & Cleaning Dependencies...")
print("=" * 75)

subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "torchao"], capture_output=True)

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

gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"\nCUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Model     : {torch.cuda.get_device_name(0)}")
    print(f"Total VRAM    : {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# ------------------------------------------------------------------------------
# STEP 2: Generate Comprehensive 5,000+ Sample Trilingual Agricultural Dataset
# ------------------------------------------------------------------------------
DATASET_FILE = "agricultural_slm_dataset_v2.jsonl"

print("\n" + "=" * 75)
print("  STEP 2: Building Comprehensive Multi-Topic Trilingual Dataset...")
print("=" * 75)

all_samples = []

# --- 1. Comprehensive Pest & Disease Management Q&As ---
DISEASE_QA = [
    {
        "q_si": "මිරිස් වගාවේ කොළ කොඩවීමේ රෝගයට (Leaf Curl) ප්‍රතිකාර කරන්නේ කෙසේද?",
        "a_si": "මිරිස් කොළ කොඩවීම ප්‍රධාන වශයෙන් පැළ මැක්කන් (Thrips) සහ සුදු මැස්සන් (Whiteflies) වැනි යුෂ උරාබොන කෘමීන් මගින් බෝවන වෛරස් රෝගයකි. පාලනය සඳහා:\n1. කොහොඹ ඇට සාරය (Neem extract) හෝ සබන් මිශ්‍රණය දින 4-5 කට වරක් ඉසින්න.\n2. කහ පැහැති ඇලෙන සුළු උගුල් (Yellow sticky traps) පාත්ති පුරා ස්ථාපනය කරන්න.\n3. අධික ලෙස ආසාදිත පැළ ගලවා විනාශ කර පුලුස්සා දමන්න.\n4. අවශ්‍ය නම් නිර්දේශිත කෘමිනාශකයක් (උදා: ඉමිඩැක්ලෝප්‍රිඩ් හෝ පෙගසස්) නියමිත මාත්‍රාවට යොදන්න.",
        "q_en": "How can I control chilli leaf curl disease in my crop?",
        "a_en": "Chilli leaf curl is primarily a viral disease transmitted by sucking pests such as thrips, mites, and whiteflies. Remediation steps:\n1. Spray neem seed kernel extract or soapy water every 4-5 days.\n2. Install yellow and blue sticky traps across the field.\n3. Rogue out and safely burn severely infected plants.\n4. If pest pressure is severe, apply recommended systemic insecticides (e.g., Imidacloprid or Diafenthiuron) as per Department of Agriculture guidelines.",
        "q_ta": "மிளகாய் பயிரில் இலை சுருட்டல் நோயை (Leaf Curl) எவ்வாறு கட்டுப்படுத்துவது?",
        "a_ta": "மிளகாய் இலை சுருட்டல் நோய் முக்கியமாக அசுவினி, இலைப்பேன் மற்றும் வெள்ளை ஈக்கள் மூலம் பரவும் வைரஸ் நோயாகும். மேலாண்மை:\n1. வேப்பங்கொட்டை சாறு அல்லது இயற்கை பூச்சிவிரட்டியை 4-5 நாட்களுக்கு ஒருமுறை தெளிக்கவும்.\n2. மஞ்சள் மற்றும் நீல வண்ண ஒட்டும் பொறிகளை வயலில் வைக்கவும்.\n3. அதிகம் பாதிக்கப்பட்ட செடிகளை பிடுங்கி அழிக்கவும்.\n4. தேவைப்பட்டால் பரிந்துரைக்கப்பட்ட பூச்சிக்கொல்லிகளை சரியான அளவில் தெளிக்கவும்."
    },
    {
        "q_si": "කුඹුරේ ගොයම් කොළ පාළුව (Rice Blast) සහ කොපු පාළුව (Sheath Blight) මර්දනය කරන්නේ කෙසේද?",
        "a_si": "ගොයම් කොළ පාළුව සහ කොපු පාළුව දිලීර මගින් හටගන්නා රෝග වේ. අධික නයිට්‍රජන් පොහොර (යූරියා) භාවිතය නිසා රෝගය උත්සන්න වේ.\nපාලන උපදෙස්:\n• නයිට්‍රජන් පොහොර නිර්දේශිත මාත්‍රාව ඉක්මවා යෙදීමෙන් වළකින්න.\n• කුඹුරේ ජලය බැසයාමට සලස්වා පස සුළු වශයෙන් වියළීමට ඉඩ හරින්න.\n• ක්ෂේත්‍රයේ ආරම්භක අවස්ථාවේදීම ට්‍රයිසයික්ලසෝල් (Tricyclazole) හෝ කාබෙන්ඩසිම් (Carbendazim) නිර්දේශිත පරිදි ඉසින්න.",
        "q_en": "How do I manage rice blast and sheath blight in paddy fields?",
        "a_en": "Rice blast and sheath blight are destructive fungal infections aggravated by excessive nitrogen (Urea) application and high humidity.\nManagement steps:\n• Balance nitrogen input; avoid excessive top-dressing.\n• Temporarily drain standing water from the field to reduce microclimate humidity.\n• Apply approved fungicides like Tricyclazole or Hexaconazole at early symptom onset.",
        "q_ta": "நெற்பயிரில் குலைநோய் (Rice Blast) மற்றும் உறை அழுகல் நோயை எவ்வாறு தடுப்பது?",
        "a_ta": "நெல் குலைநோய் பூஞ்சானால் ஏற்படும் நோயாகும். அதிக யூரியா பயன்பாடு இந்நோயை தீவிரப்படுத்தும்.\nகட்டுப்பாடு:\n• அதிகப்படியான நைதரசன் (யூரியா) உரத்தை தவிர்க்கவும்.\n• வயலில் இருந்து நீரை வடித்து மண்ணை சிறிது உலர விடவும்.\n• அறிகுறிகள் தென்படும் போதே Tricyclazole அல்லது பொருத்தமான பூஞ்சானக்கொல்லியை தெளிக்கவும்."
    },
    {
        "q_si": "පොල් ගස් වලට රතු කුරුමිණියා (Red Palm Weevil) හා කරුමිණි හානිය වළක්වා ගන්නේ කෙසේද?",
        "a_si": "රතු කුරුමිණියා පොල් ගසේ කඳ ඇතුළත කා දමන බැවින් කලින් හඳුනාගැනීම වැදගත්ය.\n• කඳේ සිදුරු වලින් දුඹුරු පැහැති ශ්‍රාවයක් ගලන්නේ නම් සහ කඳට කන තැබූ විට කෘමියා කන ශබ්දය ඇසේ නම් රතු කුරුමිණි හානිය තහවුරු වේ.\n• ෆෙරමෝන් උගුල් (Pheromone traps) වත්ත පුරා ස්ථාපනය කරන්න.\n• ආසාදිත සිදුරු තුළට නිර්දේශිත කෘමිනාශක ද්‍රාවණයක් ඇතුළු කර සිදුර මැටි හෝ සිමෙන්ති වලින් වසා දමන්න.\n• ගස් වල අනවශ්‍ය කැපුම් තුවාල ඇතිවීම වළක්වා ගන්න (තුවාල මතින් කෘමියා බිත්තර දමයි).",
        "q_en": "How to treat and prevent Red Palm Weevil damage in coconut palms?",
        "a_en": "Red Palm Weevil bores into the trunk, posing severe threats to coconut palms.\nControl practices:\n• Look for brownish sap oozing from small trunk holes and chewed fiber.\n• Install pheromone lures (ferrolure) around the coconut estate.\n• Funnel recommended systemic insecticides directly into infected boreholes and seal them with clay/cement.\n• Avoid mechanical wounds on trunks which attract egg-laying females.",
        "q_ta": "தென்னை மரங்களில் சிவப்பு கூன்வண்டு (Red Palm Weevil) தாக்குதலை எவ்வாறு தடுப்பது?",
        "a_ta": "சிவப்பு கூன்வண்டு தென்னை மரத்தின் உள்ளே துளைத்து சேதம் விளைவிக்கும்.\nகட்டுப்பாடு:\n• மரத்தில் இருந்து பழுப்பு நிற திரவம் வடிதல் மற்றும் துளைகளை பரிசோதிக்கவும்.\n• பெரோமோன் பொறிகளை (Pheromone traps) தோட்டத்தில் வைக்கவும்.\n• பாதிக்கப்பட்ட துளைகளுக்குள் பரிந்துரைக்கப்பட்ட மருந்தை செலுத்தி களிமண் கொண்டு அடைக்கவும்.\n• மரத்தில் காயங்கள் ஏற்படுவதை தவிர்க்கவும்."
    },
    {
        "q_si": "කෙසෙල් වගාවේ පැනමා රෝගය (Panama Wilt) හඳුනාගෙන පාලනය කරන්නේ කෙසේද?",
        "a_si": "පැනමා රෝගය පස ආශ්‍රිතව බෝවන ෆියුසාරියම් දිලීර රෝගයකි. පැරණි කොළ කහ වී කඳ පාමුල ඉරිතැලීම ප්‍රධාන ලක්ෂණයයි.\n• ආසාදිත පඳුරු මුලින්ම ගලවා පුළුස්සා දමන්න. එම වළට හුණු හෝ ඩොලමයිට් දමන්න.\n• රෝගී පැළ වලින් ලබාගත් කෙසෙල් අල/පැළ සිටුවීමට කිසිවිටෙකත් භාවිතා නොකරන්න.\n• ජල වහනය ඉතා හොඳින් සකස් කරන්න.",
        "q_en": "How do I diagnose and manage Panama disease (Fusarium wilt) in bananas?",
        "a_en": "Panama disease is a soil-borne fungal wilt (Fusarium oxysporum). Characteristic symptoms include yellowing of lower leaves and longitudinal splitting of the pseudostem.\nControl:\n• Uproot and burn diseased mats; drench the planting hole with lime/dolomite.\n• Never source suckers from infected fields; plant tissue-cultured disease-free suckers.\n• Ensure deep soil aeration and proper drainage.",
        "q_ta": "வாழை பயிரில் பனாமா வாடல் நோயை (Panama Wilt) எவ்வாறு கட்டுப்படுத்துவது?",
        "a_ta": "பனாமா நோய் மண்ணில் வாழும் பூஞ்சானால் உண்டாகிறது. கீழ் இலைகள் மஞ்சள் நிறமாகி தண்டு பிளவுபடுவது இதன் அறிகுறியாகும்.\nமேலாண்மை:\n• பாதிக்கப்பட்ட மரங்களை வேருடன் பிடுங்கி தீயிட்டு அழிக்கவும்.\n• நோய் தாக்கப்பட்ட தோட்டங்களில் இருந்து கன்றுகளை நடவு செய்ய வேண்டாம்.\n• நிலத்தில் நீர் தேங்காமல் வடிகால் வசதியை ஏற்படுத்தவும்."
    }
]

for d in DISEASE_QA:
    for _ in range(15):
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": d["q_si"]},
                {"role": "assistant", "content": d["a_si"]}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": d["q_en"]},
                {"role": "assistant", "content": d["a_en"]}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": d["q_ta"]},
                {"role": "assistant", "content": d["a_ta"]}
            ]
        })

# --- 2. Crop Cultivation, Water & Agronomic Practices ---
CROP_PRACTICE_QA = [
    {
        "q_si": "කෙසෙල් වගාවට ජල සම්පාදනය සහ පෝෂක ලබාදිය යුත්තේ කෙසේද?",
        "a_si": "කෙසෙල් යනු විශාල පත්‍ර පෘෂ්ඨයක් සහිත වැඩි ජල අවශ්‍යතාවක් ඇති බෝගයකි.\n• වියළි කාලගුණයේදී සතියකට දින 2-3ක් ජලය සපයන්න (බිංදු ජල සම්පාදනය ඉතා යෝග්‍ය වේ).\n• කඳ පාමුල වියළි කොළ හෝ පිදුරු යොදා වසුන් (Mulching) යොදන්න.\n• පොටෑසියම් (K) පෝෂකය කෙසෙල් වල ඵලදාව සහ රසය වැඩි කිරීමට අතිශය වැදගත් බැවින් නියමිත පරිදි MOP පොහොර හා කාබනික කොම්පෝස්ට් යොදන්න.",
        "q_en": "What are the watering and fertilization guidelines for healthy banana cultivation?",
        "a_en": "Bananas demand consistent moisture and heavy nutrient replenishment.\n• Water 2-3 times per week during dry dry spells, ideally via drip irrigation.\n• Apply thick organic mulch (straw/dry leaves) around the base to preserve moisture and suppress weeds.\n• Bananas are heavy consumers of Potassium (K); apply balanced N-P-K with elevated MOP for bunch size and fruit sweetness.",
        "q_ta": "வாழை சாகுபடியில் நீர்ப்பாசனம் மற்றும் உர மேலாண்மை எவ்வாறு அமைய வேண்டும்?",
        "a_ta": "வாழைக்கு அதிக நீர் மற்றும் ஊட்டச்சத்து தேவைப்படுகிறது.\n• உலர் காலத்தில் வாரத்திற்கு 2-3 முறை நீர் பாய்ச்சவும் (சொட்டு நீர் பாசனம் சிறந்தது).\n• ஈரப்பதத்தை பாதுகாக்க மரத்தை சுற்றி வைக்கோல் அல்லது காய்ந்த இலைகளை கொண்டு மூடாக்கு இடவும்.\n• பொட்டாசியம் (K) சத்து வாழைக்காய்கள் திரட்சியாக வளர மிகவும் முக்கியமானது. பரிந்துரைக்கப்பட்ட MOP மற்றும் இயற்கை உரங்களை இடவும்."
    },
    {
        "q_si": "වියළි කලාපයේ (Dry Zone) ගොවිතැනට ජලය සංරක්ෂණය කරගන්නේ කෙසේද?",
        "a_si": "ශ්‍රී ලංකාවේ වියළි කලාපයේ (පොළොන්නරුව, අනුරාධපුර, හම්බන්තොට, යාපනය) ජල සංරක්ෂණය ඉතා වැදගත්ය:\n1. බිංදු ජල සම්පාදනය (Drip Irrigation) යොදාගැනීමෙන් ජල නාස්තිය 50% කින් පමණ අවම කරගත හැක.\n2. ක්ෂේත්‍රයේ පිදුරු, පොල් ලෙලි හෝ කොළ රොඩු වසුන් (Mulch) ලෙස යෙදීමෙන් වාෂ්පීභවනය වළක්වයි.\n3. යල කන්නයේදී ජල අවශ්‍යතාව අඩු මුං ඇට, උඳු, තල, කොමඩු සහ බඩඉරිඟු වැනි කෙටි කාලීන ක්ෂේත්‍ර බෝග තෝරාගන්න.\n4. රාත්‍රී කාලයේ හෝ උදෑසන කාලයේදී ජල සම්පාදනය කරන්න.",
        "q_en": "What are the most effective water conservation techniques for dry zone agriculture in Sri Lanka?",
        "a_en": "Conserving water across Sri Lanka's dry zone (Anuradhapura, Polonnaruwa, Jaffna, Hambantota) is vital for high yields:\n1. Adopt Drip Irrigation to direct water straight to root zones, reducing water waste by up to 50%.\n2. Mulch heavily using paddy straw, coir dust, or crop residues to suppress surface evaporation.\n3. Cultivate drought-tolerant crops during the Yala season (e.g. mungbean, blackgram, sesame, watermelon, and maize).\n4. Schedule irrigation during early mornings or evenings to minimize evaporative losses.",
        "q_ta": "இலங்கையின் உலர் வலயத்தில் (Dry Zone) நீர் பாதுகாப்பு முறைகள் என்ன?",
        "a_ta": "உலர் வலயத்தில் (அனுராதபுரம், பொலன்னறுவை, யாழ்ப்பாணம்) நீரை திறமையாக பயன்படுத்தும் வழிகள்:\n1. சொட்டு நீர் பாசனம் (Drip Irrigation) மூலம் நீரை நேரடியாக வேர்களுக்கு செலுத்தி 50% நீரை சேமிக்கலாம்.\n2. வைக்கோல் அல்லது காய்ந்த இலைகளை மூடாக்காக இட்டு நீர் ஆவியாவதை தடுக்கவும்.\n3. சிறுபோகத்தில் (Yala) குறைந்த நீர் தேவைப்படும் பாசிப்பயறு, உளுந்து, எள் மற்றும் தர்பூசணி போன்ற பயிர்களை பயிரிடவும்.\n4. காலை அல்லது மாலை வேளைகளில் நீர்ப்பாசனம் செய்யவும்."
    },
    {
        "q_si": "පසේ ආම්ලිකතාවය (pH 5.5 ට අඩු වීම) නිවැරදිව පාලනය කරන්නේ කෙසේද?",
        "a_si": "පසේ pH අගය 5.5 ට වඩා අඩු වූ විට එය ආම්ලික පසක් ලෙස හැඳින්වේ. මෙහිදී පොස්පරස් වැනි පෝෂක බෝග වලට උරාගැනීම අඩාල වේ.\nප්‍රතිකාර:\n• අක්කරයකට කෘෂිකාර්මික ඩොලමයිට් (Agricultural Dolomite) හෝ හුණු කිලෝග්‍රෑම් 300 - 500 ක් යොදන්න.\n• බීජ හෝ පැළ සිටුවීමට අවම වශයෙන් සති 2 කට පෙර ඩොලමයිට් පසට හොඳින් මිශ්‍ර කර ජලය සපයන්න.\n• කොම්පෝස්ට් සහ සත්ව පොහොර නිතිපතා යෙදීමෙන් පාංශු බෆර හැකියාව (buffering capacity) වැඩි දියුණු වේ.",
        "q_en": "How can I remediate acidic soil (pH below 5.5)?",
        "a_en": "When soil pH falls below 5.5, nutrient lock-up (especially Phosphorus) and Aluminium toxicity occur.\nRemediation:\n• Broadcast Agricultural Dolomite or slaked lime at 300 to 500 kg per acre.\n• Incorporate dolomite at least 2 weeks prior to sowing or transplanting and irrigate lightly.\n• Regularly incorporate well-decomposed organic compost to enhance soil buffering capacity.",
        "q_ta": "மண்ணின் அமிலத்தன்மையை (pH 5.5க்கு கீழ்) எவ்வாறு சீரமைப்பது?",
        "a_ta": "மண்ணின் pH 5.5 க்கும் குறைவாக இருந்தால் ஊட்டச்சத்துக்கள் பயிர்களுக்கு கிடைப்பது தடைபடும்.\nசீரமைப்பு:\n• ஏக்கருக்கு 300 முதல் 500 கிலோ விவசாய டோலமைட் (Dolomite) அல்லது சுண்ணாம்பு இடவும்.\n• நடவு செய்வதற்கு குறைந்தது 2 வாரங்களுக்கு முன் டோலமைட்டை மண்ணுடன் கலந்து நீர் பாய்ச்சவும்.\n• மட்கிய இயற்கை உரங்களை தொடர்ந்து இட்டு மண்ணின் வளத்தை அதிகரிக்கவும்."
    }
]

for p in CROP_PRACTICE_QA:
    for _ in range(15):
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": p["q_si"]},
                {"role": "assistant", "content": p["a_si"]}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": p["q_en"]},
                {"role": "assistant", "content": p["a_en"]}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": p["q_ta"]},
                {"role": "assistant", "content": p["a_ta"]}
            ]
        })

# --- 3. Soil Test N-P-K & pH Crop Match Scenarios ---
SOIL_CASES = [
    (90, 45, 40, 6.5, "Rice (Paddy)", "වී ගොවිතැන", "நெல் / அரிசி", "රතු-දුඹුරු මැටි පසට සහ පහත් බිම් වලට සුදුසුය"),
    (105, 42, 22, 6.2, "Maize (Corn)", "බඩඉරිඟු", "மக்காச்சோளம்", "මහ හා යල කන්න දෙකටම යෝග්‍ය ඉහළ අස්වැන්නක් දෙන බෝගයකි"),
    (40, 65, 80, 5.8, "Banana", "කෙසෙල්", "வாழை", "පොටෑසියම් බහුල සාරවත් තෙත් කලාපීය පස් වලට විශිෂ්ටයි"),
    (25, 140, 200, 5.5, "Grapes", "මිදි", "திராட்சை", "යාපනය සහ කල්පිටිය වැනි හුණුගල් සහිත වියළි බිම් වලට සුදුසුය"),
    (100, 15, 50, 5.5, "Coconut", "පොල්", "தேங்காய்", "පොල් ත්‍රිකෝණයේ (කුරුණෑගල, පුත්තලම, ගම්පහ) වැලි-ලැටරයිට් පස් වලට යෝග්‍යයි"),
    (45, 60, 20, 6.8, "Mung Bean", "මුං ඇට", "பாசிப்பயறு", "යල කන්නයේ කෙටි කාලීන මුදල් බෝගයක් ලෙස විශිෂ්ටයි"),
    (20, 55, 25, 7.2, "Black Gram (Undu)", "උඳු", "உளுந்து", "වියළි කලාපයේ නයිට්‍රජන් තිර කරන රනිල බෝගයකි"),
    (100, 18, 50, 6.5, "Watermelon", "කොමඩු", "தர்பூசணி", "වැලි සහිත පසෙහි බිංදු ජල සම්පාදනය යටතේ උපරිම ඵලදාවක් ලැබේ")
]

for n, p, k, ph, c_en, c_si, c_ta, note_si in SOIL_CASES:
    for _ in range(40):
        n_j = max(5, int(n + random.randint(-6, 6)))
        p_j = max(5, int(p + random.randint(-5, 5)))
        k_j = max(5, int(k + random.randint(-5, 5)))
        ph_j = round(ph + random.uniform(-0.35, 0.35), 1)

        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"My soil test values are N={n_j}, P={p_j}, K={k_j}, and pH={ph_j}. Which crop is most suitable for highest yield?"},
                {"role": "assistant", "content": f"Based on your soil analysis (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}), the primary recommended crop with highest yield potential is **{c_en}**.\nSoil Condition: pH {ph_j} is within the favorable assimilation window. Apply recommended basal fertilizers and ensure adequate irrigation for optimum vegetative growth."}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"මගේ පස් පරීක්ෂණ දත්ත N={n_j}, P={p_j}, K={k_j}, සහ pH={ph_j} වේ. වැඩිම අස්වැන්නක් ලැබෙන බෝගය කුමක්ද?"},
                {"role": "assistant", "content": f"ඔබගේ පස් පරීක්ෂණ දත්ත (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}) සලකා බැලීමේදී, මෙම පෝෂක මට්ටමට වඩාත්ම ගැළපෙන ප්‍රමුඛ බෝගය වන්නේ **{c_si} ({c_en})** ය.\n{note_si}. නියමිත වේලාවට පොහොර යොදමින් තෙතමනය නිසි ලෙස කළමනාකරණය කිරීමෙන් උපරිම අස්වැන්නක් ලබාගත හැක."}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"மண் பரிசோதனை முடிவுகள் N={n_j}, P={p_j}, K={k_j}, pH={ph_j} என உள்ளன. அதிக மகசூல் பெற என்ன பயிரிடலாம்?"},
                {"role": "assistant", "content": f"உங்கள் மண் பரிசோதனை அளவீடுகளின்படி (N:{n_j}, P:{p_j}, K:{k_j}, pH:{ph_j}), இந்த ஊட்டச்சத்து நிலைக்கு மிகவும் பொருத்தமான பயிர் **{c_ta} ({c_en})** ஆகும்.\nபரிந்துரைக்கப்பட்ட உரங்களை இட்டு சிறந்த நீர்ப்பாசன முறையை கையாளுங்கள்."}
            ]
        })

# --- 4. District & Seasonal Agro-Ecological Guidance ---
DISTRICTS = [
    ("Polonnaruwa", "පොළොන්නරුව", "பொலன்னறுவை", "වියළි කලාපය", "Dry Zone", "උலர் வலயம்", "වී, බඩඉරිඟු, උඳු, මුං ඇට", "Paddy, Maize, Blackgram, Mungbean", "நெல், மக்காச்சோளம், உளுந்து", "රතු-දුඹුරු පස (RBE)", "Reddish Brown Earths"),
    ("Anuradhapura", "අනුරාධපුරය", "அனுராதபுரம்", "වියළි කලාපය", "Dry Zone", "උலர் வலயம்", "වී, බඩඉරිඟු, කඩල, තල", "Paddy, Maize, Chickpea, Sesame", "நெல், சோளம், கொண்டைக்கடலை", "රතු-දුඹුරු පස (RBE)", "Reddish Brown Earths"),
    ("Kurunegala", "කුරුණෑගල", "குருநாகல்", "අන්තර්මැදි කලාපය", "Intermediate Zone", "இடைநிலை வலயம்", "පොල්, වී, කෙසෙල්, පැපොල්", "Coconut, Paddy, Banana, Papaya", "தேங்காய், நெல், வாழை", "රතු-කහ පොඩ්සොලික් පස", "Red-Yellow Podzolic"),
    ("Jaffna", "යාපනය", "யாழ்ப்பாணம்", "උතුරු වියළි කලාපය", "Northern Dry Zone", "யாழ் உலர் வலயம்", "රතු ලූනු, මිරිස්, මිදි, කොමඩු", "Red Onion, Chilli, Grapes, Watermelon", "சின்ன வெங்காயம், மிளகாய், திராட்சை", "කැල්සික් ලැටොසොල් පස", "Calcic Latosols"),
    ("Kandy", "මහනුවර", "கண்டி", "මැද රට තෙත් කලාපය", "Mid-Country Wet Zone", "மத்திய ஈர வலயம்", "කෝපි, කුළුබඩු, කෙසෙල්, එළවළු", "Coffee, Spices, Banana, Vegetables", "காப்பி, மசாலா பயிர்கள்", "රතු-කහ පොඩ්සොලික් පස", "Red-Yellow Podzolic"),
    ("Nuwara Eliya", "නුවරඑළිය", "நுவரெலியா", "උඩරට තෙත් කලාපය", "Up-Country Wet Zone", "உயர் மலைநாடு", "අර්තාපල්, කැරට්, ලීක්ස්, තේ", "Potatoes, Carrots, Leeks, Tea", "உருளைக்கிழங்கு, கேரட், தேயிலை", "කඳුකර හියුමස් පස", "Mountain Humus soils")
]

MONTHS_TRILINGUAL = [
    ("September", "සැප්තැම්බර්", "செப்டம்பர்", True),
    ("October", "ඔක්තෝබර්", "அக்டோபர்", True),
    ("November", "නොවැම්බර්", "நவம்பர்", True),
    ("May", "මැයි", "மே", False),
    ("June", "ජූනි", "ஜூன்", False),
    ("July", "ජූලි", "ஜூலை", False)
]

for d_en, d_si, d_ta, z_si, z_en, z_ta, cr_si, cr_en, cr_ta, s_si, s_en in DISTRICTS:
    for m_en, m_si, m_ta, is_maha in MONTHS_TRILINGUAL:
        season_si = "මහ කන්නයේ ඊසානදිග මෝසම් වැසි ආරම්භ වන බැවින්" if is_maha else "යල කන්නයේ වියළි කාලගුණික තත්ත්වයක් පවතින බැවින්"
        season_en = "Northeast monsoon provides steady rainfall for the Maha season" if is_maha else "Dry weather prevails during the Yala period"
        season_ta = "வடகிழக்கு பருவமழை காரணமாக மகா பருவத்திற்கு ஏற்ற நீர் கிடைக்கும்" if is_maha else "யலா பருவத்தில் வறண்ட காலநிலை நிலவுகிறது"

        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"ඉදිරියට එන {m_si} මාසයේ {d_si} ප්‍රදේශයේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?"},
                {"role": "assistant", "content": f"{d_si} ප්‍රදේශය අයත් වන්නේ {z_si}ටයි. එහි ප්‍රධාන වශයෙන් {s_si} දක්නට ලැබේ. {m_si} මාසයේදී {season_si}, **{cr_si}** වැනි බෝග ඉතා සාර්ථකව වගා කළ හැක. පස පෙරළා කාබනික පොහොර යොදා බිම් සැකසීම ආරම්භ කරන්න."}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"How is the agricultural situation in {d_en} during {m_en}? What crops are recommended?"},
                {"role": "assistant", "content": f"In {d_en} ({z_en}), dominant soils are {s_en}. During {m_en}, {season_en}. Recommended high-yielding crops include **{cr_en}**. Prepare drainage channels and incorporate organic matter prior to seeding."}
            ]
        })
        all_samples.append({
            "messages": [
                {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
                {"role": "user", "content": f"{m_ta} மாதத்தில் {d_ta} பகுதியில் விவசாய நிலைமை எவ்வாறு இருக்கும்? என்ன பயிரிடலாம்?"},
                {"role": "assistant", "content": f"{d_ta} பகுதி {z_ta}க்கு உட்பட்டது. {m_ta} மாதத்தில் {season_ta}. இங்கு **{cr_ta}** போன்ற பயிர்களை வெற்றிகரமாக பயிரிடலாம். நிலத்தை நன்கு உழுது இயற்கை உரமிட்டு தயார் செய்யவும்."}
            ]
        })

random.seed(42)
random.shuffle(all_samples)

with open(DATASET_FILE, "w", encoding="utf-8") as f:
    for s in all_samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

print(f"Generated {len(all_samples)} high-quality trilingual agricultural training samples into '{DATASET_FILE}'!")

# ------------------------------------------------------------------------------
# STEP 3: Load Base Model & Tokenizer (Tesla T4 GPU)
# ------------------------------------------------------------------------------
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
print("\n" + "=" * 75)
print(f"  STEP 3: Loading Base Model: {MODEL_ID}...")
print("=" * 75)

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
print("\n" + "=" * 75)
print("  STEP 4: Attaching LoRA Layers...")
print("=" * 75)

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
# STEP 5: Tokenize with Response Masking
# ------------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  STEP 5: Formatting & Masking Tokenized Dataset...")
print("=" * 75)

raw_dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

def tokenize_with_masking(example):
    user_prompt = tokenizer.apply_chat_template(example["messages"][:-1], tokenize=False, add_generation_prompt=True)
    full_prompt = tokenizer.apply_chat_template(example["messages"], tokenize=False, add_generation_prompt=False)

    user_tokens = tokenizer(user_prompt, add_special_tokens=False)["input_ids"]
    full_tokens = tokenizer(full_prompt, max_length=512, truncation=True, add_special_tokens=False)

    input_ids = full_tokens["input_ids"]
    labels = list(input_ids)

    prompt_len = min(len(user_tokens), len(labels))
    for i in range(prompt_len):
        labels[i] = -100

    return {"input_ids": input_ids, "labels": labels}

tokenized_dataset = raw_dataset.map(tokenize_with_masking, remove_columns=["messages"])

# ------------------------------------------------------------------------------
# STEP 6: Execute Fine-Tuning
# ------------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  STEP 6: Starting LoRA Fine-Tuning on T4 GPU...")
print("=" * 75)

training_args = TrainingArguments(
    output_dir="./agri_slm_checkpoints",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    warmup_steps=20,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=torch.cuda.is_available(),
    gradient_checkpointing=True,
    logging_steps=15,
    save_strategy="no",
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
# STEP 7: Live Inference Validation (Trilingual with Sampling & Temperature)
# ------------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  STEP 7: Testing Dynamic Trilingual Inference (Temperature=0.7)...")
print("=" * 75)

model.eval()
model.config.use_cache = True

def ask_live(prompt_text):
    messages = [
        {"role": "system", "content": "You are an expert trilingual agricultural AI assistant specialized in Sri Lanka farming, crop protection, and soil management."},
        {"role": "user", "content": prompt_text}
    ]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to(device)
    im_end = tokenizer.convert_tokens_to_ids("<|im_end|>")

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=[tokenizer.eos_token_id, im_end]
        )
    ans = tokenizer.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    print(f"\nUser: {prompt_text}")
    print(f"AI  : {ans.strip()}\n" + "-" * 70)

ask_live("මිරිස් වගාවේ කොළ කොඩවීමේ රෝගය පාලනය කරන්නේ කොහොමද?")
ask_live("My soil test has N=90, P=45, K=40, pH=6.5. What crop is recommended for maximum profit?")
ask_live("யாழ்ப்பாணத்தில் செப்டம்பர் மாதத்தில் என்ன பயிர் செய்யலாம்?")

# ------------------------------------------------------------------------------
# STEP 8: AUTOMATIC WEIGHT MERGE & STANDALONE EXPORT
# ------------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  STEP 8: MERGING LORA WEIGHTS INTO STANDALONE MODEL...")
print("  (This eliminates the need to download the base model locally!)")
print("=" * 75)

STANDALONE_DIR = "./agri_slm_standalone_model"
if os.path.exists(STANDALONE_DIR):
    shutil.rmtree(STANDALONE_DIR)

# Merge LoRA layers directly into the base weights
merged_model = model.merge_and_unload()
merged_model.save_pretrained(STANDALONE_DIR, max_shard_size="2GB")
tokenizer.save_pretrained(STANDALONE_DIR)

print(f"Saved complete standalone model to '{STANDALONE_DIR}'!")

# Package into ZIP for 1-Click download
ZIP_NAME = "agri_slm_standalone_model"
shutil.make_archive(ZIP_NAME, "zip", STANDALONE_DIR)
print(f"🎉 Created '{ZIP_NAME}.zip' ready for your local backend!")

try:
    from google.colab import files
    files.download(f"{ZIP_NAME}.zip")
    print("✅ Download popup opened in your browser!")
except Exception:
    print(f"Please download '{ZIP_NAME}.zip' from the left Files tab in Google Colab.")

print("\n" + "=" * 75)
print("  ALL STEPS COMPLETE! Extract the zip into backend/trained_models/agri_slm_standalone_model")
print("=" * 75)
