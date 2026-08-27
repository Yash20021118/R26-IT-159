# Detailed Crop Aftercare Guidance Library for Sri Lankan Agricultural Context

CROP_GUIDANCE_DATABASE = {
    "rice": {
        "name": "Rice (Paddy / වී)",
        "scientific_name": "Oryza sativa",
        "category": "Cereal Crop",
        "description": "Rice is the primary staple crop of Sri Lanka. Highly suitable for clay loam to heavy clay soils with high water retention capacity across both Maha and Yala seasons.",
        "optimal_conditions": {
            "soil_type": "Clay Loam / Heavy Clay / Alluvial",
            "ph_range": "5.5 - 6.5",
            "temp_range": "20°C - 35°C",
            "humidity_range": "70% - 90%",
            "rainfall_range": "1500mm - 2500mm"
        },
        "land_prep": [
            "Primary tillage: Deep plowing to 15-20 cm depth to incorporate stubble and weeds.",
            "Puddling & Leveling: Flood the field and puddle 2-3 times to create an impermeable hardpan for water retention.",
            "Apply well-decomposed organic manure or compost at 5-10 tons/ha during land preparation."
        ],
        "irrigation": [
            "Initial Stage (Transplanting to Tillering): Maintain 2-3 cm continuous shallow water layer.",
            "Active Tillering: Alternate wetting and drying (AWD) to stimulate root elongation and aeration.",
            "Flowering & Panicle Initiation: Critical stage - maintain 5 cm standing water layer.",
            "Grain Filling to Maturity: Drain field completely 10-14 days prior to harvest."
        ],
        "fertilizer_schedule": [
            "Basal Dressing: Apply full dose of Phosphorus (TSP/ERP) and 1/3 Nitrogen (Urea) + 1/3 Potassium (MOP) prior to final land leveling.",
            "Top Dressing 1 (14-21 days after planting): Apply 1/3 Nitrogen (Urea) to boost tillering.",
            "Top Dressing 2 (Panicle Initiation stage, ~42 days): Apply remaining 1/3 Nitrogen (Urea) + 2/3 Potassium (MOP)."
        ],
        "pest_disease_control": [
            "Paddy Stem Borer: Use light traps and release Trichogramma egg parasitoids. Apply chlorantraniliprole if threshold (>5% dead hearts) is exceeded.",
            "Brown Planthopper (BPH): Avoid excessive nitrogen. Maintain water drainage and apply neem seed kernel extract or imidacloprid.",
            "Rice Blast (Pyricularia oryzae): Avoid late nitrogen application. Spray Tricyclazole 75 WP (0.6g/L) at first symptom."
        ],
        "harvest_post_harvest": [
            "Harvesting: Cut crop when 80-85% of panicles turn straw-golden yellow.",
            "Threshing & Drying: Thresh immediately and dry paddy to 13-14% moisture content for storage.",
            "Storage: Store in airtight bags (Hermetic storage) or dry storehouses free from rodents and moisture."
        ]
    },
    "maize": {
        "name": "Maize (Corn / බඩඉරිඟු)",
        "scientific_name": "Zea mays",
        "category": "Cereal Crop",
        "description": "Maize is a vital coarse grain crop widely grown in Sri Lanka's Dry and Intermediate zones under rainfed or irrigated systems.",
        "optimal_conditions": {
            "soil_type": "Deep Loam / Sandy Loam / Well-drained Red Brown Earth",
            "ph_range": "5.8 - 7.0",
            "temp_range": "18°C - 32°C",
            "humidity_range": "50% - 80%",
            "rainfall_range": "500mm - 800mm"
        },
        "land_prep": [
            "Plow field to 20-25 cm depth and disk harrow to produce a fine seedbed.",
            "Form ridges and furrows (60 cm spacing) to prevent waterlogging.",
            "Incorporate 10 tons/ha of farmyard manure during final tilling."
        ],
        "irrigation": [
            "Germination & Establishment: Irrigate immediately after sowing and again at 4-5 days.",
            "Knee-High Stage: Water every 8-10 days depending on soil moisture.",
            "Tasseling & Silking Stage: Critical water stress period - ensure adequate soil moisture.",
            "Grain Filling: Moderate irrigation; stop watering 15 days before harvest."
        ],
        "fertilizer_schedule": [
            "Basal: 50% N + 100% P + 50% K at planting time in furrows below seed depth.",
            "Top Dressing (3-4 weeks after germination): 25% N as side dressing along rows.",
            "Top Dressing (Tasseling stage, ~6 weeks): Remaining 25% N + 50% K followed by earthing up."
        ],
        "pest_disease_control": [
            "Fall Armyworm (Spodoptera frugiperda): Inspect whorls weekly. Apply Bacillus thuringiensis (Bt) or Emamectin benzoate (0.4g/L) inside leaf whorls.",
            "Maize Stem Borer: Remove infected plants; spray Carbaryl if infestation exceeds 10%.",
            "Northern Corn Leaf Blight: Rotate crops and apply Mancozeb or Azoxystrobin upon early leaf lesions."
        ],
        "harvest_post_harvest": [
            "Harvest when husk leaves turn dry and brown, and grains reach hard dough stage (black layer forms at grain base).",
            "Sun-dry ears on tarpaulins until seed moisture drops to 12%.",
            "Shell cobs and store grains in clean, sealed bins with desiccant."
        ]
    },
    "chickpea": {
        "name": "Chickpea (Gram / කඩල)",
        "scientific_name": "Cicer arietinum",
        "category": "Pulse / Legume",
        "description": "Chickpea is a nutrient-dense pulse crop highly suitable for residual moisture cultivation in dry region soils.",
        "optimal_conditions": {
            "soil_type": "Well-drained Sandy Loam to Clay Loam",
            "ph_range": "6.0 - 7.5",
            "temp_range": "15°C - 29°C",
            "humidity_range": "40% - 65%",
            "rainfall_range": "400mm - 700mm"
        },
        "land_prep": [
            "Chickpea requires a coarse seedbed for proper root aeration and nodulation.",
            "Avoid over-tilling fine dust seedbeds which cause soil crusting after rain.",
            "Apply Rhizobium inoculant to seeds prior to sowing."
        ],
        "irrigation": [
            "Light pre-sowing irrigation to ensure optimal germination.",
            "Branching Stage (~30 days): First post-sowing irrigation.",
            "Pod Development Stage (~60 days): Second critical irrigation.",
            "Avoid irrigation during full flowering stage as it causes flower drop."
        ],
        "fertilizer_schedule": [
            "Chickpea fixes atmospheric Nitrogen. Apply Basal dose: 20 kg N + 50 kg P2O5 + 20 kg K2O per hectare.",
            "Foliar spray of 2% Urea at flowering enhances pod setting."
        ],
        "pest_disease_control": [
            "Pod Borer (Helicoverpa armigera): Install pheromone traps (5 traps/ha). Spray HaNPV or Indoxacarb at pod formation.",
            "Fusarium Wilt: Use certified wilt-resistant seed varieties and treat seeds with Trichoderma viride."
        ],
        "harvest_post_harvest": [
            "Harvest when plants dry out and leaves drop, and pods turn yellowish brown.",
            "Dry harvested plants in the sun for 3-4 days before threshing.",
            "Store seeds at <10% moisture in pest-proof storage containers."
        ]
    },
    "jute": {
        "name": "Jute (ජූට් / ක්‍ෂේත්‍ර කෙඳි)",
        "scientific_name": "Corchorus capsularis",
        "category": "Fiber Crop",
        "description": "Jute is an important commercial fiber crop growing rapidly in warm, humid climates with rich alluvial soils.",
        "optimal_conditions": {
            "soil_type": "Alluvial Loam / Silt Loam",
            "ph_range": "6.0 - 7.2",
            "temp_range": "24°C - 37°C",
            "humidity_range": "70% - 90%",
            "rainfall_range": "1200mm - 1800mm"
        },
        "land_prep": [
            "Plow field 4-5 times to obtain fine tilth seedbed.",
            "Level field thoroughly to ensure even seed distribution and prevent water accumulation."
        ],
        "irrigation": [
            "Sow seeds under optimum soil moisture.",
            "Provide light irrigation every 10-12 days if rains are delayed.",
            "Requires adequate drainage during heavy rainfall to avoid seedling root rot."
        ],
        "fertilizer_schedule": [
            "Basal: 20 kg N + 40 kg P2O5 + 40 kg K2O per hectare.",
            "Top Dressing (3-4 weeks after sowing): 40 kg N/ha after weeding and thinning."
        ],
        "pest_disease_control": [
            "Jute Semilooper & Hairy Caterpillar: Hand-pick early instar larvae. Spray Chlorpyrifos 20 EC if severe.",
            "Stem Rot / Root Rot: Ensure good soil drainage and apply Copper Oxychloride spray."
        ],
        "harvest_post_harvest": [
            "Harvest at small pod stage (120-135 days after sowing) for highest quality fiber.",
            "Steep harvested plants in clear, slow-flowing water (Retting) for 15-20 days.",
            "Extract fiber by hand, wash in clean water, and sun-dry thoroughly."
        ]
    },
    "cotton": {
        "name": "Cotton (පුළුන් / කපු)",
        "scientific_name": "Gossypium hirsutum",
        "category": "Cash / Fiber Crop",
        "description": "Cotton thrives in warm tropical climates with deep black cotton soils or fertile alluvial soils.",
        "optimal_conditions": {
            "soil_type": "Black Cotton Soil / Deep Well-drained Clay Loam",
            "ph_range": "6.0 - 8.0",
            "temp_range": "21°C - 35°C",
            "humidity_range": "50% - 75%",
            "rainfall_range": "600mm - 1100mm"
        },
        "land_prep": [
            "Deep plowing (30 cm) to break hardpan and promote taproot development.",
            "Form ridges and furrows spaced 75-90 cm apart."
        ],
        "irrigation": [
            "Irrigate immediately after planting and at 4-5 days interval for seedling establishment.",
            "Square Formation & Flowering Stage: Irrigate every 12-15 days.",
            "Boll Development Stage: Critical water requirement; stop irrigation when bolls start opening."
        ],
        "fertilizer_schedule": [
            "Basal: 25% N + 100% P + 50% K.",
            "First Top Dressing (Squaring stage, ~45 days): 50% N + 25% K.",
            "Second Top Dressing (Boll formation, ~75 days): Remaining 25% N + 25% K."
        ],
        "pest_disease_control": [
            "Bollworm Complex (American / Pink Bollworm): Monitor with pheromone traps. Spray Spinetoram or Flubendiamide.",
            "Aphids & Whiteflies: Spray Neem oil (5ml/L) or Acetamiprid."
        ],
        "harvest_post_harvest": [
            "Pick fully opened seed cotton (kapas) in clean, dry weather.",
            "Store seed cotton in dry, well-ventilated sheds away from moisture before ginning."
        ]
    },
    "coconut": {
        "name": "Coconut (පොල්)",
        "scientific_name": "Cocos nucifera",
        "category": "Perennial Plantation Crop",
        "description": "Coconut is a major Sri Lankan plantation crop thriving in tropical coastal and inland plain environments.",
        "optimal_conditions": {
            "soil_type": "Sandy Loam / Alluvial / Gravelly Loam",
            "ph_range": "5.5 - 7.5",
            "temp_range": "24°C - 32°C",
            "humidity_range": "70% - 85%",
            "rainfall_range": "1300mm - 2300mm"
        },
        "land_prep": [
            "Dig planting pits of 1m x 1m x 1m size at 8m x 8m spacing.",
            "Fill pits with topsoil mixed with 25 kg organic manure, 1 kg rock phosphate, and husk layer at bottom for moisture retention."
        ],
        "irrigation": [
            "Young palms: Irrigate 45-50 liters of water twice a week during dry spells.",
            "Mature palms: Drip irrigation @ 100-120 liters/palm/day during dry seasons."
        ],
        "fertilizer_schedule": [
            "Apply CRI Recommended Fertilizer Mixture (APN / YPM) twice a year (May-June and Oct-Nov).",
            "Adult Palm Annual Dose: Urea 800g + Rock Phosphate 600g + MOP 1600g + Dolomite 1000g applied around 1.8m basin radius."
        ],
        "pest_disease_control": [
            "Rhinoceros Beetle: Hook out beetles from palm crowns; place naphthalene balls in leaf axils.",
            "Red Palm Weevil: Inject Imidacloprid (1ml/L) into trunk entry holes and seal with mud.",
            "Weligama Coconut Leaf Wilt: Practice field sanitation and control vector planthoppers."
        ],
        "harvest_post_harvest": [
            "Harvest mature nuts every 45-60 days using climbing hooks or long poles.",
            "Store harvested nuts in shade for 2-4 weeks to improve copra recovery and coconut water quality."
        ]
    },
    "papaya": {
        "name": "Papaya (පැපොල්)",
        "scientific_name": "Carica papaya",
        "category": "Fruit Crop",
        "description": "Papaya is a fast-growing, high-value tropical fruit crop yielding continuous harvests under warm climates.",
        "optimal_conditions": {
            "soil_type": "Rich Sandy Loam with excellent drainage",
            "ph_range": "6.0 - 7.0",
            "temp_range": "22°C - 33°C",
            "humidity_range": "60% - 80%",
            "rainfall_range": "1000mm - 1500mm"
        },
        "land_prep": [
            "Dig pits of 60cm x 60cm x 60cm at 2m x 2m spacing.",
            "Fill pits with topsoil, 20 kg compost, and 500g Neem cake. Drainage is vital as papaya stems rot easily in standing water."
        ],
        "irrigation": [
            "Irrigate seedlings every 2-3 days.",
            "Mature plants require 15-20 liters water every 4-5 days during dry periods. Never allow water stagnation around trunk root collar."
        ],
        "fertilizer_schedule": [
            "Monthly application per plant: N: 50g, P: 50g, K: 100g.",
            "Apply 10 kg compost per plant every 6 months to maintain soil structure."
        ],
        "pest_disease_control": [
            "Papaya Mealybug: Biological control using Acerophagus papayae parasitoid or spray Neem oil + soap solution.",
            "Papaya Ring Spot Virus (PRSV): Remove infected plants immediately; control aphid vectors using yellow sticky traps."
        ],
        "harvest_post_harvest": [
            "Harvest fruits when latex turns watery and yellow skin color appears at apex.",
            "Handle fruits carefully to avoid skin bruising and store at 12-14°C."
        ]
    },
    "banana": {
        "name": "Banana (කෙසෙල්)",
        "scientific_name": "Musa acuminata",
        "category": "Fruit Crop",
        "description": "Banana is a widely cultivated fruit in Sri Lanka demanding rich organic soils and continuous water supply.",
        "optimal_conditions": {
            "soil_type": "Deep Rich Loam / Alluvial Soil",
            "ph_range": "6.0 - 7.5",
            "temp_range": "24°C - 35°C",
            "humidity_range": "75% - 90%",
            "rainfall_range": "1500mm - 2500mm"
        },
        "land_prep": [
            "Pits of size 60cm x 60cm x 60cm spaced at 2.4m x 2.4m.",
            "Mix 15 kg well-rotted FYM and 250g Neem cake per pit."
        ],
        "irrigation": [
            "Banana requires frequent irrigation due to broad leaf area.",
            "Irrigate every 3-4 days in dry seasons. Maintain soil moisture at field capacity."
        ],
        "fertilizer_schedule": [
            "Apply Urea 300g, TSP 200g, MOP 400g per plant split across 4 application cycles (2nd, 4th, 6th, 8th month after planting)."
        ],
        "pest_disease_control": [
            "Banana Weevil / Borer: Paring suckers before planting; apply Carbofuran or neem cake around mat base.",
            "Sigatoka Leaf Spot: Prune infected leaves; spray Propiconazole or Mancozeb."
        ],
        "harvest_post_harvest": [
            "Harvest bunches when fingers turn light green and ridges flatten out (usually 80-90 days after flowering).",
            "De-hand bunches and wash in clean water to remove latex before packing in padded crates."
        ]
    },
    "watermelon": {
        "name": "Watermelon (දෙලුම් / පැණි කොමඩු)",
        "scientific_name": "Citrullus lanatus",
        "category": "Cucurbit / Fruit Crop",
        "description": "Watermelon is a fast-maturing cash crop thriving under high sunlight and warm temperatures in dry zones.",
        "optimal_conditions": {
            "soil_type": "Sandy Loam / Well-drained Alluvial Soil",
            "ph_range": "6.0 - 6.8",
            "temp_range": "24°C - 35°C",
            "humidity_range": "50% - 70%",
            "rainfall_range": "400mm - 600mm"
        },
        "land_prep": [
            "Prepare raised beds or broad ridges (2m wide) with deep tillage to support vine growth.",
            "Incorporate 15 tons/ha compost into planting channels."
        ],
        "irrigation": [
            "Drip irrigation or furrow watering every 3-5 days during early growth.",
            "Reduce watering during fruit ripening stage to enhance sugar accumulation and avoid fruit cracking."
        ],
        "fertilizer_schedule": [
            "Basal: 40 kg N + 60 kg P + 50 kg K per hectare.",
            "Top Dressing (Vine extension stage): 40 kg N + 50 kg K per hectare."
        ],
        "pest_disease_control": [
            "Fruit Fly (Bactrocera cucurbitae): Install Cue-lure pheromone traps; wrap young fruits with paper bags.",
            "Powdery Mildew: Spray Wettable Sulfur or Dinocap."
        ],
        "harvest_post_harvest": [
            "Harvest when tendril nearest to fruit stem dries out and ground spot turns yellow.",
            "Cut stem with sharp knife leaving 5 cm stem attached."
        ]
    }
}

# Fallback generic guidance generator for any crop in the dataset
DEFAULT_GUIDANCE = {
    "name": "General Agricultural Crop",
    "scientific_name": "Plantae species",
    "category": "Food / Cash Crop",
    "description": "High-yielding crop suitable for tropical Sri Lankan agricultural conditions with balanced nutrition and proper field management.",
    "optimal_conditions": {
        "soil_type": "Well-drained Loam / Sandy Loam",
        "ph_range": "6.0 - 7.0",
        "temp_range": "20°C - 32°C",
        "humidity_range": "60% - 80%",
        "rainfall_range": "800mm - 1500mm"
    },
    "land_prep": [
        "Plow land 2-3 times to achieve fine tilth and clear weeds.",
        "Incorporate organic compost or farmyard manure at 10 tons/ha prior to planting.",
        "Ensure drainage furrows are prepared to prevent standing water."
    ],
    "irrigation": [
        "Maintain adequate moisture during germination and seedling establishment.",
        "Water every 5-7 days depending on evaporation rate and soil moisture.",
        "Avoid waterlogging around root collar zone."
    ],
    "fertilizer_schedule": [
        "Basal Dressing: Apply full Phosphorus and 30% Nitrogen + Potassium at planting.",
        "Top Dressing 1: Apply 35% Nitrogen + Potassium at vegetative growth peak (~3 weeks).",
        "Top Dressing 2: Apply remaining 35% Nitrogen + Potassium at flowering/fruiting stage."
    ],
    "pest_disease_control": [
        "Monitor fields weekly for sucking insects and leaf caterpillars.",
        "Use IPM principles: yellow sticky traps, light traps, and biopesticides.",
        "Apply copper-based fungicides upon early leaf spot or blight detection."
    ],
    "harvest_post_harvest": [
        "Harvest at full economic maturity during dry morning hours.",
        "Clean, sort, and dry produce to safe moisture content before storage.",
        "Store in cool, dry, ventilated facilities."
    ]
}


def get_crop_guidance(crop_name: str) -> dict:
    """
    Retrieve aftercare guidance for a given crop name.
    Falls back to structured default guidance if exact match is not found.
    """
    key = str(crop_name).strip().lower()
    if key in CROP_GUIDANCE_DATABASE:
        guidance = CROP_GUIDANCE_DATABASE[key].copy()
        guidance["crop_key"] = key
        return guidance
    
    # Capitalize crop name for generic guidance
    custom_guidance = DEFAULT_GUIDANCE.copy()
    custom_guidance["name"] = crop_name.capitalize()
    custom_guidance["crop_key"] = key
    return custom_guidance
