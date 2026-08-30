import csv
import json
import random
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DATASET_DIR = ROOT_DIR / "SeedRecommendationEngine" / "backend" / "dataset"
OUTPUT_FILE = BACKEND_DATASET_DIR / "agricultural_chat_dataset_trilingual.jsonl"
CROP_CSV_PATH = BACKEND_DATASET_DIR / "Crop_recommendation.csv"
if not CROP_CSV_PATH.exists():
    CROP_CSV_PATH = ROOT_DIR / "dataset" / "Crop_recommendation.csv"

CROP_TRANSLATIONS = {
    "rice": {"en": "Rice (Paddy)", "si": "වී ගොවිතැන", "ta": "நெல் / அரிசி"},
    "maize": {"en": "Maize (Corn)", "si": "බඩඉරිඟු", "ta": "மக்காச்சோளம்"},
    "chickpea": {"en": "Chickpea", "si": "කඩල", "ta": "கொண்டைக்கடலை"},
    "kidneybeans": {"en": "Kidney Beans", "si": "රාජ්මා බෝංචි", "ta": "பீன்ஸ்"},
    "pigeonpeas": {"en": "Pigeon Peas", "si": "තෝර පරිප්පු", "ta": "துவரம்பருப்பு"},
    "mothbeans": {"en": "Moth Beans", "si": "කොල්ලු", "ta": "நரிப்பயறு"},
    "mungbean": {"en": "Mung Bean", "si": "මුං ඇට", "ta": "பாசிப்பயறு"},
    "blackgram": {"en": "Black Gram (Undu)", "si": "උඳු", "ta": "உளுந்து"},
    "lentil": {"en": "Lentils (Masoor)", "si": "මසූර් පරිප්පු", "ta": "பருப்பு"},
    "pomegranate": {"en": "Pomegranate", "si": "දෙළුම්", "ta": "மாதுளை"},
    "banana": {"en": "Banana", "si": "කෙසෙල්", "ta": "வாழை"},
    "mango": {"en": "Mango", "si": "අඹ", "ta": "மாம்பழம்"},
    "grapes": {"en": "Grapes", "si": "මිදි", "ta": "திராட்சை"},
    "watermelon": {"en": "Watermelon", "si": "කොමඩු", "ta": "தர்பூசணி"},
    "muskmelon": {"en": "Muskmelon / Cantaloupe", "si": "කැකිරි / කොමඩු වර්ග", "ta": "முலாம் பழம்"},
    "apple": {"en": "Apple", "si": "ඇපල්", "ta": "ஆப்பிள்"},
    "orange": {"en": "Orange / Mandarin", "si": "දොඩම්", "ta": "ஆரஞ்சு"},
    "papaya": {"en": "Papaya", "si": "පැපොල්", "ta": "பப்பாளி"},
    "coconut": {"en": "Coconut", "si": "පොල්", "ta": "தேங்காய்"},
    "cotton": {"en": "Cotton", "si": "කපු", "ta": "பருத்தி"},
    "jute": {"en": "Jute / Kenaf", "si": "හණ", "ta": "சணல்"},
    "coffee": {"en": "Coffee", "si": "කෝපි", "ta": "காப்பி"},
}

DISTRICT_INFO = {
    "Polonnaruwa": {
        "zone_si": "වියළි කලාපය (Dry Zone)",
        "zone_ta": "உலர் வலயம் (Dry Zone)",
        "zone_en": "Dry Zone",
        "soil_si": "රතු-දුඹුරු පස (Reddish Brown Earths) සහ පහත් බිම් හියුමික් මැටි පස (Low Humic Gley)",
        "soil_ta": "செம்பழுப்பு மண் (Reddish Brown Earths) மற்றும் களிமண்",
        "soil_en": "Reddish Brown Earths and Low Humic Gley soils",
        "crops": ["rice", "maize", "blackgram", "mungbean", "watermelon"],
        "maha_weather_si": "මහ කන්නයේදී (සැප්තැම්බර් සිට පෙබරවාරි දක්වා) ඊසානදිග මෝසම් වැසි ලැබෙන බැවින් කුඹුරු ගොවිතැනට ඉතා යහපත් ජල සම්පාදනයක් ලැබේ.",
        "maha_weather_ta": "மகா பருவத்தில் (செப்டம்பர் முதல் பிப்ரவரி வரை) வடகிழக்கு பருவமழை காரணமாக நெல் விவசாயத்திற்கு போதுமான நீர் கிடைக்கும்.",
        "maha_weather_en": "During the Maha season (September to February), Northeast monsoon brings abundant rainfall, ideal for extensive paddy and field crops.",
        "yala_weather_si": "යල කන්නයේදී (මැයි සිට අගෝස්තු) වියළි කාලගුණයක් පවතින බැවින් අඩු ජල අවශ්‍යතාවක් ඇති බඩඉරිඟු, මුං ඇට, උඳු සහ කොමඩු වැනි බෝග වඩාත් සුදුසු වේ.",
        "yala_weather_ta": "யலா பருவத்தில் (மே முதல் ஆகஸ்ட் வரை) வறண்ட வானிலை நிலவுவதால் குறைந்த நீர் தேவைப்படும் மக்காச்சோளம், பாசிப்பயறு போன்ற பயிர்கள் சிறந்தது.",
        "yala_weather_en": "During the Yala season (May to August), dry conditions prevail, making drought-hardy crops like maize, mungbean, and blackgram most suitable.",
    },
    "Anuradhapura": {
        "zone_si": "වියළි කලාපය (Dry Zone)",
        "zone_ta": "உலர் வலயம் (Dry Zone)",
        "zone_en": "Dry Zone",
        "soil_si": "රතු-දුඹුරු පස (Reddish Brown Earths)",
        "soil_ta": "செம்பழுப்பு மண் (Reddish Brown Earths)",
        "soil_en": "Reddish Brown Earths",
        "crops": ["rice", "maize", "blackgram", "mungbean", "chickpea", "pomegranate"],
        "maha_weather_si": "සැප්තැම්බර්/ඔක්තෝබර් සිට මහ වැසි ලැබෙන බැවින් කුඹුරු ගොවිතැනට සහ ධාන්‍ය බෝග වලට ඉතා හිතකරය.",
        "maha_weather_ta": "செப்டம்பர்/அக்டோபர் முதல் மழை பெய்வதால் நெல் மற்றும் தானிய பயிர்களுக்கு மிகவும் சாதகமானது.",
        "maha_weather_en": "Rainfall starts picking up around September/October for the Maha season, favoring paddy and other field crops.",
        "yala_weather_si": "යල කන්නයේදී ජල හිඟයක් ඇතිවිය හැකි බැවින් මුං ඇට, උඳු, සහ තල වැනි බෝග වඩාත් ප්‍රතිඵලදායකය.",
        "yala_weather_ta": "யலா பருவத்தில் நீர் பற்றாக்குறை ஏற்படலாம் என்பதால் பாசிப்பயறு, உளுந்து போன்ற பயிர்கள் உகந்தது.",
        "yala_weather_en": "Yala season brings dry weather; drought-tolerant crops like mungbean and blackgram are highly recommended.",
    },
    "Kurunegala": {
        "zone_si": "අන්තර්මැදි කලාපය (Intermediate Zone)",
        "zone_ta": "இடைநிலை வலயம் (Intermediate Zone)",
        "zone_en": "Intermediate Zone",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ රතු-දුඹුරු ලැටොසොලික් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மண்",
        "soil_en": "Red-Yellow Podzolic and Reddish Brown Latosolic soils",
        "crops": ["coconut", "rice", "banana", "papaya", "maize"],
        "maha_weather_si": "සැප්තැම්බර් මාසයේ සිට වර්ෂාපතනය ක්‍රමයෙන් වැඩිවන අතර පොල්, කෙසෙල් සහ වී වගාවට ඉතා යහපත් වේ.",
        "maha_weather_ta": "செப்டம்பர் முதல் மழை படிப்படியாக அதிகரிக்கும், இது தேங்காய், வாழை மற்றும் நெல் பயிர்ச்செய்கைக்கு நன்று.",
        "maha_weather_en": "Rainfall increases steadily from September, benefiting coconut, banana, and paddy cultivation.",
        "yala_weather_si": "මධ්‍යස්ථ වර්ෂාපතනයක් පවතින බැවින් පළතුරු සහ එළවළු වගාවන්ට සුදුසුය.",
        "yala_weather_ta": "மிதமான மழைப்பொழிவு இருப்பதால் பழங்கள் மற்றும் காய்கறிகளுக்கு ஏற்றது.",
        "yala_weather_en": "Moderate rainfall supports fruits, perennials, and short-term crops.",
    },
    "Kandy": {
        "zone_si": "තෙත් කලාපය (Wet Zone - Midcountry)",
        "zone_ta": "ஈர வலயம் (Wet Zone)",
        "zone_en": "Wet Zone (Mid-Country)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස (Red-Yellow Podzolic)",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மண்",
        "soil_en": "Red-Yellow Podzolic soils",
        "crops": ["coffee", "banana", "papaya", "rice"],
        "maha_weather_si": "නිරන්තර වැසි සහ සිසිල් දේශගුණය කුළුබඩු, කෝපි සහ උඩරට එළවළු සඳහා විශිෂ්ටයි.",
        "maha_weather_ta": "அடிக்கடி மழை மற்றும் குளிர்ந்த காலநிலை காப்பி, மசாலா பொருட்கள் மற்றும் காய்கறிகளுக்கு சிறந்தது.",
        "maha_weather_en": "High rainfall and cooler temperatures are ideal for coffee, spices, and mid-country horticulture.",
        "yala_weather_si": "නිරිතදිග මෝසම් වැසි ලැබෙන බැවින් නිරන්තර තෙතමනයක් පවතී.",
        "yala_weather_ta": "தென்மேற்கு பருவமழை காரணமாக எப்போதும் ஈரப்பதம் இருக்கும்.",
        "yala_weather_en": "Southwest monsoon provides consistent moisture throughout the season.",
    },
    "Nuwara Eliya": {
        "zone_si": "තෙත් කඳුකර කලාපය (Upcountry Wet Zone)",
        "zone_ta": "மலைநாட்டு ஈர வலயம் (Upcountry Wet Zone)",
        "zone_en": "Upcountry Wet Zone",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ කඳුකර හියුමස් සහිත පස",
        "soil_ta": "மலைநாட்டு பொட்சோலிக் மண்",
        "soil_en": "Red-Yellow Podzolic and Mountain Regosols",
        "crops": ["apple", "kidneybeans", "orange"],
        "maha_weather_si": "අධික ශීතල සහ තෙතමනය සහිත කාලගුණය උඩරට එළවළු සහ පළතුරු සඳහා යෝග්‍ය වේ.",
        "maha_weather_ta": "அதிக குளிர் மற்றும் ஈரப்பதம் மலைநாட்டு காய்கறிகள் மற்றும் பழங்களுக்கு உகந்தது.",
        "maha_weather_en": "Cool temperatures and high humidity create the perfect climate for temperate crops.",
        "yala_weather_si": "මෝසම් වැසි අධික බැවින් පාංශු ඛාදනය වැළැක්වීමේ ක්‍රමවේද අනුගමනය කිරීම වැදගත්ය.",
        "yala_weather_ta": "அதிக மழைப்பொழிவு காரணமாக மண் அரிப்பைத் தடுப்பது அவசியமாகும்.",
        "yala_weather_en": "Heavy monsoon rains require effective soil conservation and drainage practices.",
    },
    "Jaffna": {
        "zone_si": "වියළි කලාපය (Dry Zone - Peninsula)",
        "zone_ta": "உலர் வலயம் (யாழ்ப்பாணம்)",
        "zone_en": "Dry Zone (Jaffna Peninsula)",
        "soil_si": "කැල්සික් රතු-කහ ලැටොසොල් (Calcic Red Yellow Latosols)",
        "soil_ta": "சுண்ணாம்பு செம்மஞ்சள் லட்டோசோல் மண் (Calcic Red Yellow Latosols)",
        "soil_en": "Calcic Red Yellow Latosols (Limestone-based soils)",
        "crops": ["grapes", "pomegranate", "watermelon", "banana", "blackgram"],
        "maha_weather_si": "ඔක්තෝබර්-දෙසැම්බර් කාලයේ ලැබෙන ඊසානදිග මෝසම් වැසි වගාවන්ට ප්‍රධාන ජල මූලාශ්‍රය වේ.",
        "maha_weather_ta": "அக்டோபர்-டிசம்பர் வடகிழக்கு பருவமழை விவசாயத்திற்கு முக்கிய நீர் ஆதாரமாகும்.",
        "maha_weather_en": "Northeast monsoon (October-December) is the main rainy period, excellent for seasonal cultivation.",
        "yala_weather_si": "ඉතා වියළි උණුසුම් කාලගුණයක් ඇති බැවින් බිංදු ජල සම්පාදනය (Drip Irrigation) යොදාගැනීම සුදුසුය.",
        "yala_weather_ta": "மிகவும் வறண்ட காலநிலை நிலவுவதால் சொட்டு நீர் பாசனம் (Drip irrigation) சிறந்தது.",
        "yala_weather_en": "Dry and hot conditions require efficient water management like drip irrigation.",
    },
    "Galle": {
        "zone_si": "පහතරට තෙත් කලාපය (Low Country Wet Zone)",
        "zone_ta": "தாழ்நாட்டு ஈர வலயம் (Low Country Wet Zone)",
        "zone_en": "Low Country Wet Zone",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ බෝග්/අර්ධ-බෝග් පස (Bog & Half-Bog)",
        "soil_ta": "பொட்சோலிக் மற்றும் சதுப்பு நில மண்",
        "soil_en": "Red-Yellow Podzolic, Bog and Half-Bog soils",
        "crops": ["rice", "banana", "coconut", "papaya"],
        "maha_weather_si": "වසර පුරාම ඉහළ වර්ෂාපතනයක් ලැබෙන බැවින් ජලවහන පද්ධතිය නිසි ලෙස නඩත්තු කිරීම අත්‍යවශ්‍යයි.",
        "maha_weather_ta": "வருடம் முழுவதும் அதிக மழை பெய்யும் என்பதால் முறையான வடிகால் அமைப்பு அவசியமாகும்.",
        "maha_weather_en": "Year-round high rainfall requires good field drainage management for successful harvest.",
        "yala_weather_si": "නිරිතදිග මෝසමෙන් අධික වැසි ලැබෙන බැවින් කුරුඳු, පොල්, සහ කෙසෙල් වගාවන් සරුවට වැඩේ.",
        "yala_weather_ta": "தென்மேற்கு பருவமழை காரணமாக தேங்காய், வாழை போன்றவை செழிப்பாக வளரும்.",
        "yala_weather_en": "Southwest monsoon brings abundant rainfall, supporting coconut, banana, and cinnamon.",
    },
    "Hambantota": {
        "zone_si": "අර්ධ ශුෂ්ක වියළි කලාපය (Semi-Arid Dry Zone)",
        "zone_ta": "அரை வறண்ட வலயம் (Semi-Arid Dry Zone)",
        "zone_en": "Semi-Arid Dry Zone",
        "soil_si": "රතු-දුඹුරු පස, සොලොනෙට්ස් (Solodized Solonetz) සහ රෙගොසෝල් පස",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் உவர்மண்",
        "soil_en": "Reddish Brown Earths, Solonetz, and Regosols",
        "crops": ["watermelon", "cotton", "banana", "pomegranate", "mungbean", "blackgram"],
        "maha_weather_si": "නොවැම්බර්-දෙසැම්බර් කෙටි වැසි සමය උපරිමයෙන් ප්‍රයෝජනයට ගෙන බෝග ස්ථාපනය කළ යුතුය.",
        "maha_weather_ta": "நவம்பர்-டிசம்பர் குறுகிய மழைக்காலத்தை பயன்படுத்தி பயிர்களை நடவு செய்ய வேண்டும்.",
        "maha_weather_en": "The short rainy period in Nov-Dec should be utilized promptly for crop establishment.",
        "yala_weather_si": "ඉහළ උෂ්ණත්වයක් සහ වියළි බවක් පවතින බැවින් කොමඩු, කපු සහ මුං වැනි බෝග වඩාත් සුදුසුය.",
        "yala_weather_ta": "அதிக வெப்பம் மற்றும் வறட்சி காரணமாக தர்பூசணி, பருத்தி, பாசிப்பயறு போன்றவை சிறந்தது.",
        "yala_weather_en": "High temperatures and dry conditions make watermelon, cotton, and drought-hardy pulses most suitable.",
    },
    "Badulla": {
        "zone_si": "උඩරට අන්තර්මැදි කලාපය (Upcountry Intermediate Zone)",
        "zone_ta": "மலைநாட்டு இடைநிலை வலயம்",
        "zone_en": "Upcountry Intermediate Zone",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ නොමේරූ දුඹුරු ලෝම පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மண்",
        "soil_en": "Red-Yellow Podzolic and Immature Brown Loams",
        "crops": ["maize", "kidneybeans", "banana", "orange", "pomegranate"],
        "maha_weather_si": "මහ වැසි සමයේ එළවළු, බඩඉරිඟු සහ පළතුරු වගාවන් ඉතා සරුවට කළ හැක.",
        "maha_weather_ta": "மகா மழைக்காலத்தில் காய்கறிகள், மக்காச்சோளம் செழிப்பாக வளரும்.",
        "maha_weather_en": "Maha rains offer excellent conditions for vegetables, maize, and citrus fruits.",
        "yala_weather_si": "සෞම්‍ය දේශගුණයක් පවතින අතර තෙතමනය ආරක්ෂා කරමින් බෝග වගා කළ හැක.",
        "yala_weather_ta": "மிதமான காலநிலையைக் கொண்டு பயிர் செய்யலாம்.",
        "yala_weather_en": "Mild weather supports diversified horticulture and cash crops.",
    },
    "Batticaloa": {
        "zone_si": "නැගෙනහිර වියළි කලාපය (Eastern Dry Zone)",
        "zone_ta": "கிழக்கு உலர் வலயம் (மட்டக்களப்பு)",
        "zone_en": "Eastern Dry Zone",
        "soil_si": "වැලි සහිත රෙගොසෝල් සහ පහත් බිම් ඇලුවියල් පස",
        "soil_ta": "மணல் நிறைந்த மண் மற்றும் வண்டல் மண்",
        "soil_en": "Sandy Regosols and Lowland Alluvial Soils",
        "crops": ["rice", "coconut", "watermelon", "blackgram", "chickpea"],
        "maha_weather_si": "ඊසානදිග මෝසම් වැසි අධිකව ලැබෙන බැවින් කුඹුරු ගොවිතැනට ප්‍රමුඛස්ථානය හිමිවේ.",
        "maha_weather_ta": "வடகிழக்கு பருவமழை தீவிரமாக இருப்பதால் நெல் விவசாயம் முதன்மையானது.",
        "maha_weather_en": "Intense Northeast monsoon rains make it the prime season for extensive paddy.",
        "yala_weather_si": "උණුසුම් වියළි කාලගුණයේදී පොල්, කොමඩු සහ කෙටි කාලීන ධාන්‍ය බෝග සුදුසුයි.",
        "yala_weather_ta": "வறண்ட காலத்தில் தேங்காய், தர்பூசணி பயிரிடலாம்.",
        "yala_weather_en": "Hot and dry conditions favor coconut, watermelon, and drought-tolerant legumes.",
    }
}

MONTHS_SEASONS = [
    {"name_en": "January", "name_si": "ජනවාරි", "name_ta": "ஜனவரி", "season": "Maha"},
    {"name_en": "February", "name_si": "පෙබරවාරි", "name_ta": "பிப்ரவரி", "season": "Maha"},
    {"name_en": "March", "name_si": "මාර්තු", "name_ta": "மார்ச்", "season": "Maha Harvest / Inter-monsoon"},
    {"name_en": "April", "name_si": "අප්‍රේල්", "name_ta": "ஏப்ரல்", "season": "Inter-monsoon / Yala Prep"},
    {"name_en": "May", "name_si": "මැයි", "name_ta": "மே", "season": "Yala"},
    {"name_en": "June", "name_si": "ජූනි", "name_ta": "ஜூன்", "season": "Yala"},
    {"name_en": "July", "name_si": "ජූලි", "name_ta": "ஜூலை", "season": "Yala"},
    {"name_en": "August", "name_si": "අගෝස්තු", "name_ta": "ஆகஸ்ட்", "season": "Yala Harvest"},
    {"name_en": "September", "name_si": "සැප්තැම්බර්", "name_ta": "செப்டம்பர்", "season": "Maha Prep / Early Monsoon"},
    {"name_en": "October", "name_si": "ඔක්තෝබර්", "name_ta": "அக்டோபர்", "season": "Maha"},
    {"name_en": "November", "name_si": "නොවැම්බර්", "name_ta": "நவம்பர்", "season": "Maha Peak Rain"},
    {"name_en": "December", "name_si": "දෙසැම්බර්", "name_ta": "டிசம்பர்", "season": "Maha"},
]

SOIL_DIAGNOSTICS = [
    {
        "topic": "acidic_soil",
        "q_si": ["පසේ ආම්ලිකතාවය (pH අඩු වීම) පාලනය කරන්නේ කොහොමද?", "මගේ ඉඩමේ පස හරිම ඇඹුල් / ආම්ලිකයි (pH 5.0 ට අඩුයි). කුමක් කළ යුතුද?", "ඇසිඩ් පසට යොදන්න හොඳ පොහොර හෝ ද්‍රව්‍ය මොනවාද?"],
        "a_si": [
            "පසේ ආම්ලිකතාවය (pH 5.5 ට වඩා අඩු වීම) පාලනය කිරීමට හොඳම ක්‍රමය වන්නේ ඩොලමයිට් (Dolomite) හෝ කෘෂිකාර්මික හුණු (Agricultural Lime) පසට මිශ්‍ර කිරීමයි. බෝග සිටුවීමට සති 2-3කට පෙර හෙක්ටයාරයකට හෝ පර්චසයකට නිර්දේශිත මාත්‍රාවෙන් යොදා පස පෙරළන්න. එමගින් කැල්සියම් සහ මැග්නීසියම් පෝෂකද පසට එක්වේ.",
            "ආම්ලික පසක ශාක වලට පොස්පරස් හා අනෙකුත් පෝෂක උරාගැනීම අපහසු වේ. මේ සඳහා ඩොලමයිට් යෙදීම අත්‍යවශ්‍යයි. මීට අමතරව හොඳින් දිරාපත් වූ කාබනික කොම්පෝස්ට් පොහොර යෙදීමෙන් පසේ pH අගය ස්වභාවිකවම උදාසීන මට්ටමකට (pH 6.0 - 6.5) ගෙන ආ හැක."
        ],
        "q_en": ["How can I manage and correct acidic soil with low pH?", "My farm soil is very acidic (pH under 5.2). What should I apply?", "What is the recommended treatment for high soil acidity?"],
        "a_en": [
            "To correct acidic soil (pH below 5.5), apply agricultural lime or dolomite 2-3 weeks prior to planting. Dolomite neutralizes excessive acidity while supplementing essential Calcium and Magnesium. Incorporating well-rotted organic compost also buffers soil pH towards the optimal 6.0 - 6.8 range.",
            "High soil acidity restricts root phosphorus uptake and triggers aluminum toxicity. Broadcast dolomite at recommended agricultural dosages and till well into topsoil. Maintain regular organic matter additions to enhance buffering capacity."
        ],
        "q_ta": ["அமில மண்ணின் pH அளவை எவ்வாறு அதிகரிப்பது?", "எனது நிலத்தில் pH 5.0 க்கும் குறைவாக உள்ளது. என்ன தீர்வு?", "அமில மண்ணை சமநிலைப்படுத்துவது எப்படி?"],
        "a_ta": [
            "மண்ணின் அமிலத்தன்மையை (pH 5.5க்கு கீழ்) குறைக்க டோலமைட் (Dolomite) அல்லது விவசாய சுண்ணாம்பு இட வேண்டும். நடவு செய்வதற்கு 2-3 வாரங்களுக்கு முன் மண்ணில் கலந்து விடவும். இது மண்ணின் pH அளவை உயர்த்தி ஊட்டச்சத்துக்களை எளிதாக பயிர்கள் பெற உதவும்.",
            "அமிலத்தன்மை அதிகம் உள்ள நிலங்களில் இயற்கை உரம் மற்றும் டோலமைட் இடுவதன் மூலம் மண்ணின் வளம் அதிகரித்து பயிர்கள் சிறந்த முறையில் வளரும்."
        ]
    },
    {
        "topic": "alkaline_saline_soil",
        "q_si": ["පසේ ලවණතාවය හෝ භාස්මිකතාවය (pH 8.0 ට වැඩි) අඩු කරන්නේ කොහොමද?", "ලුණු සහිත / ක්ෂාරීය පස සාරවත් කරගන්නේ කෙසේද?"],
        "a_si": [
            "භාස්මික හෝ ලවණ සහිත පසක (pH 7.5 - 8.5) තත්ත්වය යහපත් කිරීමට ජිප්සම් (Gypsum / Calcium Sulfate) පසට එක් කරන්න. මීට අමතරව අධිකව කාබනික කොම්පෝස්ට්, දහයියා අළු සහ කොළ පොහොර එකතු කිරීමෙන් පසේ වායු සංසරණය හා සාරවත් බව වැඩිදියුණු වේ.",
            "ලවණ පසෙහි ජලය හොඳින් බැසයාමට කානු සකස් කිරීම සහ ජිප්සම් යෙදීම මගින් අතිරික්ත සෝඩියම් ඉවත් කරගත හැක. ලවණතාවයට ඔරොත්තු දෙන බෝග තෝරාගැනීමද වැදගත්ය."
        ],
        "q_en": ["How to treat alkaline or saline soil with high pH?", "What remedies exist for saline soil and alkaline conditions?"],
        "a_en": [
            "To rectify alkaline and saline soils (pH > 7.8), incorporate agricultural Gypsum (Calcium Sulfate) and generous amounts of organic compost. Gypsum displaces harmful sodium ions, while organic matter improves soil structure and drainage.",
            "Ensure proper drainage channels to flush out accumulated salts during heavy irrigation or rains. Green manuring and mulching also help reduce surface salinity buildup."
        ],
        "q_ta": ["கார மண் மற்றும் உவர் மண்ணை எவ்வாறு சீரமைப்பது?", "மண்ணில் pH 8.0 க்கும் அதிகமாக இருந்தால் என்ன செய்ய வேண்டும்?"],
        "a_ta": [
            "காரத்தன்மை மற்றும் உவர் மண்ணை சீரமைக்க ஜிப்சம் (Gypsum) மற்றும் அதிகளவு மக்கிய இயற்கை உரங்களை இட வேண்டும். இது மண்ணில் உள்ள அதிகப்படியான உப்பை வெளியேற்றி மண் வளத்தை கூட்டும்.",
            "முறையான வடிகால் அமைப்பதன் மூலம் மழைநீருடன் உப்பை வெளியேற்றி பயிர்களுக்கு உகந்த சூழலை உருவாக்கலாம்."
        ]
    },
    {
        "topic": "nitrogen_management",
        "q_si": ["නයිට්‍රජන් (N) ඌනතාවය හඳුනාගන්නේ කොහොමද? පිළියම් මොනවාද?", "බෝගයේ කොළ කහ පාට වෙලා. නයිට්‍රජන් අඩුද?"],
        "a_si": [
            "ශාකයේ යටි කොළ මුලින්ම කහ පැහැ ගැන්වීම සහ වර්ධනය බාල වීම නයිට්‍රජන් (N) ඌනතාවයේ ප්‍රධාන ලක්ෂණයකි. පිළියමක් ලෙස යූරියා (Urea) පොහොර නිර්දේශිත මාත්‍රාවෙන් යෙදීම හෝ නයිට්‍රජන් බහුල ග්ලිරිසීඩියා කොළ පොහොර සහ කොම්පෝස්ට් යෙදීම සුදුසුය.",
            "නයිට්‍රජන් අඩු වූ විට ප්‍රභාසංස්ලේෂණය අඩපණ වේ. ක්ෂණික විසඳුමක් ලෙස යූරියා 1% ද්‍රාවණයක් පත්‍ර මතට ඉසීම (Foliar spray) හෝ පසට මූලික පොහොර ලෙස යූරියා යෙදීම කළ හැක."
        ],
        "q_en": ["How to identify and cure Nitrogen (N) deficiency in crops?", "Leaves are turning pale yellow from the bottom. Is it lack of Nitrogen?"],
        "a_en": [
            "Nitrogen deficiency manifests as chlorosis (yellowing) starting on older lower leaves and stunted vegetative growth. Address this by applying balanced Urea fertilizer according to Department of Agriculture guidelines, or incorporating legume green manure (Gliricidia).",
            "For rapid relief of severe nitrogen starvation, a 1-2% foliar urea spray or prompt side-dressing with ammonium/urea-based fertilizer provides fast nutrient recovery."
        ],
        "q_ta": ["நைட்ரஜன் குறைபாட்டின் அறிகுறிகள் என்ன? எவ்வாறு சரிசெய்வது?", "இலைகள் மஞ்சள் நிறமாக மாறுகின்றன, என்ன உரம் இட வேண்டும்?"],
        "a_ta": [
            "அடி இலைகள் மஞ்சள் நிறமாக மாறுவதும் வளர்ச்சி குறைவதும் நைட்ரஜன் குறைபாட்டின் அறிகுறியாகும். இதற்கு பரிந்துரைக்கப்பட்ட அளவு யூரியா (Urea) அல்லது பசுந்தாள் உரம் இடுங்கள்.",
            "நைட்ரஜன் பற்றாக்குறையை போக்க மக்கிய உரம் மற்றும் தழைச்சத்து உரங்களை சரியான முறையில் பயிருக்கு வழங்குங்கள்."
        ]
    }
]

GENERAL_CONVERSATIONS = [
    {
        "q_si": "ඔබ කවුද? ඔබට මට උදව් කළ හැක්කේ කෙසේද?",
        "a_si": "මම ශ්‍රී ලංකාවේ පස, දේශගුණය සහ බෝග නිර්දේශ පිළිබඳව විශේෂඥ දැනුම සහිත කෘෂිකාර්මික AI සහායකයා (Agricultural SLM) වෙමි. ශ්‍රී ලංකාවේ ඕනෑම දිස්ත්‍රික්කයකට ගැළපෙන බෝග, මාසික කාලගුණ තත්ත්වයන්, පසේ NPK සහ pH පෝෂක මට්ටම් කළමනාකරණය පිළිබඳව ඕනෑම ප්‍රශ්නයක් මගෙන් විමසන්න!"
    },
    {
        "q_si": "හෙලෝ, මට කෘෂිකර්මාන්තය ගැන දැනගන්න පුළුවන්ද?",
        "a_si": "ආයුබෝවන්! අනිවාර්යයෙන්ම පුළුවන්. ඔබගේ ගොවිබිම පිහිටි ප්‍රදේශය, පසේ පරීක්ෂණ දත්ත හෝ ඔබ වගා කිරීමට බලාපොරොත්තු වන මාසය පවසන්න. මම ඔබට වඩාත්ම සුදුසු බෝග සහ උපදෙස් ලබාදෙන්නම්."
    },
    {
        "q_en": "Who are you and what assistance can you provide?",
        "a_en": "I am an intelligent Trilingual Agricultural AI Assistant specialized in Sri Lankan soil classification, agronomy, and seed recommendation. You can ask me about regional crop suitability across all 25 districts, seasonal Maha/Yala climate advisories, and soil N-P-K nutrient optimization."
    },
    {
        "q_en": "Hello, can you help me with farming advice for Sri Lanka?",
        "a_en": "Hello! Yes, absolutely. Please share your district, intended planting month, or soil test metrics (pH, Nitrogen, Phosphorus, Potassium). I will provide customized agronomic recommendations to maximize your harvest yield."
    },
    {
        "q_ta": "நீங்கள் யார்? நீங்கள் எனக்கு எவ்வாறு உதவ முடியும்?",
        "a_ta": "நான் இலங்கையின் மண், காலநிலை மற்றும் பயிர் பரிந்துரைகளுக்கான விசேட AI விவசாய உதவியாளர் ஆவேன். எந்தவொரு மாவட்டத்திற்கும் ஏற்ற பயிர்கள், பருவ கால ஆலோசனைகள் மற்றும் மண் ஊட்டச்சத்துக்கள் குறித்து என்னிடம் கேட்கலாம்."
    },
    {
        "q_ta": "வணக்கம், விவசாயம் பற்றி ஆலோசனை பெற முடியுமா?",
        "a_ta": "வணக்கம்! நிச்சயமாக. உங்கள் மாவட்டம், பயிரிட உத்தேசித்துள்ள மாதம் அல்லது மண்ணின் நிலை (NPK, pH) பற்றி கூறுங்கள். சிறந்த பயிர் வழிகாட்டலை நான் வழங்குகிறேன்."
    }
]

def generate_district_month_samples():
    samples = []
    
    for district, d_data in DISTRICT_INFO.items():
        for m in MONTHS_SEASONS:
            month_en = m["name_en"]
            month_si = m["name_si"]
            month_ta = m["name_ta"]
            is_maha = m["season"].startswith("Maha")
            
            weather_si = d_data["maha_weather_si"] if is_maha else d_data["yala_weather_si"]
            weather_ta = d_data["maha_weather_ta"] if is_maha else d_data["yala_weather_ta"]
            weather_en = d_data["maha_weather_en"] if is_maha else d_data["yala_weather_en"]
            
            crops_si = ", ".join([CROP_TRANSLATIONS[c]["si"] for c in d_data["crops"][:4]])
            crops_ta = ", ".join([CROP_TRANSLATIONS[c]["ta"] for c in d_data["crops"][:4]])
            crops_en = ", ".join([CROP_TRANSLATIONS[c]["en"] for c in d_data["crops"][:4]])
            
            # --- SINHALA VARIATIONS (Natural Conversational Phrasing) ---
            si_questions = [
                f"ඉදිරියට එන {month_si} මාසයේ {district} ප්‍රදේශයේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?",
                f"{district} දිස්ත්‍රික්කයේ {month_si} මාසේ වගා කරන්න සුදුසු බෝග මොනවද? දේශගුණය සහ පස කොහොමද?",
                f"{month_si} මාසයේ {district} වල ගොවිතැන් කරන්න හොඳයිද? පසේ සහ කාලගුණයේ තත්ත්වය පහදන්න.",
                f"{district} වල {month_si} මාසෙට හරියන වගාවන් මොනවද?",
                f"මගේ ගොවිබිම තියෙන්නේ {district} වල. {month_si} මාසයේ කුමක් වගා කිරීමෙන්ද වැඩිම ලාභයක් ලබන්න පුළුවන්?",
            ]
            
            si_answers = [
                f"{month_si} මාසයේ {district} ප්‍රදේශය අයත් වන්නේ {d_data['zone_si']}ටයි. ප්‍රධාන වශයෙන් {d_data['soil_si']} දක්නට ලැබේ. {weather_si} මෙම කාලසීමාව තුළ {crops_si} වැනි බෝග සාර්ථකව වගා කළ හැකි අතර, නිසි පාංශු කළමනාකරණය මගින් ඉහළ අස්වැන්නක් ලබාගත හැක.",
                f"{district} ප්‍රදේශයේ {month_si} මාසයේ කාලගුණය සලකා බැලීමේදී, {weather_si} ප්‍රදේශයේ පස {d_data['soil_si']} වන බැවින් {crops_si} වගා කිරීමට ඉතා හිතකර තත්ත්වයක් පවතී. කාබනික පොහොර සමඟ සමබර පෝෂක කළමනාකරණයක් සිදුකිරීමෙන් සාර්ථක අස්වැන්නක් ලබාගත හැක.",
                f"{district} දිස්ත්‍රික්කයේ {month_si} මාසයේ වගා කටයුතු සඳහා කාලගුණය ඉතා හිතකරය. {weather_si} එහි පස {d_data['soil_si']} ගණයට වැටෙන බැවින් {crops_si} බෝග සඳහා ඉහළ අස්වනු විභවයක් පවතී.",
            ]
            
            for q in si_questions:
                samples.append({
                    "messages": [
                        {"role": "user", "content": q},
                        {"role": "assistant", "content": random.choice(si_answers)}
                    ]
                })

            # --- ENGLISH VARIATIONS ---
            en_questions = [
                f"How is the agricultural and crop condition in {district} during {month_en}? What should I grow?",
                f"What crops are recommended for {district} in {month_en}, and how is the soil and weather?",
                f"Is {month_en} a good time for farming in {district}? Tell me about climate and suitable seeds.",
                f"I have land in {district}. What should I cultivate in {month_en}?",
            ]
            
            en_answers = [
                f"In {month_en}, {district} is situated in the {d_data['zone_en']} characterized by {d_data['soil_en']}. {weather_en} Recommended crops with high yield potential include {crops_en}. Proper soil conditioning and moisture management will ensure a bountiful harvest.",
                f"For {district} during {month_en}, climatic records show that {weather_en} Given the fertile {d_data['soil_en']}, farmers are advised to cultivate {crops_en} for optimal productivity.",
                f"Cultivation conditions in {district} for {month_en} are favorable. {weather_en} The prevailing {d_data['soil_en']} provides excellent support for {crops_en}."
            ]
            
            for q in en_questions:
                samples.append({
                    "messages": [
                        {"role": "user", "content": q},
                        {"role": "assistant", "content": random.choice(en_answers)}
                    ]
                })

            # --- TAMIL VARIATIONS ---
            ta_questions = [
                f"{month_ta} மாதத்தில் {district} பகுதியில் பயிர்ச்செய்கை நிலைமை எவ்வாறு இருக்கும்? என்ன பயிரிடலாம்?",
                f"{district} மாவட்டத்தில் {month_ta} மாதத்தில் என்ன பயிர்களை நடவு செய்யலாம்? மண் மற்றும் வானிலை எப்படி?",
                f"{month_ta} மாதத்தில் {district} விவசாயம் செய்ய உகந்ததா? சிறந்த பயிர்களை பரிந்துரைக்கவும்.",
                f"{district} இல் {month_ta} மாதத்திற்கு ஏற்ற பயிர்கள் யாவை?",
            ]
            
            ta_answers = [
                f"{month_ta} மாதத்தில் {district} பகுதி {d_data['zone_ta']}க்கு உட்பட்டது. இங்கு பிரதானமாக {d_data['soil_ta']} காணப்படுகிறது. {weather_ta} இக்காலத்தில் {crops_ta} போன்ற பயிர்களை வெற்றிகரமாக பயிரிடலாம். முறையான பராமரிப்பு மூலம் சிறந்த விளைச்சலை பெறலாம்.",
                f"{district} மாவட்டத்தில் {month_ta} மாத வானிலையை நோக்கும்போது, {weather_ta} இங்குள்ள {d_data['soil_ta']}க்கு {crops_ta} பயிரிடுவது அதிக நன்மையளிக்கும்.",
            ]
            
            for q in ta_questions:
                samples.append({
                    "messages": [
                        {"role": "user", "content": q},
                        {"role": "assistant", "content": random.choice(ta_answers)}
                    ]
                })
                
    return samples

def generate_soil_diagnostics_samples():
    samples = []
    for diag in SOIL_DIAGNOSTICS:
        for q in diag["q_si"]:
            samples.append({
                "messages": [
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": random.choice(diag["a_si"])}
                ]
            })
        for q in diag["q_en"]:
            samples.append({
                "messages": [
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": random.choice(diag["a_en"])}
                ]
            })
        for q in diag["q_ta"]:
            samples.append({
                "messages": [
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": random.choice(diag["a_ta"])}
                ]
            })
    return samples

def generate_crop_csv_samples():
    samples = []
    if not CROP_CSV_PATH.exists():
        return samples
        
    with open(CROP_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        # Sample 500 records
        sampled_rows = random.sample(rows, min(500, len(rows)))
        
        for row in sampled_rows:
            crop = row["label"].strip().lower()
            n = float(row["N"])
            p = float(row["P"])
            k = float(row["K"])
            temp = round(float(row["temperature"]), 1)
            humidity = round(float(row["humidity"]), 1)
            ph = round(float(row["ph"]), 1)
            rainfall = round(float(row["rainfall"]), 1)
            
            crop_info = CROP_TRANSLATIONS.get(crop, {"en": crop.capitalize(), "si": crop, "ta": crop})
            
            # Sinhala Questions & Answers
            q_si_variants = [
                f"මගේ පසේ පරීක්ෂණ දත්ත N={n:.0f}, P={p:.0f}, K={k:.0f}, සහ pH={ph:.1f} වේ. උෂ්ණත්වය {temp}°C පමණ වේ නම් නිර්දේශිත බෝගය කුමක්ද?",
                f"පසේ N={n:.0f}, P={p:.0f}, K={k:.0f}, pH={ph:.1f}, ආර්ද්‍රතාව {humidity}% සහ වර්ෂාපතනය {rainfall}mm තත්ත්වයන් යටතේ වැඩිම ඵලදාවක් දෙන බෝගය කුමක්ද?",
            ]
            a_si = f"ඔබගේ පස් පරීක්ෂණ දත්ත (N:{n:.0f}, P:{p:.0f}, K:{k:.0f}, pH:{ph:.1f}) සහ දේශගුණික තත්ත්වයන් (උෂ්ණත්වය {temp}°C, වර්ෂාපතනය {rainfall}mm) සලකා බැලීමේදී, මෙම පරිසරයට වඩාත්ම යෝග්‍ය සහ ඉහළ අස්වැන්නක් ලබාදෙන බෝගය වන්නේ **{crop_info['si']} ({crop_info['en']})** වේ. ප්‍රශස්ත පාංශු තෙතමනය පවත්වා ගනිමින් නිර්දේශිත පොහොර මාත්‍රා යොදන්න."
            
            for q_si in q_si_variants:
                samples.append({
                    "messages": [
                        {"role": "user", "content": q_si},
                        {"role": "assistant", "content": a_si}
                    ]
                })
            
            # English Questions & Answers
            q_en_variants = [
                f"My soil test shows N={n:.0f}, P={p:.0f}, K={k:.0f}, and pH={ph:.1f}. What is the most recommended crop for high yield?",
                f"Given soil parameters N={n:.0f}, P={p:.0f}, K={k:.0f}, pH={ph:.1f}, temperature={temp}°C, humidity={humidity}%, and rainfall={rainfall}mm, what crop should I plant?",
            ]
            a_en = f"Based on your soil nutrient metrics (N:{n:.0f}, P:{p:.0f}, K:{k:.0f}, pH:{ph:.1f}) and environmental indicators (Temp:{temp}°C, Rainfall:{rainfall}mm), the prime recommended crop is **{crop_info['en']}**. This crop exhibits maximum yield efficiency under these specific soil-climate dynamics."
            
            for q_en in q_en_variants:
                samples.append({
                    "messages": [
                        {"role": "user", "content": q_en},
                        {"role": "assistant", "content": a_en}
                    ]
                })

            # Tamil Questions & Answers
            q_ta = f"மண் பரிசோதனையில் N={n:.0f}, P={p:.0f}, K={k:.0f}, pH={ph:.1f} மற்றும் வெப்பநிலை {temp}°C என உள்ளது. அதிக விளைச்சல் தரும் சிறந்த பயிர் எது?"
            a_ta = f"உங்கள் மண் ஊட்டச்சத்து அளவுகள் (N:{n:.0f}, P:{p:.0f}, K:{k:.0f}, pH:{ph:.1f}) மற்றும் காலநிலைக்கு மிகவும் பொருத்தமான அதிக மகசூல் தரும் பயிர் **{crop_info['ta']} ({crop_info['en']})** ஆகும்."
            samples.append({
                "messages": [
                    {"role": "user", "content": q_ta},
                    {"role": "assistant", "content": a_ta}
                ]
            })
            
    return samples

def main():
    print("Generating comprehensive Trilingual Agricultural Chat Dataset...")
    all_samples = []
    
    # 1. District & Seasonal Advisories
    district_samples = generate_district_month_samples()
    print(f"Generated {len(district_samples)} district-month conversational samples.")
    all_samples.extend(district_samples)
    
    # 2. Soil & Nutrient Diagnostics
    diag_samples = generate_soil_diagnostics_samples()
    print(f"Generated {len(diag_samples)} soil diagnostic samples.")
    all_samples.extend(diag_samples)
    
    # 3. Real Crop Recommendation Metrics
    crop_samples = generate_crop_csv_samples()
    print(f"Generated {len(crop_samples)} crop parameter prediction samples.")
    all_samples.extend(crop_samples)
    
    # 4. General Conversational Openers
    for conv in GENERAL_CONVERSATIONS:
        if "q_si" in conv:
            all_samples.append({"messages": [{"role": "user", "content": conv["q_si"]}, {"role": "assistant", "content": conv["a_si"]}]})
        if "q_en" in conv:
            all_samples.append({"messages": [{"role": "user", "content": conv["q_en"]}, {"role": "assistant", "content": conv["a_en"]}]})
        if "q_ta" in conv:
            all_samples.append({"messages": [{"role": "user", "content": conv["q_ta"]}, {"role": "assistant", "content": conv["a_ta"]}]})
            
    # Shuffle samples
    random.seed(42)
    random.shuffle(all_samples)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in all_samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"Dataset generated successfully with {len(all_samples)} high-quality trilingual samples at:\n{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
