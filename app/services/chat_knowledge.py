from typing import Any, Dict, Optional, Tuple

# Comprehensive Agricultural & Agro-Ecological Knowledge for all 25 Sri Lankan Districts
DISTRICT_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "Polonnaruwa": {
        "zone_si": "වියළි කලාපය (DL1c / DL1b)",
        "zone_ta": "உலர் வலயம் (DL1c / DL1b)",
        "zone_en": "Dry Zone (DL1c / DL1b)",
        "soil_si": "රතු-දුඹුරු පස (Reddish Brown Earths) සහ පහත් බිම් හියුමික් මැටි පස (LHG)",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் களிமண் (LHG)",
        "soil_en": "Reddish Brown Earths & Low Humic Gley soils",
        "maha_crops_si": "වී ගොවිතැන, බඩඉරිඟු, උඳු, මුං ඇට සහ මිරිස්",
        "maha_crops_ta": "நெல், மக்காச்சோளம், உளுந்து, பாசிப்பயறு மற்றும் மிளகாய்",
        "maha_crops_en": "Paddy (Rice), Maize, Blackgram, Mungbean, and Chilli",
        "yala_crops_si": "කොමඩු, මුං ඇට, රටකජු, තල සහ සෝයා බෝංචි",
        "yala_crops_ta": "தர்பூசணி, பாசிப்பயறு, நிலக்கடலை, எள் மற்றும் சோயாபீன்ஸ்",
        "yala_crops_en": "Watermelon, Mungbean, Groundnut, Sesame, and Soybean",
    },
    "Anuradhapura": {
        "zone_si": "වියළි කලාපය (DL1b)",
        "zone_ta": "உலர் வலயம் (DL1b)",
        "zone_en": "Dry Zone (DL1b)",
        "soil_si": "රතු-දුඹුරු පස (Reddish Brown Earths) සහ පහත් බිම් හියුමික් පස",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் தாழ் நில மட்கிய மண்",
        "soil_en": "Reddish Brown Earths & Low Humic Gley",
        "maha_crops_si": "වී, බඩඉරිඟු, කඩල, උඳු, කුරක්කන් සහ මිරිස්",
        "maha_crops_ta": "நெல், மக்காச்சோளம், கொண்டைக்கடலை, உளுந்து மற்றும் மிளகாய்",
        "maha_crops_en": "Paddy, Maize, Chickpea, Blackgram, Finger Millet, and Chilli",
        "yala_crops_si": "මුං ඇට, තල, කොමඩු, රටකජු සහ ලූනු",
        "yala_crops_ta": "பாசிப்பயறு, எள், தர்பூசணி, நிலக்கடலை மற்றும் வெங்காயம்",
        "yala_crops_en": "Mungbean, Sesame, Watermelon, Groundnut, and Onion",
    },
    "Kurunegala": {
        "zone_si": "අන්තර්මැදි කලාපය (IL1a / IL1b)",
        "zone_ta": "இடைநிலை வலயம் (IL1a / IL1b)",
        "zone_en": "Intermediate Zone (IL1a / IL1b)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ රතු-දුඹුරු ලැටොසොලික් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் லேடோசோலிக் மண்",
        "soil_en": "Red-Yellow Podzolic & Reddish Brown Latosolic soils",
        "maha_crops_si": "පොල්, වී, කෙසෙල්, පැපොල්, බඩඉරිඟු සහ අල බෝග",
        "maha_crops_ta": "தேங்காய், நெல், வாழை, பப்பாளி, சோளம் மற்றும் கிழங்கு வகைகள்",
        "maha_crops_en": "Coconut, Paddy, Banana, Papaya, Maize, and Root Crops",
        "yala_crops_si": "එළවළු, පලතුරු, මුං ඇට, සෝයා සහ ඉඟුරු",
        "yala_crops_ta": "காய்கறிகள், பழங்கள், பாசிப்பயறு, சோயா மற்றும் இஞ்சி",
        "yala_crops_en": "Vegetables, Tropical Fruits, Mungbean, Soy, and Ginger",
    },
    "Kandy": {
        "zone_si": "මැද රට තෙත් කලාපය (WM1 / WM2)",
        "zone_ta": "மத்திய மலைநாட்டு ஈர வலயம் (WM1 / WM2)",
        "zone_en": "Mid-Country Wet Zone (WM1 / WM2)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස (නැඹුරු බෑවුම් සහිත)",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மண் (சரிவான நிலம்)",
        "soil_en": "Red-Yellow Podzolic soils (Hilly Terrain)",
        "maha_crops_si": "කෝපි, කරාබුනැටි, සාදික්කා, කුරුඳු, කෙසෙල් සහ උඩරට එළවළු",
        "maha_crops_ta": "காப்பி, கிராம்பு, ஜாதிக்காய், இலவங்கப்பட்டை, வாழை மற்றும் காய்கறிகள்",
        "maha_crops_en": "Coffee, Cloves, Nutmeg, Cinnamon, Banana, and Up-Country Veg",
        "yala_crops_si": "තේ, කුළුබඩු, පැපොල්, මඤ්ඤොක්කා සහ පළතුරු",
        "yala_crops_ta": "தேயிலை, மசாலா பயிர்கள், பப்பாளி, மரவள்ளி மற்றும் பழங்கள்",
        "yala_crops_en": "Tea, Spices, Papaya, Cassava, and Perennial Fruits",
    },
    "Nuwara Eliya": {
        "zone_si": "උඩරට තෙත් කලාපය (WU1 / WU2)",
        "zone_ta": "உயர் மலைநாட்டு ஈர வலயம் (WU1 / WU2)",
        "zone_en": "Up-Country Wet Zone (WU1 / WU2)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ කඳුකර හියුමස් බහුල පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் கரிம மட்கிய மண்",
        "soil_en": "Red-Yellow Podzolic & Mountain Humus soils",
        "maha_crops_si": "අල (Potato), කැරට්, ලීක්ස්, ගෝවා, බීට්රූට් සහ ස්ට්‍රෝබෙරි",
        "maha_crops_ta": "உருளைக்கிழங்கு, கேரட், லீக்ஸ், முட்டைக்கோஸ், பீட்ரூட் மற்றும் ஸ்ட்ராபெரி",
        "maha_crops_en": "Potatoes, Carrots, Leeks, Cabbage, Beetroot, and Strawberries",
        "yala_crops_si": "උසස් තත්ත්වයේ උඩරට තේ, සලාද කොළ, මල් වගාව සහ එළවළු",
        "yala_crops_ta": "உயர்தர தேயிலை, சாலட் இலைகள், மலர் சாகுபடி மற்றும் காய்கறிகள்",
        "yala_crops_en": "High-Grown Ceylon Tea, Lettuce, Floriculture, and Vegetables",
    },
    "Matale": {
        "zone_si": "මැද රට අතරමැදි හා වියළි කලාපය (IM / DL)",
        "zone_ta": "இடைநிலை மற்றும் உலர் வலயம் (IM / DL)",
        "zone_en": "Intermediate & Dry Zone (IM / DL)",
        "soil_si": "රතු-දුඹුරු ලැටොසොලික් සහ රතු-කහ පොඩ්සොලික් පස",
        "soil_ta": "செம்பழுப்பு லேடோசோலிக் மற்றும் பொட்சோலிக் மண்",
        "soil_en": "Reddish Brown Latosolic & Red-Yellow Podzolic",
        "maha_crops_si": "කුළුබඩු (ගම්මිරිස්, කරදමුංගු), ලොකු ලූනු, බඩඉරිඟු සහ කොකෝවා",
        "maha_crops_ta": "மசாலா பயிர்கள் (மிளகு, ஏலக்காய்), பெரிய வெங்காயம், மக்காச்சோளம்",
        "maha_crops_en": "Spices (Pepper, Cardamom), Big Onion, Maize, and Cocoa",
        "yala_crops_si": "ලොකු ලූනු බීජ නිෂ්පාදනය, එළවළු සහ පලතුරු",
        "yala_crops_ta": "வெங்காய விதை உற்பத்தி, காய்கறிகள் மற்றும் பழங்கள்",
        "yala_crops_en": "Big Onion Seed Production, Vegetables, and Fruits",
    },
    "Jaffna": {
        "zone_si": "උතුරු අර්ධද්වීප වියළි කලාපය (DL3)",
        "zone_ta": "யாழ் குடாநாட்டு உலர் வலயம் (DL3)",
        "zone_en": "Northern Dry Zone (DL3)",
        "soil_si": "කැල්සික් රතු-කහ ලැටොසොල් (හුණුගල් ආශ්‍රිත) සහ රෙගොසොල් පස",
        "soil_ta": "சுண்ணாம்பு செம்மஞ்சள் மண் மற்றும் மணல் மண்",
        "soil_en": "Calcic Red-Yellow Latosols & Sandy Regosols",
        "maha_crops_si": "රතු ලූනු, මිරිස්, දුම්කොළ, බතල, මිදි සහ කෙසෙල්",
        "maha_crops_ta": "சின்ன வெங்காயம், மிளகாய், புகையிலை, வத்தாளங்கிழங்கு, திராட்சை, வாழை",
        "maha_crops_en": "Red Onion, Chilli, Tobacco, Sweet Potato, Grapes, and Banana",
        "yala_crops_si": "මිදි (Grapes), කොමඩු, මාළු මිරිස්, රටකජු (බිංදු ජල සම්පාදනයෙන්)",
        "yala_crops_ta": "திராட்சை, தர்பூசணி, குடைமிளகாய், நிலக்கடலை (சொட்டு நீர் பாசனம்)",
        "yala_crops_en": "Grapes, Watermelon, Bell Pepper, Groundnut (via Drip Irrigation)",
    },
    "Kilinochchi": {
        "zone_si": "වියළි කලාපය (DL3)",
        "zone_ta": "உலர் வலயம் (DL3)",
        "zone_en": "Dry Zone (DL3)",
        "soil_si": "රතු-කහ ලැටොසොල් සහ පහත් බිම් මැටි පස",
        "soil_ta": "செம்மஞ்சள் லேடோசோல் மற்றும் களிமண்",
        "soil_en": "Red-Yellow Latosols & Alluvial Clay",
        "maha_crops_si": "වී, බඩඉරිඟු, උඳු, මිරිස් සහ රටකජු",
        "maha_crops_ta": "நெல், மக்காச்சோளம், உளுந்து, மிளகாய் மற்றும் நிலக்கடலை",
        "maha_crops_en": "Paddy, Maize, Blackgram, Chilli, and Groundnut",
        "yala_crops_si": "මුං ඇට, කොමඩු, තල සහ කරවිල",
        "yala_crops_ta": "பாசிப்பயறு, தர்பூசணி, எள் மற்றும் பாகற்காய்",
        "yala_crops_en": "Mungbean, Watermelon, Sesame, and Bitter Gourd",
    },
    "Mannar": {
        "zone_si": "ශුෂ්ක වියළි කලාපය (DL4)",
        "zone_ta": "மிக உலர் வலயம் (DL4)",
        "zone_en": "Arid Dry Zone (DL4)",
        "soil_si": "ග්ලැසියල් හා වැලි සහිත රෙගොසොල් සහ ලවණ පස",
        "soil_ta": "மணல் மண் மற்றும் உவர்ப்பு மண்",
        "soil_en": "Sandy Regosols & Saline Alluvium",
        "maha_crops_si": "වී (මෝඩයි කුඹුරු), ලොකු ලූනු, රටකජු සහ කොමඩු",
        "maha_crops_ta": "நெல், பெரிய வெங்காயம், நிலக்கடலை மற்றும் தர்பூசணி",
        "maha_crops_en": "Paddy, Big Onion, Groundnut, and Watermelon",
        "yala_crops_si": "තල, උඳු සහ කට්ටු මාළු/කරවල සඳහා ලුණු දරාගත හැකි බෝග",
        "yala_crops_ta": "எள், உளுந்து மற்றும் வறட்சியை தாங்கும் பயிர்கள்",
        "yala_crops_en": "Sesame, Blackgram, and Drought-Tolerant Legumes",
    },
    "Vavuniya": {
        "zone_si": "වියළි කලාපය (DL1)",
        "zone_ta": "உலர் வலயம் (DL1)",
        "zone_en": "Dry Zone (DL1)",
        "soil_si": "රතු-දුඹුරු පස (RBE) සහ පහත් බිම් හියුමික් පස",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் தாழ் நில மட்கிய மண்",
        "soil_en": "Reddish Brown Earths & Low Humic Gley",
        "maha_crops_si": "වී, බඩඉරිඟු, කඩල, උඳු සහ මිරිස්",
        "maha_crops_ta": "நெல், மக்காச்சோளம், கொண்டைக்கடலை, உளுந்து மற்றும் மிளகாய்",
        "maha_crops_en": "Paddy, Maize, Chickpea, Blackgram, and Chilli",
        "yala_crops_si": "මුං ඇට, රටකජු, තල සහ කොමඩු",
        "yala_crops_ta": "பாசிப்பயறு, நிலக்கடலை, எள் மற்றும் தர்பூசணி",
        "yala_crops_en": "Mungbean, Groundnut, Sesame, and Watermelon",
    },
    "Mullaitivu": {
        "zone_si": "වියළි කලාපය (DL3 / DL1)",
        "zone_ta": "உலர் வலயம் (DL3 / DL1)",
        "zone_en": "Dry Zone (DL3 / DL1)",
        "soil_si": "වෙරළබඩ රෙගොසොල් සහ රතු-කහ ලැටොසොල්",
        "soil_ta": "கடற்கரை மணல் மண் மற்றும் செம்மஞ்சள் லேடோசோல்",
        "soil_en": "Coastal Regosols & Red-Yellow Latosols",
        "maha_crops_si": "වී, රටකජු, බඩඉරිඟු, මඤ්ඤොක්කා සහ කජු",
        "maha_crops_ta": "நெல், நிலக்கடலை, சோளம், மரவள்ளி மற்றும் முந்திரி",
        "maha_crops_en": "Paddy, Groundnut, Maize, Cassava, and Cashew",
        "yala_crops_si": "මුං ඇට, කොමඩු සහ තල",
        "yala_crops_ta": "பாசிப்பயறு, தர்பூசணி மற்றும் எள்",
        "yala_crops_en": "Mungbean, Watermelon, and Sesame",
    },
    "Batticaloa": {
        "zone_si": "නැගෙනහිර වියළි කලාපය (DL2)",
        "zone_ta": "கிழக்கு உலர் வலயம் (DL2)",
        "zone_en": "Eastern Dry Zone (DL2)",
        "soil_si": "වැලි සහිත රෙගොසොල් සහ ඇලූවියල් (ගංවතුර නිම්න) පස",
        "soil_ta": "மணல் மண் மற்றும் வண்டல் மண்",
        "soil_en": "Sandy Regosols & Alluvial soils",
        "maha_crops_si": "වී, රටකජු, මඤ්ඤොක්කා, කජු සහ එළවළු",
        "maha_crops_ta": "நெல், நிலக்கடலை, மரவள்ளி, முந்திரி மற்றும் காய்கறிகள்",
        "maha_crops_en": "Paddy, Groundnut, Cassava, Cashew, and Vegetables",
        "yala_crops_si": "රටකජු, කොමඩු, තල, මිරිස් සහ බඩඉරිඟු",
        "yala_crops_ta": "நிலக்கடலை, தர்பூசணி, எள், மிளகாய் மற்றும் சோளம்",
        "yala_crops_en": "Groundnut, Watermelon, Sesame, Chilli, and Maize",
    },
    "Ampara": {
        "zone_si": "දිගාමඩුල්ල වියළි කලාපය (DL2)",
        "zone_ta": "திகாமடுல்ல உலர் வலயம் (DL2)",
        "zone_en": "Eastern Dry Zone (DL2)",
        "soil_si": "සාරවත් ඇලූවියල් මැටි පස සහ රතු-දුඹුරු පස",
        "soil_ta": "வண்டல் களிமண் மற்றும் செம்பழுப்பு மண்",
        "soil_en": "Fertile Alluvial Clay & Reddish Brown Earths",
        "maha_crops_si": "මහා පරිමාණ වී වගාව, බඩඉරිඟු, උක් සහ රටකජු",
        "maha_crops_ta": "பெரிய அளவிலான நெல் விவசாயம், சோளம், கரும்பு, நிலக்கடலை",
        "maha_crops_en": "Large-Scale Paddy, Maize, Sugarcane, and Groundnut",
        "yala_crops_si": "වී (වාරිමාර්ග යටතේ), මුං ඇට, සෝයා සහ කොමඩු",
        "yala_crops_ta": "நீர்ப்பாசன நெல், பாசிப்பயறு, சோயா மற்றும் தர்பூசணி",
        "yala_crops_en": "Irrigated Paddy, Mungbean, Soybean, and Watermelon",
    },
    "Trincomalee": {
        "zone_si": "නැගෙනහිර වියළි කලාපය (DL1 / DL2)",
        "zone_ta": "கிழக்கு உலர் வலயம் (DL1 / DL2)",
        "zone_en": "Eastern Dry Zone (DL1 / DL2)",
        "soil_si": "රතු-දුඹුරු පස, ඇලූවියල් පස සහ වෙරළබඩ වැලි පස",
        "soil_ta": "செம்பழுப்பு மண், வண்டல் மண் மற்றும் கடற்கரை மணல்",
        "soil_en": "Reddish Brown Earths, Alluvial & Beach Sand",
        "maha_crops_si": "වී, බඩඉරිඟු, උඳු, මිරිස් සහ රටකජු",
        "maha_crops_ta": "நெல், சோளம், உளுந்து, மிளகாய் மற்றும் நிலக்கடலை",
        "maha_crops_en": "Paddy, Maize, Blackgram, Chilli, and Groundnut",
        "yala_crops_si": "ලොකු ලූනු, කොමඩු, තල සහ මුං ඇට",
        "yala_crops_ta": "பெரிய வெங்காயம், தர்பூசணி, எள் மற்றும் பாசிப்பயறு",
        "yala_crops_en": "Big Onion, Watermelon, Sesame, and Mungbean",
    },
    "Puttalam": {
        "zone_si": "වයඹ වියළි හා ශුෂ්ක කලාපය (DL3 / DL1)",
        "zone_ta": "வடமேற்கு உலர் வலயம் (DL3 / DL1)",
        "zone_en": "North-Western Dry Zone (DL3 / DL1)",
        "soil_si": "රතු-කහ ලැටොසොල්, රෙගොසොල් සහ හුණුගල් පස",
        "soil_ta": "செம்மஞ்சள் லேடோசோல் மற்றும் மணல் மண்",
        "soil_en": "Red-Yellow Latosols, Regosols & Calcic Soils",
        "maha_crops_si": "පොල්, කජු, වී, රතු ලූනු සහ මඤ්ඤොක්කා",
        "maha_crops_ta": "தேங்காய், முந்திரி, நெல், சின்ன வெங்காயம், மரவள்ளி",
        "maha_crops_en": "Coconut, Cashew, Paddy, Red Onion, and Cassava",
        "yala_crops_si": "කොමඩු, තල, රටකජු සහ බිංදු ජල සම්පාදන එළවළු",
        "yala_crops_ta": "தர்பூசணி, எள், நிலக்கடலை மற்றும் சொட்டு நீர் காய்கறிகள்",
        "yala_crops_en": "Watermelon, Sesame, Groundnut, and Drip-Irrigated Veg",
    },
    "Badulla": {
        "zone_si": "ඌව අතරමැදි කලාපය (IM1 / IU)",
        "zone_ta": "ஊவா இடைநிலை வலயம் (IM1 / IU)",
        "zone_en": "Uva Intermediate Zone (IM1 / IU)",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ රතු-දුඹුරු ලැටොසොලික් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் செம்பழுப்பு மண்",
        "soil_en": "Red-Yellow Podzolic & Reddish Brown Latosolic",
        "maha_crops_si": "උඩරට එළවළු (බෝංචි, තක්කාලි, ගෝවා), තේ, පැඟිරි සහ කෝපි",
        "maha_crops_ta": "காய்கறிகள் (பீன்ஸ், தக்காளி, முட்டைக்கோஸ்), தேயிலை, காப்பி",
        "maha_crops_en": "Up-Country Vegetables (Beans, Tomato, Cabbage), Tea, Coffee",
        "yala_crops_si": "අර්තාපල්, බඩඉරිඟු, සලාද එළවළු සහ පළතුරු",
        "yala_crops_ta": "உருளைக்கிழங்கு, சோளம் மற்றும் பழங்கள்",
        "yala_crops_en": "Potatoes, Sweet Corn, Salad Crops, and Fruits",
    },
    "Monaragala": {
        "zone_si": "අතරමැදි හා වියළි කලාපය (IL1c / DL1b)",
        "zone_ta": "இடைநிலை மற்றும் உலர் வலயம் (IL1c / DL1b)",
        "zone_en": "Intermediate & Dry Zone (IL1c / DL1b)",
        "soil_si": "රතු-දුඹුරු පස (RBE) සහ නොකැල්සික් දුඹුරු පස",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் சுண்ணமற்ற பழுப்பு மண்",
        "soil_en": "Reddish Brown Earths & Noncalcic Brown soils",
        "maha_crops_si": "උක් (Sugarcane), රබර්, බඩඉරිඟු, කෙසෙල්, පැඟිරි සහ වී",
        "maha_crops_ta": "கரும்பு, ரப்பர், சோளம், வாழை, சிட்ரஸ் பழங்கள் மற்றும் நெல்",
        "maha_crops_en": "Sugarcane, Rubber, Maize, Banana, Citrus, and Paddy",
        "yala_crops_si": "තල, මුං ඇට, රටකජු, කොමඩු සහ දෙළුම්",
        "yala_crops_ta": "எள், பாசிப்பயறு, நிலக்கடலை, தர்பூசணி மற்றும் மாதுளை",
        "yala_crops_en": "Sesame, Mungbean, Groundnut, Watermelon, and Pomegranate",
    },
    "Ratnapura": {
        "zone_si": "පහත රට තෙත් කලාපය (WL1 / WL2)",
        "zone_ta": "தாழ் நில ஈர வலயம் (WL1 / WL2)",
        "zone_en": "Low-Country Wet Zone (WL1 / WL2)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස (බොරළු සහිත) සහ ඇලූවියල් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் வண்டல் மண்",
        "soil_en": "Red-Yellow Podzolic (Lateritic) & Alluvial soils",
        "maha_crops_si": "තේ, රබර්, කුරුඳු, කෙසෙල්, පැපොල් සහ පුවක්",
        "maha_crops_ta": "தேயிலை, ரப்பர், இலவங்கப்பட்டை, வாழை, பப்பாளி, பாக்கு",
        "maha_crops_en": "Low-Grown Tea, Rubber, Cinnamon, Banana, Papaya, and Arecanut",
        "yala_crops_si": "ගම්මිරිස්, කරාබුනැටි, අන්නාසි, රඹුටන් සහ එළවළු",
        "yala_crops_ta": "மிளகு, கிராம்பு, அன்னாசி, ரம்புட்டான் மற்றும் காய்கறிகள்",
        "yala_crops_en": "Pepper, Cloves, Pineapple, Rambutan, and Vegetables",
    },
    "Kegalle": {
        "zone_si": "පහත හා මැද රට තෙත් කලාපය (WL2 / WM3)",
        "zone_ta": "தாழ் மற்றும் மத்திய ஈர வலயம் (WL2 / WM3)",
        "zone_en": "Wet Zone (WL2 / WM3)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස (සාරවත් කාබනික ස්ථරයක් සහිත)",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மண் (வளமான கரிம அடுக்கு)",
        "soil_en": "Red-Yellow Podzolic with Organic Horizon",
        "maha_crops_si": "රබර්, තේ, කුළුබඩු (කුරුඳු, කරාබුනැටි, සාදික්කා), කෙසෙල්",
        "maha_crops_ta": "ரப்பர், தேயிலை, மசாலா பயிர்கள் (இலவங்கம், கிராம்பு), வாழை",
        "maha_crops_en": "Rubber, Tea, Minor Export Crops (Cinnamon, Clove, Nutmeg), Banana",
        "yala_crops_si": "පැපොල්, අන්නාසි, එළවළු, ඉඟුරු සහ කහ",
        "yala_crops_ta": "பப்பாளி, அன்னாசி, காய்கறிகள், இஞ்சி மற்றும் மஞ்சள்",
        "yala_crops_en": "Papaya, Pineapple, Ginger, Turmeric, and Vegetables",
    },
    "Colombo": {
        "zone_si": "පහත රට තෙත් කලාපය (WL1)",
        "zone_ta": "தாழ் நில ஈர வலயம் (WL1)",
        "zone_en": "Low-Country Wet Zone (WL1)",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ අර්ධ බොග්/වගුරු පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் சதுப்பு நில மண்",
        "soil_en": "Red-Yellow Podzolic & Bog/Half-Bog soils",
        "maha_crops_si": "නාගරික එළවළු, කොළ එළවළු (කංකුං, මුකුණුවැන්න), කෙසෙල් සහ බුලත්",
        "maha_crops_ta": "நகர்ப்புற காய்கறிகள், கீரை வகைகள், வாழை மற்றும் வெற்றிலை",
        "maha_crops_en": "Urban Horticulture, Leafy Greens, Banana, and Betel",
        "yala_crops_si": "හයිඩ්‍රොපොනික්ස්, පැපොල්, අන්නාසි සහ විසිතුරු මල්",
        "yala_crops_ta": "ஹைட்ரோபோனிக்ஸ், பப்பாளி, அன்னாசி மற்றும் மலர் சாகுபடி",
        "yala_crops_en": "Hydroponics, Papaya, Pineapple, and Floriculture",
    },
    "Gampaha": {
        "zone_si": "පහත රට තෙත් කලාපය (WL1)",
        "zone_ta": "தாழ் நில ஈர வலயம் (WL1)",
        "zone_en": "Low-Country Wet Zone (WL1)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ ලැටරයිට් (කබොක්) පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் சரளை மண்",
        "soil_en": "Red-Yellow Podzolic & Lateritic (Kabok) soils",
        "maha_crops_si": "පොල්, අන්නාසි, රඹුටන්, වී, කෙසෙල් සහ බුලත්",
        "maha_crops_ta": "தேங்காய், அன்னாசி, ரம்புட்டான், நெல், வாழை மற்றும் வெற்றிலை",
        "maha_crops_en": "Coconut, Pineapple, Rambutan, Paddy, Banana, and Betel",
        "yala_crops_si": "අන්නාසි, එළවළු, පළතුරු සහ මඤ්ඤොක්කා",
        "yala_crops_ta": "அன்னாசி, காய்கறிகள், பழங்கள் மற்றும் மரவள்ளி",
        "yala_crops_en": "Pineapple, Vegetables, Tropical Fruits, and Cassava",
    },
    "Kalutara": {
        "zone_si": "පහත රට අතිශය තෙත් කලාපය (WL1 / WL2)",
        "zone_ta": "அதி ஈர வலயம் (WL1 / WL2)",
        "zone_en": "Low-Country Super Wet Zone (WL1 / WL2)",
        "soil_si": "රතු-කහ පොඩ්සොලික් සහ බොග් (Bog) පස්",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் சதுப்பு மண்",
        "soil_en": "Red-Yellow Podzolic & Bog soils",
        "maha_crops_si": "රබර්, තේ, කුරුඳු, කෙසෙල්, පැපොල් සහ වී",
        "maha_crops_ta": "ரப்பர், தேயிலை, இலவங்கப்பட்டை, வாழை, பப்பாளி மற்றும் நெல்",
        "maha_crops_en": "Rubber, Low-Grown Tea, Cinnamon, Banana, Papaya, and Paddy",
        "yala_crops_si": "කුරුඳු, පළතුරු, මඤ්ඤොක්කා සහ කොළ එළවළු",
        "yala_crops_ta": "இலவங்கப்பட்டை, பழங்கள், மரவள்ளி மற்றும் கீரைகள்",
        "yala_crops_en": "Cinnamon, Perennial Fruits, Cassava, and Leafy Greens",
    },
    "Galle": {
        "zone_si": "දකුණු තෙත් කලාපය (WL1 / WL4)",
        "zone_ta": "தெற்கு ஈர வலயம் (WL1 / WL4)",
        "zone_en": "Southern Wet Zone (WL1 / WL4)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ වෙරළබඩ ඇලූවියල් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் வண்டல் மண்",
        "soil_en": "Red-Yellow Podzolic & Coastal Alluvial soils",
        "maha_crops_si": "කුරුඳු (Cinnamon - ප්‍රමුඛ අපනයන බෝගය), තේ, පොල්, රබර් සහ වී",
        "maha_crops_ta": "இலவங்கப்பட்டை (முக்கிய ஏற்றுமதி), தேயிலை, தேங்காய், ரப்பர், நெல்",
        "maha_crops_en": "Ceylon Cinnamon (Top Export), Low Tea, Coconut, Rubber, Paddy",
        "yala_crops_si": "කුරුඳු අස්වනු නෙළීම, පැපොල්, අන්නාසි සහ එළවළු",
        "yala_crops_ta": "இலவங்கப்பட்டை அறுவடை, பப்பாளி, அன்னாசி மற்றும் காய்கறிகள்",
        "yala_crops_en": "Cinnamon Harvesting, Papaya, Pineapple, and Tropical Veg",
    },
    "Matara": {
        "zone_si": "දකුණු තෙත් හා අතරමැදි කලාපය (WL / IL)",
        "zone_ta": "தெற்கு ஈர மற்றும் இடைநிலை வலயம் (WL / IL)",
        "zone_en": "Southern Wet & Intermediate Zone (WL / IL)",
        "soil_si": "රතු-කහ පොඩ්සොලික් පස සහ ඇලූවියල් පස",
        "soil_ta": "செம்மஞ்சள் பொட்சோலிக் மற்றும் வண்டல் மண்",
        "soil_en": "Red-Yellow Podzolic & Alluvial soils",
        "maha_crops_si": "කුරුඳු, තේ, පොල්, පැටවුම් වී සහ එළවළු",
        "maha_crops_ta": "இலவங்கப்பட்டை, தேயிலை, தேங்காய், நெல் மற்றும் காய்கறிகள்",
        "maha_crops_en": "Cinnamon, Low Tea, Coconut, Paddy, and Vegetables",
        "yala_crops_si": "පොල් අතුරු බෝග, කෙසෙල්, පැපොල් සහ ඉඟුරු",
        "yala_crops_ta": "தேங்காய் இடைப்பயிர், வாழை, பப்பாளி மற்றும் இஞ்சி",
        "yala_crops_en": "Coconut Intercropping, Banana, Papaya, and Ginger",
    },
    "Hambantota": {
        "zone_si": "දකුණු වියළි හා ශුෂ්ක කලාපය (DL5 / DL1)",
        "zone_ta": "தெற்கு உலர் மற்றும் மிக உலர் வலயம் (DL5 / DL1)",
        "zone_en": "Southern Dry & Arid Zone (DL5 / DL1)",
        "soil_si": "රතු-දුඹුරු පස (RBE), ග්‍රැනියුලර් නොකැල්සික් දුඹුරු පස සහ ලවණ පස",
        "soil_ta": "செம்பழுப்பு மண் மற்றும் உவர்ப்பு மண்",
        "soil_en": "Reddish Brown Earths & Saline Alluvium",
        "maha_crops_si": "වී (වලව ව්‍යාපෘතිය), බඩඉරිඟු, කෙසෙල්, කොමඩු, රටකජු සහ මිරිස්",
        "maha_crops_ta": "நெல், மக்காச்சோளம், வாழை, தர்பூசணி, நிலக்கடலை மற்றும் மிளகாய்",
        "maha_crops_en": "Paddy (Walawa Scheme), Maize, Banana, Watermelon, Peanut, Chilli",
        "yala_crops_si": "කොමඩු, තල, මුං ඇට, දෙළුම්, මිදි සහ රටකජු",
        "yala_crops_ta": "தர்பூசணி, எள், பாசிப்பயறு, மாதுளை, திராட்சை மற்றும் நிலக்கடலை",
        "yala_crops_en": "Watermelon, Sesame, Mungbean, Pomegranate, Grapes, Groundnut",
    },
}

CROP_DICTIONARY: Dict[str, Dict[str, str]] = {
    "rice": {"en": "Rice (Paddy)", "si": "වී ගොවිතැන", "ta": "நெல் / அரிசி"},
    "maize": {"en": "Maize (Corn)", "si": "බඩඉරිඟු", "ta": "மக்காச்சோளம்"},
    "chickpea": {"en": "Chickpea", "si": "කඩල", "ta": "கொண்டைக்கடலை"},
    "kidneybeans": {"en": "Kidney Beans", "si": "රාජ්මා බෝංචි", "ta": "பீன்ஸ்"},
    "pigeonpeas": {"en": "Pigeon Peas", "si": "තෝර පරිප්පු", "ta": "துவரை"},
    "mothbeans": {"en": "Moth Beans", "si": "මෑ කරල්", "ta": "தட்டாம்பயறு"},
    "mungbean": {"en": "Mung Bean", "si": "මුං ඇට", "ta": "பாசிப்பயறு"},
    "blackgram": {"en": "Black Gram (Undu)", "si": "උඳු", "ta": "உளுந்து"},
    "lentil": {"en": "Lentil", "si": "මසූර් පරිප්පු", "ta": "பருப்பு"},
    "pomegranate": {"en": "Pomegranate", "si": "දෙළුම්", "ta": "மாதுளை"},
    "banana": {"en": "Banana", "si": "කෙසෙල්", "ta": "வாழை"},
    "mango": {"en": "Mango", "si": "අඹ", "ta": "மாம்பழம்"},
    "grapes": {"en": "Grapes", "si": "මිදි", "ta": "திராட்சை"},
    "watermelon": {"en": "Watermelon", "si": "කොමඩු", "ta": "தர்பூசணி"},
    "muskmelon": {"en": "Muskmelon", "si": "කැකිරි / කැන්ටලූප්", "ta": "முலாம் பழம்"},
    "apple": {"en": "Apple (Up-Country)", "si": "ඇපල්", "ta": "ஆப்பிள்"},
    "orange": {"en": "Orange / Citrus", "si": "පැඟිරි / දොඩම්", "ta": "ஆரஞ்சு"},
    "papaya": {"en": "Papaya", "si": "පැපොල්", "ta": "பப்பாளி"},
    "coconut": {"en": "Coconut", "si": "පොල්", "ta": "தேங்காய்"},
    "cotton": {"en": "Cotton", "si": "කපු", "ta": "பருத்தி"},
    "jute": {"en": "Jute / Fiber", "si": "සණ / කෙඳි", "ta": "சணல்"},
    "coffee": {"en": "Coffee", "si": "කෝපි", "ta": "காப்பி"},
}


DISTRICT_ALIASES: Dict[str, str] = {
    # Polonnaruwa
    "polonnaruwa": "Polonnaruwa", "පොළොන්නරු": "Polonnaruwa", "පොලොන්නරු": "Polonnaruwa", "பொலன்னறுவை": "Polonnaruwa",
    # Anuradhapura
    "anuradhapura": "Anuradhapura", "අනුරාධපුර": "Anuradhapura", "அனுராதபுரம்": "Anuradhapura",
    # Kurunegala
    "kurunegala": "Kurunegala", "කුරුණෑගල": "Kurunegala", "குருநாகல்": "Kurunegala",
    # Kandy
    "kandy": "Kandy", "මහනුවර": "Kandy", "නුවර": "Kandy", "கண்டி": "Kandy",
    # Nuwara Eliya
    "nuwara eliya": "Nuwara Eliya", "නුවරඑළිය": "Nuwara Eliya", "නුවර එළිය": "Nuwara Eliya", "நுவரெலியா": "Nuwara Eliya",
    # Matale
    "matale": "Matale", "මාතලේ": "Matale", "மாத்தளை": "Matale",
    # Jaffna
    "jaffna": "Jaffna", "යාපනය": "Jaffna", "යාපනේ": "Jaffna", "யாழ்ப்பாணம்": "Jaffna", "யாழ்ப்பாண": "Jaffna",
    # Kilinochchi
    "kilinochchi": "Kilinochchi", "කිලිනොච්චි": "Kilinochchi", "கிளிநொச்சி": "Kilinochchi",
    # Mannar
    "mannar": "Mannar", "මන්නාරම": "Mannar", "මන්නාරම්": "Mannar", "மன்னார்": "Mannar",
    # Vavuniya
    "vavuniya": "Vavuniya", "වවුනියාව": "Vavuniya", "வவுனியா": "Vavuniya",
    # Mullaitivu
    "mullaitivu": "Mullaitivu", "මුලතිව්": "Mullaitivu", "முல்லைத்தீவு": "Mullaitivu",
    # Batticaloa
    "batticaloa": "Batticaloa", "මඩකලපුව": "Batticaloa", "මඩකලපු": "Batticaloa", "மட்டக்களப்பு": "Batticaloa",
    # Ampara
    "ampara": "Ampara", "අම්පාර": "Ampara", "අම්පාරේ": "Ampara", "அம்பாறை": "Ampara",
    # Trincomalee
    "trincomalee": "Trincomalee", "ත්‍රිකුණාමලය": "Trincomalee", "ත්‍රිකුණාමල": "Trincomalee", "திருகோணமலை": "Trincomalee",
    # Puttalam
    "puttalam": "Puttalam", "පුත්තලම": "Puttalam", "පුත්තලම්": "Puttalam", "புத்தளம்": "Puttalam",
    # Badulla
    "badulla": "Badulla", "බදුල්ල": "Badulla", "බදුල්ලේ": "Badulla", "பதுளை": "Badulla",
    # Monaragala
    "monaragala": "Monaragala", "මොනරාගල": "Monaragala", "மொணராகலை": "Monaragala",
    # Ratnapura
    "ratnapura": "Ratnapura", "රත්නපුර": "Ratnapura", "இரத்தினபுரி": "Ratnapura",
    # Kegalle
    "kegalle": "Kegalle", "කෑගල්ල": "Kegalle", "கேகாலை": "Kegalle",
    # Colombo
    "colombo": "Colombo", "කොළඹ": "Colombo", "கொழும்பு": "Colombo",
    # Gampaha
    "gampaha": "Gampaha", "ගම්පහ": "Gampaha", "கம்பஹா": "Gampaha",
    # Kalutara
    "kalutara": "Kalutara", "කළුතර": "Kalutara", "களுத்துறை": "Kalutara",
    # Galle
    "galle": "Galle", "ගාල්ල": "Galle", "ගාල්ලේ": "Galle", "காலி": "Galle",
    # Matara
    "matara": "Matara", "මාතර": "Matara", "மாத்தறை": "Matara",
    # Hambantota
    "hambantota": "Hambantota", "හම්බන්තොට": "Hambantota", "அம்பாந்தோட்டை": "Hambantota",
}

def detect_district_from_text(text: str) -> Optional[str]:
    text_lower = text.lower()
    for alias, dist_name in DISTRICT_ALIASES.items():
        if alias in text_lower or alias in text:
            return dist_name
    return None

def get_district_info(district_name: str) -> Optional[Dict[str, Any]]:
    d_clean = district_name.strip().title()
    for d, info in DISTRICT_KNOWLEDGE.items():
        if d.lower() == d_clean.lower():
            return info
    return None



def get_soil_remediation_advice(ph: Optional[float], n: Optional[float], p: Optional[float], k: Optional[float], lang: str = "en") -> str:
    tips = []
    
    # pH remediation
    if ph is not None:
        if ph < 5.2:
            if lang == "si":
                tips.append(f"පසේ pH අගය {ph} ක් වන බැවින් පස අධික ලෙස ආම්ලික වේ (Acidic Soil). අක්කරයකට ඩොලමයිට් (Dolomite) හෝ කෘෂිකාර්මික හුණු කිලෝග්‍රෑම් 300-500ක් යෙදීමෙන් pH අගය 6.0 - 6.5 මට්ටමට ඔසවා ගත හැක.")
            elif lang == "ta":
                tips.append(f"மண்ணின் pH அளவு {ph} ஆக இருப்பதால் நிலம் அதிக அமிலத்தன்மை கொண்டது. ஏக்கருக்கு 300-500 கிலோ டோலமைட் (Dolomite) அல்லது சுண்ணாம்பு இட்டு pH அளவை 6.0 - 6.5 வரை சீராக்கவும்.")
            else:
                tips.append(f"Soil pH is {ph} (strongly acidic). Apply Agricultural Dolomite or slaked lime at 300-500 kg/acre to raise the pH into the optimal 6.0 - 6.5 agronomic range.")
        elif ph > 7.5:
            if lang == "si":
                tips.append(f"පසේ pH අගය {ph} ක් වන බැවින් පස ක්ෂාරීය/ලවණ සහිතය (Alkaline Soil). කාබනික කොම්පෝස්ට් පොහොර, ගොම පොහොර සහ අවශ්‍ය නම් ජිප්සම් (Gypsum) යොදා පාංශු ව්‍යුහය සමතුලිත කරන්න.")
            elif lang == "ta":
                tips.append(f"மண்ணின் pH அளவு {ph} ஆக இருப்பதால் நிலம் காரத்தன்மை/உவர்ப்பானது. மட்கிய உரம், ஜிப்சம் (Gypsum) இட்டு மண்ணின் தன்மையை சமப்படுத்தவும்.")
            else:
                tips.append(f"Soil pH is {ph} (alkaline/saline tendency). Incorporate organic compost, green manure, and agricultural gypsum to buffer alkalinity and improve cation exchange.")

    # Nutrient balance tips
    if n is not None and n < 40:
        if lang == "si":
            tips.append("නයිට්‍රජන් (N) පෝෂක මට්ටම අඩු බැවින් කොළ කහවීම වැළැක්වීමට යූරියා (Urea) හෝ ග්ලිරිසීඩියා කොළ පොහොර එක් කරන්න.")
        elif lang == "ta":
            tips.append("நைதரசன் (N) அளவு குறைவாக உள்ளது. யூரியா உரம் அல்லது இயற்கை பசுந்தாள் உரம் இடுங்கள்.")
        else:
            tips.append("Nitrogen (N) is deficient; supplement with basal Urea or nitrogen-fixing green manuring (Gliricidia).")

    if p is not None and p < 25:
        if lang == "si":
            tips.append("පොස්පරස් (P) අඩු බැවින් ශක්තිමත් මුල් වර්ධනය සඳහා ත්‍රිත්ව සුපර් පොස්පේට් (TSP) හෝ රොක් පොස්පේට් යොදන්න.")
        elif lang == "ta":
            tips.append("பொசுபரசு (P) குறைவாக உள்ளது. வேர் வளர்ச்சிக்கு TSP உரம் இடுங்கள்.")
        else:
            tips.append("Phosphorus (P) is low; apply Triple Super Phosphate (TSP) or Eppawala Rock Phosphate (ERP) for root establishment.")

    if k is not None and k < 30:
        if lang == "si":
            tips.append("පොටෑසියම් (K) මට්ටම අඩු බැවින් පළතුරු සහ බීජ මේරීම වැඩි කිරීමට මියුරියේට් ඔෆ් පොටෑෂ් (MOP) එක් කරන්න.")
        elif lang == "ta":
            tips.append("பொட்டாசியம் (K) குறைவாக உள்ளது. சிறந்த விளைச்சலுக்கு MOP உரம் இடுங்கள்.")
        else:
            tips.append("Potassium (K) is below target; incorporate Muriate of Potash (MOP) for robust grain filling and disease resilience.")

    if not tips:
        if lang == "si":
            return "පසේ N-P-K පෝෂක සහ pH අගය ඉතා යහපත් සමතුලිත මට්ටමක පවතී. සාමාන්‍ය නිර්දේශිත මට්ටමින් කාබනික පොහොර යෙදීම ප්‍රමාණවත්ය."
        elif lang == "ta":
            return "மண்ணின் N-P-K மற்றும் pH அளவுகள் சமநிலையில் உள்ளன. வழக்கமான இயற்கை உரங்களை இட்டு பராமரிக்கலாம்."
        else:
            return "Soil nutrient concentrations and pH are well-balanced. Maintain periodic organic compost application to sustain soil microbial health."

    return " \n• ".join(tips)


def get_district_advice(district: str, month_input: Any = None, lang: str = "en", turn: int = 0) -> str:
    data = get_district_info(district)
    if not data:
        data = DISTRICT_KNOWLEDGE.get("Polonnaruwa", {})
        district = "Polonnaruwa"

    is_maha = True
    month_name_si = "සැප්තැම්බර්"
    month_name_ta = "செப்டம்பர்"
    month_name_en = "September"

    if isinstance(month_input, (list, tuple)) and len(month_input) >= 3:
        month_name_en, month_name_si, month_name_ta = month_input[:3]
        if str(month_name_en).lower() in ["may", "june", "july", "august", "april"]:
            is_maha = False
    elif isinstance(month_input, str):
        m_lower = month_input.lower()
        month_map = {
            "january": ("January", "ජනවාරි", "ஜனவரி", True),
            "february": ("February", "පෙබරවාරි", "பிப்ரவரி", True),
            "march": ("March", "මාර්තු", "மார்ச்", False),
            "april": ("April", "අප්‍රේල්", "ஏப்ரல்", False),
            "may": ("May", "මැයි", "மே", False),
            "june": ("June", "ජූනි", "ஜூன்", False),
            "july": ("July", "ජූලි", "ஜூலை", False),
            "august": ("August", "අගෝස්තු", "ஆகஸ்ட்", False),
            "september": ("September", "සැප්තැම්බර්", "செப்டம்பர்", True),
            "october": ("October", "ඔක්තෝබර්", "அக்டோபர்", True),
            "november": ("November", "නොවැම්බර්", "நவம்பர்", True),
            "december": ("December", "දෙසැම්බර්", "டிசம்பர்", True),
        }
        for m_k, (en, si, ta, maha) in month_map.items():
            if m_k in m_lower:
                month_name_en, month_name_si, month_name_ta = en, si, ta
                is_maha = maha
                break

    season_name_si = "මහ කන්නය (ඊසානදිග මෝසම)" if is_maha else "යල කන්නය (අඩු වර්ෂාපතන වියළි කාලය)"
    season_name_ta = "பெரும்போகம் (வடகிழக்கு பருவமழை)" if is_maha else "சிறுபோகம் (குறைந்த மழைக்காலம்)"
    season_name_en = "Maha Season (Northeast Monsoon)" if is_maha else "Yala Season (Dry Period / Inter-monsoon)"

    crops_si = data["maha_crops_si"] if is_maha else data["yala_crops_si"]
    crops_ta = data["maha_crops_ta"] if is_maha else data["yala_crops_ta"]
    crops_en = data["maha_crops_en"] if is_maha else data["yala_crops_en"]

    style = turn % 8

    if lang == "si":
        if style == 0:
            return (
                f"{district} දිස්ත්‍රික්කය - කලාපීය කෘෂිකාර්මික වාර්තාව ({data['zone_si']})\n\n"
                f"කාලගුණික පසුබිම ({month_name_si}): {season_name_si} අනුව පවතින කාලගුණික සහ ජල තත්ත්වයන් සැලකිල්ලට ගෙන ඇත.\n"
                f"ප්‍රධාන පස: {data['soil_si']}\n"
                f"නිර්දේශිත බෝග: {crops_si}\n\n"
                f"ක්ෂේත්‍ර උපදෙස්: බිම් සැකසීමේදී හොඳින් දිරූ කොම්පෝස්ට් පසට එකතු කරන්න. වැසි කාලයේදී ජලය එකතැන නොරැඳෙන සේ කාණු පද්ධති සකස් කරන්න."
            )
        elif style == 1:
            return (
                f"{district} ප්‍රදේශයේ වගා මාර්ගෝපදේශය ({data['zone_si']})\n\n"
                f"පවතින කන්නය: {month_name_si} මාසය තුළ {season_name_si} ක්‍රියාත්මක වේ.\n"
                f"පාංශු තත්ත්වය: {data['soil_si']} මෙම කලාපයේ බහුලව පවතී.\n"
                f"වඩාත්ම ඵලදායී බෝග තේරීම: {crops_si}\n\n"
                f"කළමනාකරණ පියවර: මුල් කාලයේ පාංශු තෙතමනය රැක ගැනීමට කාබනික වසුන් යොදන්න. නිර්දේශිත පොහොර නියමිත වේලාවට යෙදීමෙන් උපරිම අස්වැන්නක් ලබාගත හැක."
            )
        elif style == 2:
            return (
                f"{district} කෘෂි පාරිසරික තක්සේරුව ({data['zone_si']})\n\n"
                f"දේශගුණික සන්දර්භය: {month_name_si} මාසයේදී {season_name_si} ආශ්‍රිත කාලගුණ රටා පවතී.\n"
                f"පාංශු කාණ්ඩය: {data['soil_si']}\n"
                f"ඉහළ අස්වැන්නක් සඳහා නිර්දේශිත බෝග: {crops_si}\n\n"
                f"විද්‍යාත්මක නිර්දේශය: පාංශු පරීක්ෂාවකට අනුව N, P, K පෝෂක තුලනය කර බීජ තවාන් හෝ සෘජු බීජ වැපිරීම සිදු කරන්න."
            )
        elif style == 3:
            return (
                f"{district} ක්ෂේත්‍ර බෝග සැලැස්ම සහ කන්න උපදෙස්:\n\n"
                f"කලාපීය වර්ගීකරණය: {data['zone_si']}\n"
                f"කාලගුණ කාල සටහන: {month_name_si} - {season_name_si}\n"
                f"භූමි පාංශු ලක්ෂණ: {data['soil_si']}\n"
                f"සුදුසුම බෝග වර්ග: {crops_si}\n\n"
                f"වගා උපක්‍රම: බීජ ප්‍රරෝහණය සඳහා පසේ තෙතමනය පරික්ෂා කර නියමිත පරතරය සහිතව රෝපණය කරන්න. කාබනික ද්‍රව්‍ය මගින් පසේ සාරවත් බව ආරක්ෂා වේ."
            )
        elif style == 4:
            return (
                f"{district} ගොවිජන සේවා කලාපීය බෝග නිර්දේශය ({season_name_si}):\n\n"
                f"{month_name_si} මාසය තුළ {data['zone_si']} හි වගා කළ හැකි ප්‍රමුඛතම බෝග:\n"
                f"{crops_si}\n\n"
                f"පාංශු තත්ත්වය: {data['soil_si']}\n"
                f"පෝෂක කළමනාකරණය: මුල් අදින අවධියේදී මූලික පොහොර යොදා සති 3-4 කින් නයිට්‍රජන් හා පොටෑසියම් අතිරේක යෙදුම් ලබාදෙන්න."
            )
        elif style == 5:
            return (
                f"{district} දිස්ත්‍රික්කයේ කෘෂිකාර්මික ශක්‍යතා වාර්තාව:\n\n"
                f"කෘෂි දේශගුණය: {data['zone_si']} | කන්නය: {season_name_si} ({month_name_si})\n"
                f"ස්වභාවික පස: {data['soil_si']}\n"
                f"අධික ඵලදාවක් දෙන බෝග: {crops_si}\n\n"
                f"පළිබෝධ සහ ජල පාලනය: වියළි කාලගුණයක් පවතී නම් බිංදු ජල සම්පාදනය යොදාගන්න. අධික වැසි කාලයේදී පාංශු සෝදාපාළුව වැළැක්වීමට ආවරණ බෝග වවන්න."
            )
        elif style == 6:
            return (
                f"{district} වගා දින දර්ශනය සහ කලාපීය උපදේශනය:\n\n"
                f"අදාළ කලාපය: {data['zone_si']}\n"
                f"දේශගුණික චක්‍රය: {season_name_si} ආශ්‍රිත {month_name_si} මාසය\n"
                f"පාංශු කාණ්ඩය: {data['soil_si']}\n"
                f"තෝරාගත යුතු බෝග: {crops_si}\n\n"
                f"මගපෙන්වීම: වගාබිම සකස් කිරීමේදී පස හොඳින් වාතාශ්‍රය ලැබෙන සේ බුරුල් කරන්න. රසායනික පොහොර පමණක් නොයොදා කොම්පෝස්ට් සමඟ සමබරව භාවිතා කරන්න."
            )
        else:
            return (
                f"{district} කෘෂිකාර්මික සංවර්ධන හා පාංශු උපදෙස් මාලාව:\n\n"
                f"කලාපය: {data['zone_si']}\n"
                f"කන්නය: {season_name_si} ({month_name_si})\n"
                f"පසේ ස්වභාවය: {data['soil_si']}\n"
                f"නිර්දේශිත බෝග වර්ග: {crops_si}\n\n"
                f"ප්‍රධාන පියවර: නියමිත කාලයට බීජ තවාන් පිහිටුවන්න. පාංශු pH අගය පරීක්ෂා කර ආම්ලික පස් සඳහා ඩොලමයිට් යෙදීමට වගබලා ගන්න."
            )
    elif lang == "ta":
        if style % 2 == 0:
            return (
                f"{district} மாவட்டம் - விவசாய வழிகாட்டல் ({data['zone_ta']})\n\n"
                f"பருவநிலை சூழல் ({month_name_ta}): {season_name_ta} காலத்தின் மழைப்பொழிவு மற்றும் நீர்வளத்திற்கு ஏற்ப திட்டமிடப்பட்டுள்ளது.\n"
                f"பிரதான மண் வகை: {data['soil_ta']}\n"
                f"பரிந்துரைக்கப்பட்ட பயிர்கள்: {crops_ta}\n\n"
                f"வயல் ஆலோசனை: நிலத்தை உழும்போது இயற்கை உரங்களை இடுங்கள். மழைக்காலங்களில் வடிகால் வசதியை முறையாக பராமரிக்கவும்."
            )
        else:
            return (
                f"{district} மாவட்ட விவசாய திட்டம் ({data['zone_ta']})\n\n"
                f"பருவம்: {month_name_ta} மாதத்தில் {season_name_ta} நிலவுகிறது.\n"
                f"மண் தன்மை: {data['soil_ta']}\n"
                f"உகந்த பயிர்கள்: {crops_ta}\n\n"
                f"பயிர் பாதுகாப்பு: போதுமான இயற்கை உரம் மற்றும் முறையான நீர்ப்பாசன முறையை பயன்படுத்தி அதிக விளைச்சல் பெறலாம்."
            )
    else:
        if style == 0:
            return (
                f"{district} District Agronomic Advisory ({data['zone_en']})\n\n"
                f"Seasonal Context ({month_name_en}): Operating under the {season_name_en} with characteristic rainfall and hydrological patterns.\n"
                f"Dominant Soil Series: {data['soil_en']}\n"
                f"Recommended High-Yield Crops: {crops_en}\n\n"
                f"Field Advisory: Incorporate well-decomposed organic manure prior to seeding. Ensure proper field bund preparation and drainage channels to prevent waterlogging during monsoon spells."
            )
        elif style == 1:
            return (
                f"{district} Cultivation Strategy & Regional Planning ({data['zone_en']})\n\n"
                f"Agro-Ecological Setting: {data['zone_en']} during {month_name_en} ({season_name_en}).\n"
                f"Soil Profile: {data['soil_en']}\n"
                f"Top Suited Crops: {crops_en}\n\n"
                f"Operational Guidance: Prioritize seedbed aeration and root zone moisture management. Apply balanced basal fertilization aligned with local Department of Agriculture guidelines."
            )
        elif style == 2:
            return (
                f"{district} Agricultural Assessment & Suitability Overview ({data['zone_en']})\n\n"
                f"Climate & Season: {season_name_en} during {month_name_en}.\n"
                f"Target Soil Classification: {data['soil_en']}\n"
                f"Crops with High Yield Potential: {crops_en}\n\n"
                f"Agronomic Summary: Soil structure supports the listed crops effectively. Ensure adequate drainage channels and maintain organic mulch to optimize water efficiency."
            )
        elif style == 3:
            return (
                f"{district} Regional Cropping Framework:\n\n"
                f"Agro-Zone: {data['zone_en']}\n"
                f"Seasonal Cycle: {month_name_en} ({season_name_en})\n"
                f"Identified Soil Type: {data['soil_en']}\n"
                f"Viable Cultivars: {crops_en}\n\n"
                f"Action Steps: Prepare raised beds for root vegetables and ensure timely basal N-P-K placement. Mulching is advised to suppress weeds and retain subsoil humidity."
            )
        elif style == 4:
            return (
                f"{district} Agronomic Action Dossier ({season_name_en}):\n\n"
                f"Target Region: {data['zone_en']}\n"
                f"Active Calendar: {month_name_en}\n"
                f"Soil Classification: {data['soil_en']}\n"
                f"Recommended Crops for High Profitability: {crops_en}\n\n"
                f"Nutrient Strategy: Supplement initial planting with enriched compost. Monitor soil pH and apply dolomite if acidity drops below 5.5."
            )
        elif style == 5:
            return (
                f"{district} Field Suitability & Seasonal Agronomic Guide:\n\n"
                f"Geographic Domain: {data['zone_en']}\n"
                f"Seasonal Window: {month_name_en} - {season_name_en}\n"
                f"Soil Series: {data['soil_en']}\n"
                f"Best Suited Plantings: {crops_en}\n\n"
                f"Water & Crop Care: Utilize micro-irrigation where available during dry spells. Implement contour bunding in sloping terrains to preserve topsoil nutrients."
            )
        elif style == 6:
            return (
                f"{district} District Agro-Intelligence Summary:\n\n"
                f"Climate Setting: {data['zone_en']} in {month_name_en} ({season_name_en})\n"
                f"Prevalent Soil Order: {data['soil_en']}\n"
                f"Recommended Cropping Palette: {crops_en}\n\n"
                f"Field Directives: Soil conditions are conducive to rapid emergence. Ensure certified seed usage and maintain integrated pest management practices from nursery stage onward."
            )
        else:
            return (
                f"{district} Agronomic Review & Cultivar Guidelines:\n\n"
                f"Agro-Ecological Classification: {data['zone_en']}\n"
                f"Seasonal Phase: {season_name_en} ({month_name_en})\n"
                f"Soil Matrix: {data['soil_en']}\n"
                f"High-Performing Crops: {crops_en}\n\n"
                f"Implementation Note: Maintain split potassium top-dressing during vegetative expansion. Ensure field runoff channels are clear to prevent standing water."
            )

