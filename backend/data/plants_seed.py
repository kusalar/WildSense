"""
Comprehensive Botanical Knowledge Base Seed Data for WildSense.
Contains 105+ scientifically curated plant and flower species with broad Indian & global coverage.
Includes taxonomy, synonyms, English common names, verified Hindi & Bengali regional names,
distinguishing botanical characteristics, growth habit, flowering seasons, and safety notes.
"""

from typing import List, Dict, Any

PLANTS_SEED_DATA: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. MEDICINAL & AROMATIC PLANTS (22 Species)
    # =========================================================================
    {
        "id": "ocimum-tenuiflorum",
        "scientific_name": "Ocimum tenuiflorum L.",
        "canonical_name": "Ocimum tenuiflorum",
        "family": "Lamiaceae",
        "genus": "Ocimum",
        "species": "tenuiflorum",
        "synonyms": ["Ocimum sanctum L."],
        "common_names": ["Holy Basil", "Tulsi", "Tulasi", "Sacred Basil"],
        "regional_names": {
            "hi": ["तुलसी (Tulsi)", "कृष्ण तुलसी (Krishna Tulsi)", "राम तुलसी (Rama Tulsi)"],
            "bn": ["তুলসী (Tulsi)", "কৃষ্ণ তুলসী (Krishna Tulsi)"],
            "ta": ["துளசி (Thulasi)"],
            "sa": ["सुरसा (Surasa)", "वृन्दा (Vrinda)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Tropical plains, home gardens, temple courtyards throughout South Asia",
        "flowering_season": "Year-round, peaking July to November",
        "description": "An aromatic erect subshrub growing up to 60 cm tall with purplish to green pubescent stems and strongly scented leaves.",
        "distinguishing_characteristics": "Quadrangular (square) hairy purplish stems; opposite ovate serrated leaves with strong clove-like aromatic scent; small purplish to white verticillaster flowers in racemes.",
        "safety_notes": "Generally safe for consumption as tea. May have mild blood-thinning effects; excessive concentrated extracts should be used cautiously during pregnancy.",
        "confusable_species": [
            "Ocimum basilicum (Sweet Basil) - has hairless green stems and sweeter anise aroma",
            "Ocimum gratissimum (Vana Tulsi) - much larger coarse leaves and strong eugenol scent"
        ]
    },
    {
        "id": "azadirachta-indica",
        "scientific_name": "Azadirachta indica A.Juss.",
        "canonical_name": "Azadirachta indica",
        "family": "Meliaceae",
        "genus": "Azadirachta",
        "species": "indica",
        "synonyms": ["Melia azadirachta L."],
        "common_names": ["Neem", "Indian Lilac", "Margosa"],
        "regional_names": {
            "hi": ["नीम (Neem)"],
            "bn": ["নিম (Nim)"],
            "ta": ["வேப்ப மரம் (Veppam)"],
            "te": ["వేప (Vepa)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "tree",
        "habitat": "Dry tropical and subtropical deciduous forests, roadsides, village commons across India",
        "flowering_season": "March to May",
        "description": "A medium to large evergreen tree reaching 15–20 meters with wide-spreading branches, deeply grooved grey-brown bark, and intensely bitter foliage.",
        "distinguishing_characteristics": "Alternate once-pinnate leaves with 7–17 distinctly falcate (sickle-shaped) asymmetric serrated leaflets; small fragrant white honey-scented star-shaped flowers; yellowish-green ellipsoidal drupes.",
        "safety_notes": "Neem oil is strictly external and toxic if consumed internally in quantity, especially in children (causes metabolic acidosis). Leaves are bitter and used traditionally, but large doses should be avoided.",
        "confusable_species": [
            "Melia azedarach (Chinaberry / Bakain) - has bipinnate (twice-divided) leaves and poisonous spherical yellow berries",
            "Murraya koenigii (Curry leaf) - much smaller shrub/tree with strongly fragrant aromatic leaflets"
        ]
    },
    {
        "id": "aloe-vera",
        "scientific_name": "Aloe vera (L.) Burm.f.",
        "canonical_name": "Aloe vera",
        "family": "Asphodelaceae",
        "genus": "Aloe",
        "species": "vera",
        "synonyms": ["Aloe barbadensis Mill."],
        "common_names": ["Aloe Vera", "Indian Aloe", "Ghritkumari"],
        "regional_names": {
            "hi": ["घृतकुमारी (Ghritkumari)", "ग्वारपाठा (Gwarpatha)"],
            "bn": ["ঘৃতকুমারী (Ghritakumari)"],
            "ta": ["சோற்றுக்கற்றாழை (Sotru Katrazhai)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "succulent",
        "habitat": "Arid to semi-arid tropical soils, rockeries, cultivated pots",
        "flowering_season": "October to March",
        "description": "Stemless or very short-stemmed succulent plant forming dense rosettes of thick fleshy green to grey-green upright leaves filled with clear mucilaginous gel.",
        "distinguishing_characteristics": "Thick lanceolate turgid fleshy leaves with serrated margins bearing small pale teeth; clear soothing inner gel; yellow tubular flowers in an erect terminal spike up to 90 cm high.",
        "safety_notes": "Inner transparent gel is safe topically. The yellow bitter sap (aloin latex) directly under leaf skin is a strong purgative and can cause severe abdominal cramping; avoid during pregnancy.",
        "confusable_species": [
            "Agave americana (Century plant) - much more rigid fibrous leaves with vicious terminal spine",
            "Aloe arborescens (Candelabra aloe) - distinct branched woody stem with arching leaves"
        ]
    },
    {
        "id": "mentha-spicata",
        "scientific_name": "Mentha spicata L.",
        "canonical_name": "Mentha spicata",
        "family": "Lamiaceae",
        "genus": "Mentha",
        "species": "spicata",
        "synonyms": ["Mentha viridis L."],
        "common_names": ["Spearmint", "Garden Mint", "Pudina"],
        "regional_names": {
            "hi": ["पुदीना (Pudina)"],
            "bn": ["পুদিনা (Pudina)"],
            "ta": ["புதினா (Pudhina)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Moist temperate to tropical garden soils, streamsides, kitchen plots",
        "flowering_season": "July to September",
        "description": "A vigorous stoloniferous perennial herb growing 30–80 cm tall with highly aromatic refreshing green foliage and upright purple-flowering spikes.",
        "distinguishing_characteristics": "Opposite sessile or sub-sessile ovate-lanceolate serrated leaves; square stems; slender terminal spikes with pinkish-lilac flowers; characteristic carvone-rich cooling mint aroma.",
        "safety_notes": "Safe culinary herb. Pure concentrated essential oil is an irritant and should not be inhaled by infants.",
        "confusable_species": [
            "Mentha x piperita (Peppermint) - leaves are stalked (petiolate) with higher menthol pungency",
            "Mentha arvensis (Corn mint / Field mint) - flowers are in axillary whorls rather than terminal spikes"
        ]
    },
    {
        "id": "cymbopogon-citratus",
        "scientific_name": "Cymbopogon citratus (DC.) Stapf",
        "canonical_name": "Cymbopogon citratus",
        "family": "Poaceae",
        "genus": "Cymbopogon",
        "species": "citratus",
        "synonyms": ["Andropogon citratus DC."],
        "common_names": ["Lemongrass", "West Indian Lemongrass", "Lemon Grass"],
        "regional_names": {
            "hi": ["लेमनग्रास (Lemongrass)", "गंधतृण (Gandhatrina)"],
            "bn": ["লেমনগ্রাস (Lemongrass)", "লেবুঘাস (Lebughas)"],
            "ta": ["எலுமிச்சைப்புல் (Elumichai Pul)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Warm tropical and subtropical climates, well-drained loamy soils, cultivated fields",
        "flowering_season": "Rarely flowers under cultivation; flowers in autumn if mature",
        "description": "A tall perennial tufted grass with dense clump-forming culms, linear arching bluish-green foliage, and a distinctive citrus aroma when crushed.",
        "distinguishing_characteristics": "Thick swollen basal stalks; long linear arching leaf blades with rough scaberulous margins; strong unmistakable lemon-citral scent when bruised.",
        "safety_notes": "Edible culinary herb in tea and cooking. Rough leaf margins can cause minor paper-like skin cuts if handled carelessly.",
        "confusable_species": [
            "Cymbopogon winterianus (Citronella grass) - has reddish basal stems and sharper insect-repellent scent",
            "Cymbopogon flexuosus (East Indian lemongrass) - taller, seeds prolifically, darker purple-tinged leaf sheaths"
        ]
    },
    {
        "id": "curcuma-longa",
        "scientific_name": "Curcuma longa L.",
        "canonical_name": "Curcuma longa",
        "family": "Zingiberaceae",
        "genus": "Curcuma",
        "species": "longa",
        "synonyms": ["Curcuma domestica Valeton"],
        "common_names": ["Turmeric", "Indian Saffron", "Haldi"],
        "regional_names": {
            "hi": ["हल्दी (Haldi)"],
            "bn": ["হলুদ (Holud)"],
            "ta": ["மஞ்சள் (Manjal)"],
            "sa": ["हरिद्रा (Haridra)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Warm humid tropics with abundant rainfall, partial shade under trees or open fertile beds",
        "flowering_season": "August to October",
        "description": "Rhizomatous perennial herb reaching up to 1 meter in height with broad oblong-lanceolate leaves and brilliant orange-yellow cylindrical branched rhizomes.",
        "distinguishing_characteristics": "Large oblong pointed distichous leaves with prominent parallel veins; central spike surrounded by green to white/pink tipped sterile bracts; intense golden-yellow interior rhizome with curcumin aroma.",
        "safety_notes": "Safe culinary spice. Excessive therapeutic supplemental doses may cause gastrointestinal discomfort or interact with anticoagulant medications.",
        "confusable_species": [
            "Zingiber officinale (Ginger) - narrower leaves and pale yellowish rhizomes with sharp zingerone pungency",
            "Curcuma caesia (Black Turmeric) - leaves have deep purple midrib and rhizomes are bluish-black inside"
        ]
    },
    {
        "id": "zingiber-officinale",
        "scientific_name": "Zingiber officinale Roscoe",
        "canonical_name": "Zingiber officinale",
        "family": "Zingiberaceae",
        "genus": "Zingiber",
        "species": "officinale",
        "synonyms": ["Amomum zingiber L."],
        "common_names": ["Ginger", "Garden Ginger", "Adrak"],
        "regional_names": {
            "hi": ["अदरक (Adrak)", "सोंठ (Sonth - dry)"],
            "bn": ["আদা (Ada)"],
            "ta": ["இஞ்சி (Inji)"],
            "sa": ["आर्द्रक (Aadraka)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Moist, warm tropical forest understories and cultivated fields with rich organic soil",
        "flowering_season": "Summer to early autumn; rarely flowers in cultivation",
        "description": "An herbaceous reed-like perennial growing 60–100 cm tall from thick knobby branched pale-yellow rhizomes with warm pungent flavor.",
        "distinguishing_characteristics": "Slender pseudostems composed of overlapping leaf sheaths; narrow linear-lanceolate alternate leaves (15–20 cm long); knobby pale tan finger-like rhizome with pungent aroma.",
        "safety_notes": "Safe culinary root. May potentiate blood-thinning medications in massive doses.",
        "confusable_species": [
            "Curcuma longa (Turmeric) - much wider oblong leaf blades and deep orange interior rhizome",
            "Alpinia galanga (Galangal) - much larger plant with woody pinkish-white rhizomes smelling of camphor"
        ]
    },
    {
        "id": "murraya-koenigii",
        "scientific_name": "Murraya koenigii (L.) Spreng.",
        "canonical_name": "Murraya koenigii",
        "family": "Rutaceae",
        "genus": "Murraya",
        "species": "koenigii",
        "synonyms": ["Bergera koenigii L."],
        "common_names": ["Curry Leaf Plant", "Curry Tree", "Sweet Neem"],
        "regional_names": {
            "hi": ["कढ़ी पत्ता (Kadhi Patta)", "मीठा नीम (Meetha Neem)"],
            "bn": ["কারিপাতা (Kari Pata)", "মিষ্টি নিম (Mishti Nim)"],
            "ta": ["கறிவேப்பிலை (Kariveppilai)"],
            "te": ["కరివేపాకు (Karivepaku)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "shrub",
        "habitat": "Subtropical scrub forests, foothills of the Himalayas to southern India, home kitchen gardens",
        "flowering_season": "April to May",
        "description": "An aromatic small deciduous shrub or tree up to 4–6 meters high, widely prized for its highly pungent culinary leaves.",
        "distinguishing_characteristics": "Pinnate leaves with 11–21 asymmetric ovate-lanceolate leaflets with serrulate margins; strong warm aromatic citrus-sulfur scent when crushed; clusters of small white fragrant funnel-shaped flowers; shiny black berries when ripe.",
        "safety_notes": "Foliage is edible and commonly eaten cooked. Raw seeds inside berries are toxic and should not be crushed or swallowed in quantity.",
        "confusable_species": [
            "Azadirachta indica (Neem) - leaves look superficially similar but are bitterly astringent, not warmly aromatic",
            "Clausena heptaphylla - leaflets have an anise-like aroma rather than curry aroma"
        ]
    },
    {
        "id": "withania-somnifera",
        "scientific_name": "Withania somnifera (L.) Dunal",
        "canonical_name": "Withania somnifera",
        "family": "Solanaceae",
        "genus": "Withania",
        "species": "somnifera",
        "synonyms": ["Physalis somnifera L."],
        "common_names": ["Ashwagandha", "Indian Ginseng", "Poison Gooseberry", "Winter Cherry"],
        "regional_names": {
            "hi": ["अश्वगंधा (Ashwagandha)", "असंगध (Asgandh)"],
            "bn": ["অশ্বগন্ধা (Ashwagandha)"],
            "ta": ["அமுக்கிரா (Amukkira)"],
            "sa": ["अश्वगन्धा (Ashvagandha)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "shrub",
        "habitat": "Dry and stony areas, wastelands, arid plains of western and central India",
        "flowering_season": "Year-round, primarily July to November",
        "description": "A stout erect tomentose subshrub 30–120 cm high covered in fine stellate silvery hairs, producing small greenish bell flowers and orange-red berries enclosed in an inflated papery calyx.",
        "distinguishing_characteristics": "Dull green elliptic-ovate leaves with fine greyish stellate pubescence; small greenish-yellow axillary clustered flowers; red berry inside an inflated papery lantern-like calyx; root has a distinct horse-like earthy odor.",
        "safety_notes": "Roots are widely used in traditional adaptogenic formulas. Berries and foliage are non-edible. Avoid therapeutic supplementation during pregnancy.",
        "confusable_species": [
            "Physalis angulata (Wild cape gooseberry) - annual herbaceous weed with hairless stems and edible sweet/sour yellow fruit",
            "Solanum nigrum (Black nightshade) - produces dark black berries without lantern calyx"
        ]
    },
    {
        "id": "bacopa-monnieri",
        "scientific_name": "Bacopa monnieri (L.) Wettst.",
        "canonical_name": "Bacopa monnieri",
        "family": "Plantaginaceae",
        "genus": "Bacopa",
        "species": "monnieri",
        "synonyms": ["Herpestis monnieria (L.) Kunth", "Lysimachia monnieri L."],
        "common_names": ["Brahmi", "Water Hyssop", "Thyme-leaved Gratiola"],
        "regional_names": {
            "hi": ["ब्राह्मी (Brahmi)"],
            "bn": ["ব্রাহ্মী শাক (Brahmi Shak)"],
            "ta": ["நீர்ப் பிராமி (Neer Brahmi)"],
            "sa": ["ब्राह्मी (Brahmi)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Wet marshy stream margins, shallow wetlands, rice paddy borders across tropical Asia",
        "flowering_season": "April to October",
        "description": "A small creeping glabrous succulent perennial herb rooting at nodes, forming low mats in damp soil.",
        "distinguishing_characteristics": "Small oblong-oblanceolate opposite succulent sessile leaves (1–2 cm); pale blue or white solitary axillary 4–5 lobed flowers on slender pedicels; aquatic/marsh creeping habit.",
        "safety_notes": "Widely consumed as a nootropic leafy herb. May cause mild nausea or digestive cramping if taken on an empty stomach in high doses.",
        "confusable_species": [
            "Centella asiatica (Gotu Kola / Mandukaparni) - often also called Brahmi in north India, but has kidney-shaped serrated leaves with long petioles",
            "Mecardonia procumbens - similar marsh herb but with yellow flowers"
        ]
    },
    {
        "id": "centella-asiatica",
        "scientific_name": "Centella asiatica (L.) Urb.",
        "canonical_name": "Centella asiatica",
        "family": "Apiaceae",
        "genus": "Centella",
        "species": "asiatica",
        "synonyms": ["Hydrocotyle asiatica L."],
        "common_names": ["Gotu Kola", "Indian Pennywort", "Mandukaparni", "Thankuni"],
        "regional_names": {
            "hi": ["मंडूकपर्णी (Mandukaparni)", "ब्रह्ममंडूकी (Brahmamanduki)"],
            "bn": ["থানকুনী পাতা (Thankuni Pata)"],
            "ta": ["வல்லாரை (Vallarai)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Damp wetlands, marshy grasslands, edges of canals and ponds throughout tropical Asia",
        "flowering_season": "April to July",
        "description": "A low-growing creeping perennial herb producing long slender horizontal stolons that root at nodes, bearing kidney-shaped scalloped leaves.",
        "distinguishing_characteristics": "Reniform to orbicular fan-shaped leaves with crenate margins; long channeled petioles emerging from nodes; tiny pink to white flowers in small umbels near ground level.",
        "safety_notes": "Commonly eaten fresh in salads and traditional curries. Safe in typical dietary amounts; excessive long-term doses may burden the liver.",
        "confusable_species": [
            "Hydrocotyle vulgaris (Common pennywort) - leaves are strictly peltate (stem attaches at center of round leaf like an umbrella)",
            "Bacopa monnieri - fleshy oblong leaves without stalks"
        ]
    },
    {
        "id": "phyllanthus-emblica",
        "scientific_name": "Phyllanthus emblica L.",
        "canonical_name": "Phyllanthus emblica",
        "family": "Phyllanthaceae",
        "genus": "Phyllanthus",
        "species": "emblica",
        "synonyms": ["Emblica officinalis Gaertn."],
        "common_names": ["Amla", "Indian Gooseberry", "Emblic Myrobalan"],
        "regional_names": {
            "hi": ["आंवला (Amla)"],
            "bn": ["আমলকী (Amloki)"],
            "ta": ["நெல்லிக்காய் (Nellikai)"],
            "sa": ["आमलकी (Amalaki)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "tree",
        "habitat": "Deciduous and mixed forests of the Indian subcontinent, dry rocky hills, cultivated orchards",
        "flowering_season": "March to May",
        "description": "A small to medium deciduous tree 8–18 m high with light grey bark and feathery light-green foliage resembling pinnate leaves.",
        "distinguishing_characteristics": "Branchlets densely set with tiny linear-oblong distichous leaves appearing like fine pinnate foliage; greenish-yellow spherical hard fleshy berries with 6 vertical indistinct furrows; astringent sour taste.",
        "safety_notes": "Highly nutritious fruit rich in Vitamin C. Generally safe; high sour intake may aggravate acid reflux in sensitive individuals.",
        "confusable_species": [
            "Phyllanthus acidus (Star gooseberry / Harfarauri) - fruit is distinctly 6–8 lobed star-shaped and much more acidic",
            "Tamarindus indica (Tamarind) - pinnate leaves with brown bean-like pods, not round fleshy berries"
        ]
    },
    {
        "id": "tinospora-cordifolia",
        "scientific_name": "Tinospora cordifolia (Willd.) Miers",
        "canonical_name": "Tinospora cordifolia",
        "family": "Menispermaceae",
        "genus": "Tinospora",
        "species": "cordifolia",
        "synonyms": ["Menispermum cordifolium Willd."],
        "common_names": ["Giloy", "Guduchi", "Heart-leaved Moonseed"],
        "regional_names": {
            "hi": ["गिलोय (Giloy)", "गुडूची (Guduchi)"],
            "bn": ["গুলঞ্চ (Gulancha)"],
            "ta": ["சீந்தில் (Seenthil)"],
            "sa": ["अमृता (Amrita)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "climber",
        "habitat": "Tropical deciduous forests, climbing on large trees like Neem, Banyan, and Mango",
        "flowering_season": "January to April",
        "description": "A large glabrous deciduous climbing shrub with corky grooved bark, slender aerial roots descending from branches, and heart-shaped leaves.",
        "distinguishing_characteristics": "Heart-shaped (cordate) membranous leaves with 7–9 basal palmate veins; aerial thread-like roots; greyish succulent stem with prominent lenticels; small yellow unisexual flowers; red pea-sized drupes.",
        "safety_notes": "Widely utilized immune-modulating herb. Rare cases of idiosyncratic liver inflammation reported with unregulated high-concentration commercial extracts.",
        "confusable_species": [
            "Tinospora crispa - stem has prominent wart-like tubercles and produces yellow-orange fruit",
            "Piper betle (Paan) - thicker leathery leaves with characteristic peppery aromatic scent"
        ]
    },
    {
        "id": "asparagus-racemosus",
        "scientific_name": "Asparagus racemosus Willd.",
        "canonical_name": "Asparagus racemosus",
        "family": "Asparagaceae",
        "genus": "Asparagus",
        "species": "racemosus",
        "synonyms": ["Asparagopsis racemosa (Willd.) Kunth"],
        "common_names": ["Shatavari", "Wild Asparagus", "Satavar"],
        "regional_names": {
            "hi": ["शतावरी (Shatavari)", "सतावर (Satavar)"],
            "bn": ["শতমুখী (Shatamukhi)", "শতমূলী (Shatamuli)"],
            "ta": ["தண்ணீர்விட்டான் கிழங்கு (Thanneer Vittan Kizhangu)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "climber",
        "habitat": "Rocky dry soils, tropical scrub jungles and lower Himalayan foothills up to 1400m",
        "flowering_season": "June to August",
        "description": "A woody climbing perennial with prickly stems, feathery needle-like branchlets (cladodes), and a tuberous cluster of succulent spindle-shaped roots.",
        "distinguishing_characteristics": "Sharp recurved spines on woody stems; fine sickle-shaped cladodes in clusters of 2–6 resembling pine needles; small fragrant white flowers in racemes; red spherical berries.",
        "safety_notes": "Tuberous roots are widely used for female reproductive tonic formulations. Safe in traditional food/herbal amounts; raw berries are mildly toxic.",
        "confusable_species": [
            "Asparagus setaceus (Lace fern / Asparagus fern) - delicate horizontal flat fronds, non-climbing ornamental",
            "Asparagus densiflorus (Foxtail fern) - dense cylindrical plume-like stems"
        ]
    },
    {
        "id": "andrographis-paniculata",
        "scientific_name": "Andrographis paniculata (Burm.f.) Nees",
        "canonical_name": "Andrographis paniculata",
        "family": "Acanthaceae",
        "genus": "Andrographis",
        "species": "paniculata",
        "synonyms": ["Justicia paniculata Burm.f."],
        "common_names": ["Kalmegh", "Green Chiretta", "King of Bitters"],
        "regional_names": {
            "hi": ["कालमेघ (Kalmegh)", "कड़वा चिरायता (Kadva Chirayata)"],
            "bn": ["কালমেঘ (Kalmegh)"],
            "ta": ["நிலவேம்பு (Nilavembu)"],
            "te": ["నేలవేము (Nelavemu)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Moist shady wastelands, deciduous forests, agricultural field bunds across India and Sri Lanka",
        "flowering_season": "September to December",
        "description": "An erect annual herb growing 30–90 cm tall with sharply quadrangular winged stems and extraordinarily bitter taste throughout all plant tissues.",
        "distinguishing_characteristics": "Dark green 4-angled winged stems; opposite lanceolate glabrous leaves; small solitary or panicled white flowers with rose-purple spots on lower lip; intensely, extraordinarily bitter taste.",
        "safety_notes": "Well-studied respiratory and febrile remedy (Nilavembu Kudineer component). Very bitter; excessive doses can cause gastric upset or allergic hives.",
        "confusable_species": [
            "Swertia chirayita (True Chirata) - temperate Himalayan gentian with round stems, larger yellow-purple flowers",
            "Justicia adhatoda - much larger perennial shrub with broad leaves"
        ]
    },
    {
        "id": "justicia-adhatoda",
        "scientific_name": "Justicia adhatoda L.",
        "canonical_name": "Justicia adhatoda",
        "family": "Acanthaceae",
        "genus": "Justicia",
        "species": "adhatoda",
        "synonyms": ["Adhatoda vasica Nees"],
        "common_names": ["Vasaka", "Malabar Nut", "Adhatoda"],
        "regional_names": {
            "hi": ["वासा (Vasa)", "अड़ूसा (Adusa)"],
            "bn": ["বাসক (Basak)"],
            "ta": ["ஆடாதோடை (Adathodai)"],
            "sa": ["वासक (Vasaka)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "shrub",
        "habitat": "Plains and lower sub-Himalayan valleys, roadside hedges and village thickets",
        "flowering_season": "December to April",
        "description": "A dense evergreen perennial shrub 1.5–3 m high with opposite lanceolate leaves, unpleasant scent when crushed, and dense white spikes.",
        "distinguishing_characteristics": "Large opposite elliptic-lanceolate dark green leaves (10–20 cm) with bitter taste; large white bilabiate flowers with purple-veined lower throat crowded in short spikes; distinct foul vegetative smell.",
        "safety_notes": "Well-known bronchodilator (source of vasicine / bromhexine precursor). Uterine stimulant; contraindicated during pregnancy.",
        "confusable_species": [
            "Cestrum nocturnum (Raat ki Rani) - alternate leaves and tubular pale green flowers, fragrant only at night",
            "Clerodendrum infortunatum (Bhant) - square stems and pinkish-white flowers with long exerted stamens"
        ]
    },
    {
        "id": "lawsonia-inermis",
        "scientific_name": "Lawsonia inermis L.",
        "canonical_name": "Lawsonia inermis",
        "family": "Lythraceae",
        "genus": "Lawsonia",
        "species": "inermis",
        "synonyms": ["Lawsonia alba Lam."],
        "common_names": ["Henna", "Mehendi", "Mignonette Tree"],
        "regional_names": {
            "hi": ["मेंहदी (Mehendi)"],
            "bn": ["মেহেদি (Mehedi)"],
            "ta": ["மருதாணி (Maruthani)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "shrub",
        "habitat": "Semi-arid to sub-humid tropical scrub, hedges, and irrigated fields of Rajasthan and Gujarat",
        "flowering_season": "May to July",
        "description": "A glabrous much-branched shrub or small tree 2–6 m tall, famous for its lawsone pigment used worldwide as natural skin dye and hair conditioner.",
        "distinguishing_characteristics": "Opposite entire small elliptic-lanceolate leaves (1.5–4 cm long); spiny branchlets on older wood; sweet-smelling clusters of 4-petaled cream-white or reddish flowers; small round capsule fruits.",
        "safety_notes": "Natural henna paste is safe externally. Beware of adulterated 'Black Henna' which contains toxic paraphenylenediamine (PPD) causing severe chemical burns.",
        "confusable_species": [
            "Punica granatum (Pomegranate) - leaves are similar size but opposite/fascicled with glossy texture and large scarlet flowers",
            "Dodonaea viscosa - alternate sticky resinous leaves"
        ]
    },
    {
        "id": "piper-nigrum",
        "scientific_name": "Piper nigrum L.",
        "canonical_name": "Piper nigrum",
        "family": "Piperaceae",
        "genus": "Piper",
        "species": "nigrum",
        "synonyms": [],
        "common_names": ["Black Pepper", "King of Spices", "Kali Mirch"],
        "regional_names": {
            "hi": ["काली मिर्च (Kali Mirch)"],
            "bn": ["গোল মরিচ (Gol Morich)"],
            "ta": ["மிளகு (Milagu)"],
            "sa": ["मरिच (Maricha)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "climber",
        "habitat": "Warm humid evergreen rainforests of the Western Ghats (Kerala, Karnataka), climbing on tall support trees",
        "flowering_season": "May to August",
        "description": "A vigorous woody perennial evergreen climber rooting at nodes, reaching up to 10 m up tree trunks with broad glossy cordate-ovate leaves.",
        "distinguishing_characteristics": "Alternate broad ovate-cordate leathery glossy leaves with 5–7 prominent curving veins; swollen stem nodes; pendulous spikes (8–15 cm) packed with small sessile green drupes that ripen to red.",
        "safety_notes": "Safe culinary spice. Ingestion of massive quantities of piperine extract can cause mucosal irritation.",
        "confusable_species": [
            "Piper betle (Betel vine) - leaves are more heart-shaped and non-peppery, used as masticatory",
            "Piper longum (Pippali / Long pepper) - upright cylindrical spike fruits, not spherical drupes"
        ]
    },
    {
        "id": "trachyspermum-ammi",
        "scientific_name": "Trachyspermum ammi (L.) Sprague",
        "canonical_name": "Trachyspermum ammi",
        "family": "Apiaceae",
        "genus": "Trachyspermum",
        "species": "ammi",
        "synonyms": ["Carum copticum (L.) Benth. & Hook.f."],
        "common_names": ["Ajwain", "Bishop's Weed", "Carom Seed Plant"],
        "regional_names": {
            "hi": ["अजवाइन (Ajwain)"],
            "bn": ["জোয়ান (Jowan)"],
            "ta": ["ஓமம் (Omam)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Cultivated across Rajasthan, Gujarat, Madhya Pradesh, and plains of South Asia",
        "flowering_season": "January to March",
        "description": "An erect annual herbaceous plant 30–90 cm tall with highly dissected feathery leaves and small white flowers arranged in terminal compound umbels.",
        "distinguishing_characteristics": "Feathery multi-pinnatisect thread-like leaf segments; compound umbels of tiny white flowers; small greyish-brown ridged schizocarp fruits with intense thymol (thyme/oregano) scent and pungent warm bite.",
        "safety_notes": "Safe culinary spice and carminative digestive seed. Avoid pure thymol oil ingestion in high doses.",
        "confusable_species": [
            "Cuminum cyminum (Cumin / Jeera) - larger brownish fruits with warm earthy cumin aroma, lacking thymol scent",
            "Foeniculum vulgare (Fennel / Saunf) - much taller with sweet licorice-scented yellow flowers"
        ]
    },
    {
        "id": "chrysopogon-zizanioides",
        "scientific_name": "Chrysopogon zizanioides (L.) Roberty",
        "canonical_name": "Chrysopogon zizanioides",
        "family": "Poaceae",
        "genus": "Chrysopogon",
        "species": "zizanioides",
        "synonyms": ["Vetiveria zizanioides (L.) Nash"],
        "common_names": ["Vetiver", "Khus", "Khas Grass"],
        "regional_names": {
            "hi": ["खस (Khus)", "उशीर (Ushira)"],
            "bn": ["খসখস (Khus-khus)", "বীরণ (Biran)"],
            "ta": ["வெட்டிவேர் (Vettiver)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Riverbanks, marshy alluvial floodplains, bunds across northern and southern India",
        "flowering_season": "August to October",
        "description": "A densely tufted perennial grass growing in massive clumps 1.5–2 m tall with deep fibrous spongy roots famous for cooling vetiver essential oil.",
        "distinguishing_characteristics": "Tall erect spongy culms; stiff erect folded linear leaves with scabrous margins; large brownish-purple panicles (15–30 cm); massive dense aromatic root system smelling of cooling damp forest earth.",
        "safety_notes": "Safe natural aromatic root. Often used in water flavoring and cooling screens. Leaves are non-edible.",
        "confusable_species": [
            "Saccharum spontaneum (Kans grass) - produces dazzling silvery-white feathery plumes and non-aromatic roots",
            "Cymbopogon citratus (Lemongrass) - leaves smell strongly of lemon, not earthy vetiver"
        ]
    },
    {
        "id": "elettaria-cardamomum",
        "scientific_name": "Elettaria cardamomum (L.) Maton",
        "canonical_name": "Elettaria cardamomum",
        "family": "Zingiberaceae",
        "genus": "Elettaria",
        "species": "cardamomum",
        "synonyms": ["Amomum cardamomum L."],
        "common_names": ["Green Cardamom", "True Cardamom", "Elaichi"],
        "regional_names": {
            "hi": ["छोटी इलायची (Chhoti Elaichi)"],
            "bn": ["ছোট এলাচ (Chhoto Elach)"],
            "ta": ["ஏலக்காய் (Yelakkai)"],
            "sa": ["एला (Ela)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Shaded evergreen cloud forests of the Western Ghats (Cardamom Hills, Kerala/Karnataka) between 600–1500m",
        "flowering_season": "April to August",
        "description": "A magnificent robust rhizomatous perennial reed 2–4 m high with large lanceolate leaves and prostrate panicles trailing on the ground.",
        "distinguishing_characteristics": "Pseudostems with large alternate dark-green glossy leaves (30–60 cm long); flowering panicles emerge horizontally along forest floor; white flowers with violet-striped lip; 3-valved pale green aromatic capsules.",
        "safety_notes": "Safe culinary aromatic spice. Rare allergic contact dermatitis reported with concentrated oil.",
        "confusable_species": [
            "Amomum subulatum (Black / Large cardamom) - mountain Himalayan species with dark brown coarse wrinkled capsules",
            "Alpinia galanga - upright panicle terminal on stems, not prostrate on soil"
        ]
    },
    {
        "id": "ocimum-basilicum",
        "scientific_name": "Ocimum basilicum L.",
        "canonical_name": "Ocimum basilicum",
        "family": "Lamiaceae",
        "genus": "Ocimum",
        "species": "basilicum",
        "synonyms": [],
        "common_names": ["Sweet Basil", "Sabja Plant", "Genovese Basil"],
        "regional_names": {
            "hi": ["सब्जा (Sabja)", "तुकमरिया (Tukmaria)", "मीठा तुलसी (Meetha Tulsi)"],
            "bn": ["বাবুই তুলসী (Babui Tulsi)", "সবজা (Sabja)"],
            "ta": ["திருநீற்றுப்பச்சிலை (Thirunitrupachilai)"]
        },
        "category": "medicinal_aromatic",
        "growth_type": "herb",
        "habitat": "Cultivated globally in culinary gardens, temperate to tropical regions",
        "flowering_season": "June to September",
        "description": "A bushy annual herb 30–60 cm tall with smooth glossy bright green ovate leaves and warm sweet spicy aroma with hints of anise.",
        "distinguishing_characteristics": "Glabrous (non-hairy) green stems; glossy broader ovate leaves; white to pale pink two-lipped flowers; black tear-shaped seeds (Sabja) that swell dramatically in water to form gelatinous coatings.",
        "safety_notes": "Safe culinary herb and beverage seed. Highly mucilaginous seeds must be soaked in water before consuming to prevent choking.",
        "confusable_species": [
            "Ocimum tenuiflorum (Holy Basil / Tulsi) - hairy purplish stems, smaller serrate leaves, clove/eugenol scent",
            "Ocimum americanum (Hoary basil) - white hairy calyces and smaller leaves"
        ]
    },

    # =========================================================================
    # 2. FLOWERS & ORNAMENTALS (24 Species)
    # =========================================================================
    {
        "id": "hibiscus-rosa-sinensis",
        "scientific_name": "Hibiscus rosa-sinensis L.",
        "canonical_name": "Hibiscus rosa-sinensis",
        "family": "Malvaceae",
        "genus": "Hibiscus",
        "species": "rosa-sinensis",
        "synonyms": [],
        "common_names": ["China Rose", "Hibiscus", "Shoeblack Plant", "Gurhal"],
        "regional_names": {
            "hi": ["गुड़हल (Gurhal)", "जवाकुसुम (Jawakusum)"],
            "bn": ["জবা ফুল (Jaba Phul)"],
            "ta": ["செம்பருத்தி (Sembaruthi)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Cultivated across tropical and subtropical gardens worldwide, ubiquitous in Indian home yards",
        "flowering_season": "Year-round in tropical climates",
        "description": "A bushy evergreen shrub or small tree 2.5–5 m tall with glossy dark green leaves and magnificent solitary funnel-shaped flowers in red, pink, yellow, and white.",
        "distinguishing_characteristics": "Alternate ovate-lanceolate leaves with coarse serrations toward the tip; large 5-petaled or double bell-shaped flowers; prominent long exerted staminal column with yellow anthers and 5-lobed stigma at tip.",
        "safety_notes": "Flowers and leaves are edible, non-toxic, and used in teas and hair care formulations.",
        "confusable_species": [
            "Hibiscus syriacus (Rose of Sharon) - deciduous hardy shrub with deeply 3-lobed leaves",
            "Malvaviscus arboreus (Turk's cap) - petals never fully open, remain tightly furled around staminal column"
        ]
    },
    {
        "id": "tagetes-erecta",
        "scientific_name": "Tagetes erecta L.",
        "canonical_name": "Tagetes erecta",
        "family": "Asteraceae",
        "genus": "Tagetes",
        "species": "erecta",
        "synonyms": [],
        "common_names": ["African Marigold", "Aztec Marigold", "Genda"],
        "regional_names": {
            "hi": ["गेंदा (Genda)", "गेंदा फूल (Genda Phool)"],
            "bn": ["গাঁদা ফুল (Gada Phul)"],
            "ta": ["சாமந்தி (Saamandi)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Widely cultivated across Indian agricultural fields for festival garlands and pest management",
        "flowering_season": "October to March (winter festival peak)",
        "description": "A stout erect annual herb 40–100 cm tall bearing deeply pinnatifid pungent leaves and large globular flowerheads in vibrant golden, yellow, and orange hues.",
        "distinguishing_characteristics": "Opposite or alternate pinnately divided leaves with translucent oil glands along margins; strong pungent musky fragrance; large dense globular composite heads (5–12 cm across) of ruffled ray florets.",
        "safety_notes": "Non-toxic ornamental and garland flower. Leaves can occasionally trigger contact skin dermatitis in sensitive individuals due to phototoxic thiophenes.",
        "confusable_species": [
            "Tagetes patula (French marigold) - much smaller compact bush with multi-colored bicolored (red and yellow) flowerheads",
            "Calendula officinalis (Pot marigold) - simple non-divided sticky leaves and flat daisy-like heads"
        ]
    },
    {
        "id": "rosa-indica",
        "scientific_name": "Rosa indica L.",
        "canonical_name": "Rosa indica",
        "family": "Rosaceae",
        "genus": "Rosa",
        "species": "indica",
        "synonyms": ["Rosa chinensis Jacq."],
        "common_names": ["Indian Rose", "China Rose", "Gulab", "Desi Gulab"],
        "regional_names": {
            "hi": ["गुलाब (Gulab)", "देसी गुलाब (Desi Gulab)"],
            "bn": ["গোলাপ (Golap)"],
            "ta": ["ரோஜா (Roja)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Gardens, commercial rose nurseries across Uttar Pradesh, Rajasthan, and Karnataka",
        "flowering_season": "November to March (temperate) and year-round with irrigation",
        "description": "An upright or climbing prickly deciduous to semi-evergreen shrub renowned for intensely fragrant pink or deep red blossoms harvested for rosewater and gulkand.",
        "distinguishing_characteristics": "Woody stems armed with hooked prickles (thorns); alternate pinnately compound leaves with 3–7 serrate ovate leaflets; fragrant multi-petaled blossoms with numerous stamens surrounding hypanthium; fleshy red rose hips.",
        "safety_notes": "Petals and hips are safe, edible, and non-toxic. Watch for sharp stem prickles.",
        "confusable_species": [
            "Rosa damascena (Damask Rose) - 30-petaled pale pink intensely perfumed rose with glandular bristles",
            "Hibiscus rosa-sinensis - lacks prickles, possesses single staminal column"
        ]
    },
    {
        "id": "jasminum-sambac",
        "scientific_name": "Jasminum sambac (L.) Aiton",
        "canonical_name": "Jasminum sambac",
        "family": "Oleaceae",
        "genus": "Jasminum",
        "species": "sambac",
        "synonyms": ["Nyctanthes sambac L."],
        "common_names": ["Arabian Jasmine", "Mogra", "Beli", "Tuscan Jasmine"],
        "regional_names": {
            "hi": ["मोगरा (Mogra)", "मोतिया (Motiya)"],
            "bn": ["বেলী ফুল (Beli Phul)"],
            "ta": ["மல்லிகை (Malligai)"],
            "te": ["మల్లెపువ్వు (Mallepuvvu)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Warm humid tropics, courtyard gardens, commercial jasmine farms across Tamil Nadu and West Bengal",
        "flowering_season": "March to August",
        "description": "A small scrambling evergreen shrub or weak climber up to 2–3 m with intensely sweet-scented pure white flowers used for garlands, teas, and perfumes.",
        "distinguishing_characteristics": "Opposite or in whorls of 3, glossy ovate-elliptic leaves with prominent undulating margins; clusters of intensely fragrant starry pure white flowers (single or double petals) that open at dusk and turn purplish as they fade.",
        "safety_notes": "Non-toxic flowers widely used in culinary teas and adornments. Foliage is non-edible.",
        "confusable_species": [
            "Tabernaemontana divaricata (Crape jasmine / Chandni) - unscented white flowers that release white milky sap when stems are broken",
            "Jasminum grandiflorum (Chameli / Spanish jasmine) - pinnate leaves with 7–11 leaflets, not simple opposite leaves"
        ]
    },
    {
        "id": "nelumbo-nucifera",
        "scientific_name": "Nelumbo nucifera Gaertn.",
        "canonical_name": "Nelumbo nucifera",
        "family": "Nelumbonaceae",
        "genus": "Nelumbo",
        "species": "nucifera",
        "synonyms": ["Nelumbium speciosum Willd."],
        "common_names": ["Sacred Lotus", "Indian Lotus", "Kamal", "Padma"],
        "regional_names": {
            "hi": ["कमल (Kamal)", "पद्म (Padma)"],
            "bn": ["পদ্ম ফুল (Padma Phul)"],
            "ta": ["தாமரை (Thamarai)"],
            "sa": ["पद्म (Padma)", "कमल (Kamala)"]
        },
        "category": "aquatic",
        "growth_type": "aquatic_herb",
        "habitat": "Shallow freshwater ponds, temple water tanks, marshes, and slow river deltas",
        "flowering_season": "April to October",
        "description": "The National Flower of India: a majestic aquatic perennial with massive circular peltate leaves held high above water on spiny petioles and magnificent solitary pink or white blossoms.",
        "distinguishing_characteristics": "Leaves are strictly peltate and held ABOVE the water surface (not floating on surface); water beads up due to microscopic superhydrophobic wax nanostructures (Lotus Effect); distinctive conical perforated seed receptacle in flower center.",
        "safety_notes": "All parts (seeds, rhizomes/kamal kakdi, young petals) are edible and non-toxic when grown in unpolluted water. Accumulates heavy metals in polluted waterways.",
        "confusable_species": [
            "Nymphaea nouchali (Water Lily) - leaves float directly flat ON the water surface with a deep radial V-shaped slit; lacks conical central seed receptacle"
        ]
    },
    {
        "id": "nymphaea-nouchali",
        "scientific_name": "Nymphaea nouchali Burm.f.",
        "canonical_name": "Nymphaea nouchali",
        "family": "Nymphaeaceae",
        "genus": "Nymphaea",
        "species": "nouchali",
        "synonyms": ["Nymphaea stellata Willd."],
        "common_names": ["Blue Water Lily", "Star Lotus", "Neelkamal", "Shaluk"],
        "regional_names": {
            "hi": ["नीलकमल (Neelkamal)", "कुमुद (Kumud)"],
            "bn": ["শাপলা (Shapla)", "শালুক (Shaluk)"],
            "ta": ["நீலாம்பல் (Neelambal)"]
        },
        "category": "aquatic",
        "growth_type": "aquatic_herb",
        "habitat": "Quiet freshwater lakes, village ponds, irrigation tanks across Bengal and South India",
        "flowering_season": "July to November",
        "description": "The National Flower of Bangladesh: an aquatic perennial herb with rounded floating leaves and star-shaped white, blue, or violet blossoms floating directly on or just above the water surface.",
        "distinguishing_characteristics": "Leaves float directly on water surface with a distinct radial slit from margin to petiole center; sharply pointed starry petals (blue, white, or violet) surrounding yellow stamens; lacks conical seed receptacle.",
        "safety_notes": "Stems and tubers (shaluk) are traditionally cooked in Bengal. Some wild Nymphaea alkaloids are mildly psychoactive in concentrated doses; avoid raw ingestion.",
        "confusable_species": [
            "Nelumbo nucifera (Sacred Lotus) - leaves are circular without slit and held well above water surface on prickly stalks",
            "Nymphoides hydrophylla - much smaller white flowers with feathery petals"
        ]
    },
    {
        "id": "helianthus-annuus",
        "scientific_name": "Helianthus annuus L.",
        "canonical_name": "Helianthus annuus",
        "family": "Asteraceae",
        "genus": "Helianthus",
        "species": "annuus",
        "synonyms": [],
        "common_names": ["Common Sunflower", "Sunflower", "Surajmukhi"],
        "regional_names": {
            "hi": ["सूरजमुखी (Surajmukhi)"],
            "bn": ["সূর্যমুখী (Surjamukhi)"],
            "ta": ["சூரியகாந்தி (Suriyakanthi)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Open sunny agricultural fields, cultivated widely across Maharashtra, Karnataka, and Punjab",
        "flowering_season": "June to September (summer/monsoon crop)",
        "description": "A tall coarse annual herb reaching 1.5–3.5 m with rough bristly stems, massive cordate leaves, and iconic golden-yellow radiating composite flowerheads that track the sun when young (heliotropism).",
        "distinguishing_characteristics": "Coarse hispid bristly thick stem; broad cordate rough leaves with dentate margins; immense composite capitulum (10–30 cm across) with golden-yellow ray florets and dark central disc florets arranged in Fibonacci spirals.",
        "safety_notes": "Seeds and oil are highly nutritious and safe. Rough stem hairs can cause mild skin irritation on prolonged contact.",
        "confusable_species": [
            "Tithonia diversifolia (Mexican sunflower) - perennial shrub with deeply 3–5 lobed leaves",
            "Helianthus tuberosus (Jerusalem artichoke) - perennial producing edible underground tubers"
        ]
    },
    {
        "id": "bougainvillea-spectabilis",
        "scientific_name": "Bougainvillea spectabilis Willd.",
        "canonical_name": "Bougainvillea spectabilis",
        "family": "Nyctaginaceae",
        "genus": "Bougainvillea",
        "species": "spectabilis",
        "synonyms": [],
        "common_names": ["Bougainvillea", "Great Bougainvillea", "Paper Flower"],
        "regional_names": {
            "hi": ["बोगनवेलिया (Bougainvillea)", "कागज़ी फूल (Kagazi Phool)"],
            "bn": ["কাগজ ফুল (Kagoj Phul)", "বাগানবিলাস (Baganbilash)"],
            "ta": ["காகிதப்பூ (Kagitha Poo)"]
        },
        "category": "flower",
        "growth_type": "climber",
        "habitat": "Sunny compound walls, urban roadsides, garden arches throughout India and the tropics",
        "flowering_season": "November to May",
        "description": "A vigorous thorny woody evergreen climbing shrub famous for its vibrant paper-like floral bracts in magenta, purple, red, pink, orange, and white.",
        "distinguishing_characteristics": "Woody stems armed with sharp recurved spines (thorns); dull green ovate leaves; true flower is tiny, white, and tubular, surrounded by 3 large, papery, brightly colored persistent petaloid bracts.",
        "safety_notes": "Sharp thorns can inflict puncture wounds. Sap can cause mild skin dermatitis in sensitive people; non-edible.",
        "confusable_species": [
            "Bougainvillea glabra (Lesser bougainvillea) - hairless stems, lighter green leaves, more purplish bracts",
            "Quisqualis indica (Madhu Malati) - unarmed climber with tubular fragrant white-to-red flowers without papery bracts"
        ]
    },
    {
        "id": "catharanthus-roseus",
        "scientific_name": "Catharanthus roseus (L.) G.Don",
        "canonical_name": "Catharanthus roseus",
        "family": "Apocynaceae",
        "genus": "Catharanthus",
        "species": "roseus",
        "synonyms": ["Vinca rosea L.", "Lochnera rosea (L.) Rchb."],
        "common_names": ["Madagascar Periwinkle", "Rosy Periwinkle", "Sadabahar", "Nayantara"],
        "regional_names": {
            "hi": ["सदाबहार (Sadabahar)", "सदाफूली (Sadafhuli)"],
            "bn": ["নয়নতারা (Nayantara)"],
            "ta": ["நித்திய கல்யாணி (Nithya Kalyani)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Dry sandy soils, roadsides, disturbed wastelands, and cultivated ornamental borders",
        "flowering_season": "Year-round (hence the name 'Sadabahar')",
        "description": "A hardy evergreen subshrub 30–80 cm high with glossy opposite leaves and salverform pink, rose, or pure white blossoms with dark pink eyes.",
        "distinguishing_characteristics": "Opposite glossy oval leaves with pale central midrib; clear/watery sap; salverform 5-lobed flat flowers with slender basal tube; pair of narrow cylindrical folicle fruits.",
        "safety_notes": "Extremely toxic if consumed raw: source of potent chemotherapy alkaloids (vincristine, vinblastine). Can cause severe hypotension and organ failure if ingested.",
        "confusable_species": [
            "Vinca minor (Lesser periwinkle) - temperate trailing groundcover with solitary blue flowers",
            "Impatiens walleriana (Balsam) - succulent watery stems with alternate leaves and spurred flowers"
        ]
    },
    {
        "id": "plumeria-rubra",
        "scientific_name": "Plumeria rubra L.",
        "canonical_name": "Plumeria rubra",
        "family": "Apocynaceae",
        "genus": "Plumeria",
        "species": "rubra",
        "synonyms": ["Plumeria acutifolia Poir."],
        "common_names": ["Frangipani", "Red Frangipani", "Temple Tree", "Champa"],
        "regional_names": {
            "hi": ["चंपा (Champa)", "लाल चंपा (Lal Champa)"],
            "bn": ["কাঠগোলাপ (Kathgolap)", "গোলাঞ্চ (Golancha)"],
            "ta": ["செண்பகம் (Shenbagam)", "பெருங்கள்ளி (Perunkalli)"]
        },
        "category": "flower",
        "growth_type": "tree",
        "habitat": "Temple premises, cemeteries, parks, coastal avenues throughout tropical Asia",
        "flowering_season": "April to October",
        "description": "A small deciduous succulent-stemmed tree 4–8 m tall with swollen fleshy branches, milky sap, and famously fragrant 5-petaled flowers.",
        "distinguishing_characteristics": "Thick sausage-like fleshy blunt branches with prominent leaf scars; copious white latex sap; large obovate pointed leaves clustered at branch tips with prominent parallel secondary veins; intensely fragrant spiral 5-petaled flowers (pink, yellow-white, or red).",
        "safety_notes": "White milky latex sap is an irritant to skin and eyes and toxic if swallowed.",
        "confusable_species": [
            "Plumeria obtusa (White Frangipani) - blunt rounded glossy evergreen leaves and pure white petals with yellow center",
            "Michelia champaca (Swarna Champa) - true timber tree with alternate leaves and golden-orange scented petals"
        ]
    },
    {
        "id": "nyctanthes-arbor-tristis",
        "scientific_name": "Nyctanthes arbor-tristis L.",
        "canonical_name": "Nyctanthes arbor-tristis",
        "family": "Oleaceae",
        "genus": "Nyctanthes",
        "species": "arbor-tristis",
        "synonyms": [],
        "common_names": ["Night-flowering Jasmine", "Coral Jasmine", "Parijat", "Shiuli"],
        "regional_names": {
            "hi": ["पारिजात (Parijat)", "हरसिंगार (Harsingar)"],
            "bn": ["শিউলি ফুল (Shiuli Phul)", "শেফালী (Shephali)"],
            "ta": ["பவழமல்லி (Pavazhamalli)"]
        },
        "category": "flower",
        "growth_type": "tree",
        "habitat": "Sub-Himalayan tracts, dry deciduous forests, and courtyard gardens across Bengal and north India",
        "flowering_season": "September to November (herald of Durga Puja in Bengal)",
        "description": "A small coarse tree or large shrub 3–10 m high, famous in Indian folklore for fragrant night-blooming flowers with white corolla lobes and a bright orange-coral tube that drop at dawn.",
        "distinguishing_characteristics": "Quadrangular (4-angled) young branchlets; rough scabrous opposite ovate leaves with sandpapery texture; intensely sweet night-blooming flowers with 5–8 snow-white petals and bright orange central tube.",
        "safety_notes": "Flowers and leaves are non-toxic; leaves have traditional anti-arthritic usage. Seeds and root bark should not be ingested in excess.",
        "confusable_species": [
            "Jasminum sambac (Mogra) - smooth leaves, white corolla tube without orange center",
            "Clerodendrum chinense - large cabbage-like round heads of double pink-white flowers"
        ]
    },
    {
        "id": "tabernaemontana-divaricata",
        "scientific_name": "Tabernaemontana divaricata (L.) R.Br. ex Roem. & Schult.",
        "canonical_name": "Tabernaemontana divaricata",
        "family": "Apocynaceae",
        "genus": "Tabernaemontana",
        "species": "divaricata",
        "synonyms": ["Ervatamia coronaria (Jacq.) Stapf"],
        "common_names": ["Crape Jasmine", "Pinwheel Flower", "Chandni", "East Indian Rosebay"],
        "regional_names": {
            "hi": ["चांदनी (Chandni)", "तगर (Tagar)"],
            "bn": ["টগর ফুল (Tagar Phul)"],
            "ta": ["நந்தியாவட்டை (Nandiyavattai)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Widely planted garden shrub across homes and parks throughout the Indian subcontinent",
        "flowering_season": "Year-round, peaking in monsoon and summer",
        "description": "A handsome evergreen shrub 1.5–2.5 m tall with glossy dark green leaves, abundant milky latex, and pure white pinwheel-shaped or ruffled double blossoms.",
        "distinguishing_characteristics": "Copious milky latex upon snapping stems; opposite glossy deep-green elliptic leaves with undulating margins; pure white scentless (or faintly scented at night) flowers with 5 pinwheel-twisted lobes or full double carnation-like heads.",
        "safety_notes": "Milky latex is toxic if ingested and irritating to eyes. Not related to true jasmine.",
        "confusable_species": [
            "Jasminum sambac (Mogra) - lacks milky sap, flowers are intensely sweet-scented",
            "Gardenia jasminoides - intensely scented waxy white flowers with distinct ribbed calyx"
        ]
    },
    {
        "id": "clitoria-ternatea",
        "scientific_name": "Clitoria ternatea L.",
        "canonical_name": "Clitoria ternatea",
        "family": "Fabaceae",
        "genus": "Clitoria",
        "species": "ternatea",
        "synonyms": [],
        "common_names": ["Butterfly Pea", "Blue Pea", "Aparajita", "Shankhupushpi"],
        "regional_names": {
            "hi": ["अपराजिता (Aparajita)", "विष्णुकांता (Vishnukanta)"],
            "bn": ["অপরাজিতা (Aparajita)"],
            "ta": ["சங்குப்பூ (Sangu Poo)"]
        },
        "category": "flower",
        "growth_type": "climber",
        "habitat": "Tropical scrub, fences, hedges, domestic gardens across India",
        "flowering_season": "July to December",
        "description": "A slender perennial herbaceous twiner producing pinnate leaves and stunning vivid deep-blue solitary pea-like blossoms with a bright yellow-white throat.",
        "distinguishing_characteristics": "Twiner with odd-pinnate leaves bearing 5–7 elliptic leaflets; distinctive inverted butterfly-shaped papilionaceous flower in intense cobalt blue (or white); flat pubescent legume pods.",
        "safety_notes": "Flowers are edible and safe, used worldwide for blue herbal tea (rich in anthocyanins). Roots and seeds are purgative and should not be swallowed raw.",
        "confusable_species": [
            "Vigna unguiculata (Cowpea) - pale yellowish or purple flowers, much longer fleshy bean pods",
            "Centrosema pubescens - dull purple flowers with large standard petal bearing spurs"
        ]
    },
    {
        "id": "calotropis-gigantea",
        "scientific_name": "Calotropis gigantea (L.) W.T.Aiton",
        "canonical_name": "Calotropis gigantea",
        "family": "Apocynaceae",
        "genus": "Calotropis",
        "species": "gigantea",
        "synonyms": ["Asclepias gigantea L."],
        "common_names": ["Crown Flower", "Giant Milkweed", "Madar", "Aak"],
        "regional_names": {
            "hi": ["मदार (Madar)", "आक (Aak)"],
            "bn": ["আকন্দ (Akanda)"],
            "ta": ["எருக்கு (Erukku)"]
        },
        "category": "wild_grass",
        "growth_type": "shrub",
        "habitat": "Dry open wastelands, sandy roadsides, degraded soils, coastal belts across India",
        "flowering_season": "Year-round",
        "description": "A robust large xerophytic shrub 2–4 m tall with thick waxy pale green leaves, profuse milky sap, and crown-like lavender or white flowers used in religious worship.",
        "distinguishing_characteristics": "Opposite sessile leathery obovate-oblong leaves covered in white cottony down when young; copious toxic white latex; waxy 5-lobed flowers with central elevated crown (corona); large inflated curved follicle fruits filled with silky parachute seeds.",
        "safety_notes": "EXTREMELY TOXIC: Milky latex contains dangerous cardiac glycosides (calotropin, uscharin). Sap causes severe corneal damage/blindness if rubbed in eyes; fatal if ingested in quantity.",
        "confusable_species": [
            "Calotropis procera (Small Milkweed) - smaller shrub with erect corolla lobes (not spreading) and darker purple flower tips",
            "Nerium oleander - narrow lanceolate leaves and tubular pink/white flowers"
        ]
    },
    {
        "id": "mirabilis-jalapa",
        "scientific_name": "Mirabilis jalapa L.",
        "canonical_name": "Mirabilis jalapa",
        "family": "Nyctaginaceae",
        "genus": "Mirabilis",
        "species": "jalapa",
        "synonyms": [],
        "common_names": ["Four O'Clock Flower", "Marvel of Peru", "Gul Abbas", "Sandhyamala"],
        "regional_names": {
            "hi": ["गुल अब्बास (Gul Abbas)", "संध्या मालती (Sandhya Malati)"],
            "bn": ["সন্ধ্যামালতী (Sandhyamalati)"],
            "ta": ["அந்திமந்தாரை (Anthimantharai)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Village gardens, waste places, roadsides, readily self-seeding in tropical soils",
        "flowering_season": "July to November",
        "description": "A bushy perennial herb 60–100 cm tall bearing tubular fragrant flowers that open in the late afternoon (around 4 PM) in yellow, magenta, white, and multicolored patterns.",
        "distinguishing_characteristics": "Swollen stem nodes; opposite ovate pointed leaves; trumpet-shaped flowers opening late afternoon and closing by morning; black spherical wrinkled seed resembling a miniature hand grenade.",
        "safety_notes": "Roots and seeds are toxic and have strong purgative effects. Keep seeds away from small children and pets.",
        "confusable_species": [
            "Catharanthus roseus - flat 5-lobed flowers that remain open all day",
            "Petunia x atkinsiana - sticky hairy foliage and wide trumpet flowers"
        ]
    },
    {
        "id": "canna-indica",
        "scientific_name": "Canna indica L.",
        "canonical_name": "Canna indica",
        "family": "Cannaceae",
        "genus": "Canna",
        "species": "indica",
        "synonyms": [],
        "common_names": ["Indian Shot", "Canna Lily", "Keli"],
        "regional_names": {
            "hi": ["केली (Keli)", "सर्वजय (Sarvajjaya)"],
            "bn": ["সর্বজয়া (Sarbajaya)"],
            "ta": ["கல்வாழை (Kalvazhai)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Wet ditches, garden borders, river banks, and tropical landscape beds",
        "flowering_season": "May to November",
        "description": "A robust perennial herb 1–2 m tall growing from thick rhizomes, with paddle-shaped leaves and showy asymmetric red, orange, or yellow flowers.",
        "distinguishing_characteristics": "Large broad banana-like oblong-elliptic leaves; asymmetric flowers with brightly colored petaloid staminodes (modified stamens acting as petals); warty round capsules containing hard shot-like spherical black seeds.",
        "safety_notes": "Non-toxic. Tubers are rich in edible starch (used like arrowroot).",
        "confusable_species": [
            "Musa paradisiaca (Banana) - massive leaves with distinct trunk-like pseudostem and large pendulous flower bud",
            "Heliconia psittacorum - distinct claw-shaped stiff leathery bracts"
        ]
    },
    {
        "id": "crossandra-infundibuliformis",
        "scientific_name": "Crossandra infundibuliformis (L.) Nees",
        "canonical_name": "Crossandra infundibuliformis",
        "family": "Acanthaceae",
        "genus": "Crossandra",
        "species": "infundibuliformis",
        "synonyms": ["Justicia infundibuliformis L."],
        "common_names": ["Firecracker Flower", "Crossandra", "Kanakambaram"],
        "regional_names": {
            "hi": ["क्रासैंड्रा (Crossandra)", "अबोली (Aboli)"],
            "bn": ["ক্রসান্ড্রা (Crossandra)"],
            "ta": ["கனகாம்பரம் (Kanakambaram)"],
            "te": ["కనకాంబరం (Kanakambaram)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Cultivated widely in southern India as a key traditional hair garland flower",
        "flowering_season": "Year-round, peaking in summer and monsoon",
        "description": "A compact evergreen subshrub 40–90 cm tall with glossy dark green leaves and 4-sided flower spikes yielding vibrant salmon-orange or apricot-coral blossoms.",
        "distinguishing_characteristics": "Whorled or opposite glossy deep-green ovate-elliptic leaves with undulating edges; 4-angled square terminal spike; asymmetric fan-shaped 3–5 lobed corolla in bright apricot-orange; seed capsules explode with a pop in water (firecracker).",
        "safety_notes": "Non-toxic garland flower. Not typically consumed as food.",
        "confusable_species": [
            "Justicia brandegeeana (Shrimp plant) - overlapping reddish bracts resembling shrimp tails",
            "Ixora coccinea - dense spherical clusters of 4-petaled tubular scarlet flowers"
        ]
    },
    {
        "id": "ixora-coccinea",
        "scientific_name": "Ixora coccinea L.",
        "canonical_name": "Ixora coccinea",
        "family": "Rubiaceae",
        "genus": "Ixora",
        "species": "coccinea",
        "synonyms": [],
        "common_names": ["Jungle Flame", "Flame of the Woods", "Rangan", "Rugmini"],
        "regional_names": {
            "hi": ["रुक्मिणी (Rukmini)", "रंगन (Rangan)"],
            "bn": ["রঙ্গন ফুল (Rangan Phul)"],
            "ta": ["இட்லிப்பூ (Idli Poo)", "வெட்சி (Vetchi)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Moist tropical scrub forests of the Western Ghats and coastal gardens across India",
        "flowering_season": "Year-round, heaviest during monsoon",
        "description": "A dense multi-branched evergreen shrub 1–3 m high bearing leathery leaves and spherical ball-like heads of vibrant scarlet-red tubular flowers.",
        "distinguishing_characteristics": "Opposite sessile or sub-sessile glossy leathery oblong-elliptic leaves; dense terminal corymbs packed with numerous small 4-lobed tubular scarlet flowers; paired interpetiolar stipules characteristic of Rubiaceae.",
        "safety_notes": "Non-toxic ornamental. Ripe black berries are consumed in some tribal regions.",
        "confusable_species": [
            "Pentas lanceolata (Egyptian starcluster) - herbaceous hairy plant with 5-pointed star flowers, not 4-lobed",
            "Clerodendrum paniculatum (Pagoda flower) - massive tiered pyramid of orange-red blossoms"
        ]
    },
    {
        "id": "dahlia-pinnata",
        "scientific_name": "Dahlia pinnata Cav.",
        "canonical_name": "Dahlia pinnata",
        "family": "Asteraceae",
        "genus": "Dahlia",
        "species": "pinnata",
        "synonyms": [],
        "common_names": ["Garden Dahlia", "Dahlia"],
        "regional_names": {
            "hi": ["डहलिया (Dahlia)"],
            "bn": ["ডালিয়া (Dahlia)"],
            "ta": ["டேலியா (Dahlia)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Cool winter garden beds and hill station flower shows across India",
        "flowering_season": "December to March in plains; summer in hill stations",
        "description": "A bushy tuberous perennial herb 60–180 cm tall with hollow stems and large spectacular multi-layered flowerheads in virtually every color except pure blue.",
        "distinguishing_characteristics": "Opposite pinnately segmented leaves with ovate serrate leaflets; tuberous root clusters; massive circular composite flowerheads with tiered ray florets forming geometric or pom-pom arrangements.",
        "safety_notes": "Non-toxic to humans; may cause mild digestive upset in dogs and cats.",
        "confusable_species": [
            "Chrysanthemum morifolium - leaves are deeply aromatic and lobed, smaller heads",
            "Zinnia elegans - leaves are rough, sessile and clasping stems"
        ]
    },
    {
        "id": "chrysanthemum-morifolium",
        "scientific_name": "Chrysanthemum morifolium Ramat.",
        "canonical_name": "Chrysanthemum morifolium",
        "family": "Asteraceae",
        "genus": "Chrysanthemum",
        "species": "morifolium",
        "synonyms": ["Dendranthema x grandiflorum (Ramat.) Kitam."],
        "common_names": ["Florist's Chrysanthemum", "Mum", "Guldaudi"],
        "regional_names": {
            "hi": ["गुलदाउदी (Guldaudi)"],
            "bn": ["চন্দ্রমল্লিকা (Chandramallika)"],
            "ta": ["சாமந்தி (Sevanthi)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Winter gardens, pot culture, and commercial flower fields across North India and Bengal",
        "flowering_season": "November to February",
        "description": "An erect aromatic perennial herb 30–90 cm tall famous for its pungent lobed foliage and profuse winter blooms in yellow, bronze, pink, purple, and white.",
        "distinguishing_characteristics": "Alternate deeply lobed serrate leaves with greyish down beneath and distinct strong herbal chrysanthemum scent; dense composite flowerheads ranging from button to spider and incurved forms.",
        "safety_notes": "Foliage contains pyrethrins; contact with plant sap can cause allergic contact dermatitis in gardeners. Toxic to cats and dogs.",
        "confusable_species": [
            "Dahlia pinnata - lacks pungent scent and has tuberous roots",
            "Tagetes erecta (Marigold) - pinnately divided leaves with oil glands and orange/yellow heads"
        ]
    },
    {
        "id": "zinnia-elegans",
        "scientific_name": "Zinnia elegans Jacq.",
        "canonical_name": "Zinnia elegans",
        "family": "Asteraceae",
        "genus": "Zinnia",
        "species": "elegans",
        "synonyms": ["Zinnia violacea Cav."],
        "common_names": ["Common Zinnia", "Youth-and-Age"],
        "regional_names": {
            "hi": ["जीनिया (Zinnia)"],
            "bn": ["জিনিয়া (Zinnia)"],
            "ta": ["ஜின்னியா (Zinnia)"]
        },
        "category": "flower",
        "growth_type": "herb",
        "habitat": "Warm sunny garden borders, monsoon and summer flower beds across India",
        "flowering_season": "June to November",
        "description": "An erect rough-hairy annual herb 30–90 cm tall with stiff stems, opposite clasping leaves, and long-lasting solitary flowerheads in brilliant colors.",
        "distinguishing_characteristics": "Stiff hispid (bristly) stems; opposite sessile ovate leaves clasping the stem without stalks; solitary terminal daisy-like flowerheads with central cone of yellow five-pointed disc florets; petals feel stiff and papery.",
        "safety_notes": "Non-toxic garden flower safe around children and pets.",
        "confusable_species": [
            "Tagetes patula (French marigold) - leaves are finely dissected and pinnate, not simple clasping",
            "Echinacea purpurea (Coneflower) - drooping ray petals with prominent spiny spiky cone"
        ]
    },
    {
        "id": "nerium-oleander",
        "scientific_name": "Nerium oleander L.",
        "canonical_name": "Nerium oleander",
        "family": "Apocynaceae",
        "genus": "Nerium",
        "species": "oleander",
        "synonyms": ["Nerium indicum Mill."],
        "common_names": ["Oleander", "Rosebay", "Kaner", "Karabi"],
        "regional_names": {
            "hi": ["कनेर (Kaner)", "लाल कनेर (Lal Kaner)"],
            "bn": ["করবী (Karabi)"],
            "ta": ["அரளி (Arali)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Highway dividers, arid roadsides, riverbanks, and temple yards across India",
        "flowering_season": "Year-round, peaking April to September",
        "description": "A vigorous upright evergreen shrub 2–5 m tall with narrow leathery leaves in whorls of three and clusters of beautiful rose-pink, red, or white funnel-shaped flowers.",
        "distinguishing_characteristics": "Leaves in distinct whorls of 3, narrow linear-lanceolate (10–20 cm) with prominent pale midrib and fine parallel transverse veins; clear watery or cloudy sap; 5-lobed funnel flowers with fringed corona in throat; long paired cylindrical follicle pods.",
        "safety_notes": "EXTREMELY POISONOUS: Contains lethal cardiac glycosides (oleandrin, neriine). Every part of the plant (leaves, flowers, twigs, sap) is deadly toxic if ingested. Smoke from burning wood is poisonous.",
        "confusable_species": [
            "Cascabela thevetia (Yellow Oleander / Pila Kaner) - bright yellow trumpet flowers and alternate linear leaves",
            "Plumeria rubra (Frangipani) - much thicker succulent blunt branches and wide obovate leaves"
        ]
    },
    {
        "id": "cascabela-thevetia",
        "scientific_name": "Cascabela thevetia (L.) Lippold",
        "canonical_name": "Cascabela thevetia",
        "family": "Apocynaceae",
        "genus": "Cascabela",
        "species": "thevetia",
        "synonyms": ["Thevetia peruviana (Pers.) K.Schum."],
        "common_names": ["Yellow Oleander", "Lucky Nut", "Pila Kaner", "Kolkaphool"],
        "regional_names": {
            "hi": ["पीला कनेर (Peela Kaner)"],
            "bn": ["কলকে ফুল (Kolke Phul)", "পীত করবী (Peet Karabi)"],
            "ta": ["மஞ்சள் அரளி (Manjal Arali)"]
        },
        "category": "flower",
        "growth_type": "shrub",
        "habitat": "Roadsides, village boundaries, temple gardens throughout India",
        "flowering_season": "Year-round",
        "description": "A graceful large shrub or small tree 2–6 m tall with linear glossy green leaves, milky latex sap, and bright yellow funnel-shaped flowers.",
        "distinguishing_characteristics": "Alternate spirally arranged narrow linear-lanceolate glossy leaves (10–15 cm long); copious white milky sap; bell-funnel shaped bright canary-yellow or peach flowers; distinctive rhomboid green drupe fruit containing a hard angular 'lucky nut' stone.",
        "safety_notes": "HIGHLY DANGEROUS / LETHAL: All parts contain thevetin, a potent cardiac poison. Ingestion of seeds is a frequent cause of fatal poisoning; keep away from children.",
        "confusable_species": [
            "Nerium oleander - leaves in whorls of 3 and flowers pink/red/white, not yellow",
            "Allamanda cathartica (Golden trumpet) - climbing shrub with leaves in whorls of 4 and larger trumpet flowers"
        ]
    },
    {
        "id": "passiflora-incarnata",
        "scientific_name": "Passiflora incarnata L.",
        "canonical_name": "Passiflora incarnata",
        "family": "Passifloraceae",
        "genus": "Passiflora",
        "species": "incarnata",
        "synonyms": [],
        "common_names": ["Purple Passionflower", "Maypop", "Passion Flower", "Krishna Kamal"],
        "regional_names": {
            "hi": ["कृष्ण कमल (Krishna Kamal)"],
            "bn": ["ঝুমকো লতা (Jhumko Lata)"],
            "ta": ["ராதா மாதவம் (Radha Madhavam)"]
        },
        "category": "flower",
        "growth_type": "climber",
        "habitat": "Garden trellises, fences, orchards across tropical and subtropical zones",
        "flowering_season": "July to October",
        "description": "A vigorous tendril-climbing perennial vine famous for extraordinary intricate circular blossoms with a corona of radiating thread-like filaments.",
        "distinguishing_characteristics": "Alternate deeply 3-lobed palmately divided leaves with serrated margins and 2 glands on petiole; axillary coiled tendrils; solitary spectacular flowers with 5 petals, 5 sepals, and an intricate circular corona of purple and white wavy filaments surrounding an elevated stalk (androgynophore) bearing 5 stamens and 3 purple stigmas.",
        "safety_notes": "Foliage is traditionally used as a mild calming tea. Unripe green fruits should not be eaten.",
        "confusable_species": [
            "Passiflora edulis (Edible passion fruit) - produces dark purple or yellow round edible fruit with smooth rind",
            "Passiflora foetida (Stinking passionflower) - covered in sticky glandular hairs and surrounded by mossy pinnatifid bracts"
        ]
    },

    # =========================================================================
    # 3. TREES OF INDIA & THE TROPICS (20 Species)
    # =========================================================================
    {
        "id": "ficus-benghalensis",
        "scientific_name": "Ficus benghalensis L.",
        "canonical_name": "Ficus benghalensis",
        "family": "Moraceae",
        "genus": "Ficus",
        "species": "benghalensis",
        "synonyms": [],
        "common_names": ["Banyan Tree", "Indian Banyan", "Bargad", "Bat Gachh"],
        "regional_names": {
            "hi": ["बरगद (Bargad)", "बड़ (Bad)"],
            "bn": ["বট গাছ (Bot Gachh)"],
            "ta": ["ஆலமரம் (Aalamaram)"],
            "sa": ["वट (Vata)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Throughout the Indian subcontinent; village squares, roadside avenues, ancient temples",
        "flowering_season": "Syconia (figs) ripen February to May",
        "description": "The National Tree of India: an enormous sprawling evergreen banyan tree famous for massive aerial prop roots that grow downward from horizontal branches into the ground to form secondary trunks.",
        "distinguishing_characteristics": "Massive spreading canopy supported by woody columnar aerial roots; milky latex sap in all tissues; alternate thick leathery ovate leaves (10–20 cm) with rounded base and 5–7 basal veins; paired sessile scarlet-red spherical figs (1.5–2 cm) in leaf axils.",
        "safety_notes": "Non-toxic sacred tree. Figs are eaten by birds, bats, and monkeys. Milky sap may mildly irritate sensitive eyes.",
        "confusable_species": [
            "Ficus religiosa (Peepal) - leaves have long slender tail-like drip tip and NO aerial prop roots",
            "Ficus elastica (Rubber tree) - thicker shiny oblong leaves and reddish stipular sheath"
        ]
    },
    {
        "id": "ficus-religiosa",
        "scientific_name": "Ficus religiosa L.",
        "canonical_name": "Ficus religiosa",
        "family": "Moraceae",
        "genus": "Ficus",
        "species": "religiosa",
        "synonyms": [],
        "common_names": ["Sacred Fig", "Peepal Tree", "Bodhi Tree", "Ashwattha"],
        "regional_names": {
            "hi": ["पीपल (Peepal)"],
            "bn": ["অশ্বত্থ (Aswattha)", "পিপল (Pipal)"],
            "ta": ["அரச மரம் (Arasa Maram)"],
            "sa": ["अश्वत्थ (Ashvattha)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Ancient temples, roadsides, brick walls, rocky outcrops throughout South Asia",
        "flowering_season": "Figs ripen April to June",
        "description": "A sacred deciduous to semi-evergreen tree revered in Hinduism and Buddhism (the tree under which Siddhartha Gautama attained enlightenment), known for its rustling heart-shaped leaves.",
        "distinguishing_characteristics": "Distinctive cordate (heart-shaped) leaves with an exceptionally long, slender tail-like drip tip (2–5 cm); long slender petiole causing leaves to flutter and rustle in the slightest breeze; purplish-black small sessile figs in axillary pairs; lacks pillar-like aerial prop roots.",
        "safety_notes": "Non-toxic sacred tree. Can be destructive to masonry and building foundations when seeds germinate in brickwork.",
        "confusable_species": [
            "Ficus benghalensis (Banyan) - lacks elongated tail-like drip tip, possesses prominent aerial roots",
            "Thespesia populnea (Portia tree) - yellow hibiscus-like flowers, leaves lack long tail"
        ]
    },
    {
        "id": "delonix-regia",
        "scientific_name": "Delonix regia (Bojer ex Hook.) Raf.",
        "canonical_name": "Delonix regia",
        "family": "Fabaceae",
        "genus": "Delonix",
        "species": "regia",
        "synonyms": ["Poinciana regia Bojer"],
        "common_names": ["Gulmohar", "Royal Poinciana", "Flamboyant", "Flame Tree"],
        "regional_names": {
            "hi": ["गुलमोहर (Gulmohar)"],
            "bn": ["কৃষ্ণচূড়া (Krishnachura)"],
            "ta": ["செம்மயிற்கொன்றை (Semmayirkondrai)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Avenue trees in tropical cities, parks, university campuses across India",
        "flowering_season": "April to June (peak summer spectacle)",
        "description": "A magnificent wide-spreading umbrella-canopied tree 10–15 m high, blanketed in early summer by breathtaking masses of fiery scarlet-orange orchid-like flowers.",
        "distinguishing_characteristics": "Wide spreading umbrella-shaped flat-topped crown; feathery light-green bipinnate leaves with thousands of tiny leaflets (resembling fern foliage); massive scarlet-red 5-petaled flowers with one white/yellow-streaked standard petal; enormous woody brown flat seed pods up to 60 cm long.",
        "safety_notes": "Non-toxic avenue tree. Pods and seeds are not consumed.",
        "confusable_species": [
            "Caesalpinia pulcherrima (Peacock flower / Chhota Gulmohar) - small garden shrub under 3 m with long exerted stamens",
            "Peltophorum pterocarpum (Yellow Gulmohar / Copperpod) - bright yellow flowers and rusty-copper pods"
        ]
    },
    {
        "id": "tectona-grandis",
        "scientific_name": "Tectona grandis L.f.",
        "canonical_name": "Tectona grandis",
        "family": "Lamiaceae",
        "genus": "Tectona",
        "species": "grandis",
        "synonyms": [],
        "common_names": ["Teak", "Sagwan", "Teakwood Tree"],
        "regional_names": {
            "hi": ["सागवान (Sagwan)", "सागौन (Sagaun)"],
            "bn": ["সেগুন গাছ (Segun Gachh)"],
            "ta": ["தேக்கு (Thekku)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Deciduous timber forests of central and southern India (Madhya Pradesh, Maharashtra, Kerala)",
        "flowering_season": "June to August",
        "description": "One of the world's premier hardwood timber trees, reaching 30–40 meters with massive rough elliptic leaves and vast airy panicles of tiny white flowers.",
        "distinguishing_characteristics": "Immense opposite ovate-elliptic leaves (30–60 cm long, sometimes 1 m on saplings) with sandpaper-like rough upper surface and hairy underside; quadrangular branchlets; crushed fresh leaves yield red juice; huge branched airy panicles of tiny white blossoms.",
        "safety_notes": "Valuable non-toxic timber tree. Rough leaves can feel coarse on skin.",
        "confusable_species": [
            "Shorea robusta (Sal) - alternate glossy oblong leaves, not giant opposite sandpapery leaves",
            "Gmelina arborea (Gamhar) - heart-shaped leaves with yellow-brown flowers"
        ]
    },
    {
        "id": "shorea-robusta",
        "scientific_name": "Shorea robusta Gaertn.",
        "canonical_name": "Shorea robusta",
        "family": "Dipterocarpaceae",
        "genus": "Shorea",
        "species": "robusta",
        "synonyms": [],
        "common_names": ["Sal Tree", "Shala", "Sakhu"],
        "regional_names": {
            "hi": ["साल (Sal)", "साखू (Sakhu)"],
            "bn": ["শাল গাছ (Shal Gachh)"],
            "ta": ["குங்கிலியம் (Kungiliyam)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Sub-Himalayan belt, Chota Nagpur plateau, central and eastern India (Jharkhand, Odisha, Bengal)",
        "flowering_season": "March to April",
        "description": "A dominant forest canopy tree 25–35 m tall with tall straight cylindrical bole, dark reddish-brown deeply furrowed bark, and valuable heavy hardwood timber.",
        "distinguishing_characteristics": "Tall straight unbranched lower trunk; alternate tough leathery ovate-oblong leaves (10–25 cm long) with shiny upper surface and prominent lateral veins; small whitish-yellow flowers in racemes; winged fruit (5 unequal persistent calyx wings) that spins down like a shuttlecock.",
        "safety_notes": "Non-toxic timber and resin-producing tree (yields dammar/sal resin). Leaves are traditionally stitched into eco-friendly dining plates (pattal).",
        "confusable_species": [
            "Tectona grandis (Teak) - opposite giant leaves and square branchlets",
            "Terminalia tomentosa (Asan / Indian Laurel) - bark has 'crocodile skin' checkered texture"
        ]
    },
    {
        "id": "moringa-oleifera",
        "scientific_name": "Moringa oleifera Lam.",
        "canonical_name": "Moringa oleifera",
        "family": "Moringaceae",
        "genus": "Moringa",
        "species": "oleifera",
        "synonyms": [],
        "common_names": ["Moringa", "Drumstick Tree", "Horseradish Tree", "Sahjan"],
        "regional_names": {
            "hi": ["सहजन (Sahjan)", "मुनगा (Munga)"],
            "bn": ["সজিনা (Sojina)", "সজনে ডাঁটা (Sojne Data)"],
            "ta": ["முருங்கை (Murungai)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Cultivated across backyard gardens and arid farms throughout India",
        "flowering_season": "December to April",
        "description": "A fast-growing drought-tolerant tree 8–12 m high with soft brittle wood, tripinnate feathery leaves, and highly nutritious long ribbed pendulous seed pods.",
        "distinguishing_characteristics": "Tripinnate (3-times divided) feathery foliage with tiny round-obovate leaflets; fragrant yellowish-white 5-petaled flowers; long pendulous 3-angled ribbed seed pods (drumsticks, 30–60 cm long); roots smell sharply of horseradish.",
        "safety_notes": "Leaves, flowers, and immature pods are exceptionally nutritious superfoods. Tree root bark contains moringinine and should not be eaten in large quantities (uterine stimulant).",
        "confusable_species": [
            "Sesbania grandiflora (Agathi) - simply pinnate leaves and much larger fleshy white/red blossoms",
            "Melia azedarach - bipinnate leaves with poisonous spherical yellow drupes"
        ]
    },
    {
        "id": "terminalia-arjuna",
        "scientific_name": "Terminalia arjuna (Roxb. ex DC.) Wight & Arn.",
        "canonical_name": "Terminalia arjuna",
        "family": "Combretaceae",
        "genus": "Terminalia",
        "species": "arjuna",
        "synonyms": [],
        "common_names": ["Arjun Tree", "Arjuna", "White Murdah"],
        "regional_names": {
            "hi": ["अर्जुन (Arjun)"],
            "bn": ["অর্জুন গাছ (Arjun Gachh)"],
            "ta": ["மருத மரம் (Marutha Maram)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Riverbanks, streamsides, alluvial valleys throughout the central and southern Indian peninsula",
        "flowering_season": "April to July",
        "description": "A massive buttressed riverine tree 20–25 m tall with distinctive smooth pinkish-grey peeling bark celebrated in Ayurvedic cardiology.",
        "distinguishing_characteristics": "Exceptionally smooth pinkish-white to pale grey bark that flakes off in large flat sheets; sub-opposite oblong leaves with 2 glands at base of petiole; small pale yellow sessile flowers; distinctive woody 5-winged fibrous fruit (drupe).",
        "safety_notes": "Bark is a renowned Ayurvedic cardioprotective tonic. Non-toxic in standard therapeutic decoctions.",
        "confusable_species": [
            "Terminalia tomentosa (Asan) - deeply fissured black checkered bark (like crocodile hide)",
            "Eucalyptus globulus - smooth peeling bark but foliage has distinct cineole oil scent and sickled leaves"
        ]
    },
    {
        "id": "saraca-asoca",
        "scientific_name": "Saraca asoca (Roxb.) Willd.",
        "canonical_name": "Saraca asoca",
        "family": "Fabaceae",
        "genus": "Saraca",
        "species": "asoca",
        "synonyms": ["Saraca indica sensu auct."],
        "common_names": ["Sita Ashok", "True Ashoka Tree", "Ashoka"],
        "regional_names": {
            "hi": ["अशोक (Ashok)", "सीता अशोक (Sita Ashok)"],
            "bn": ["অশোক গাছ (Ashok Gachh)"],
            "ta": ["அசோக மரம் (Asoka Maram)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Humid evergreen forests of the Western Ghats and eastern Himalayas; temple groves",
        "flowering_season": "February to April",
        "description": "The sacred mythological Ashoka tree: a medium evergreen tree 7–10 m tall with dense deep green crown, drooping coppery-red young leaves, and spectacular fragrant orange-scarlet floral bunches.",
        "distinguishing_characteristics": "Pinnate leaves with 4–6 pairs of lanceolate leaflets; young flaccid leaves hang limp in delicate coppery-pink tassels; dense fragrant corymbs of flowers that open orange-yellow and turn scarlet-red; flat leathery pods.",
        "safety_notes": "Bark is celebrated in traditional gynecological medicine. Non-toxic sacred tree.",
        "confusable_species": [
            "Polyalthia longifolia (False Ashoka / Mast tree) - ubiquitous upright mast-like cemetery tree with wavy simple leaves and greenish-white flowers (frequently misidentified by the public as Ashok)"
        ]
    },
    {
        "id": "polyalthia-longifolia",
        "scientific_name": "Monoon longifolium (Sonn.) B.Xue & R.M.K.Saunders",
        "canonical_name": "Polyalthia longifolia",
        "family": "Annonaceae",
        "genus": "Polyalthia",
        "species": "longifolia",
        "synonyms": ["Polyalthia longifolia (Sonn.) Thwaites"],
        "common_names": ["False Ashoka", "Mast Tree", "Cemetery Tree", "Indian Fir"],
        "regional_names": {
            "hi": ["अशोक (Ashok - colloquial)", "देवदार (Debdaru)"],
            "bn": ["দেবদারু (Debdaru)"],
            "ta": ["நெட்டிலிங்கம் (Nettilingam)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Urban avenues, campus boundary lines, noise buffers throughout tropical India",
        "flowering_season": "March to May",
        "description": "A very tall slender pyramidal or columnar evergreen tree reaching 15–20 m, universally planted along Indian roadsides as windbreak and visual screen.",
        "distinguishing_characteristics": "Columnar mast-like pencil habit (in var. pendula) with drooping short branches; alternate lanceolate glossy dark-green leaves with distinctly wavy (undulating) margins; star-like pale green flowers; clusters of small black oval fruits.",
        "safety_notes": "Non-toxic avenue tree. Widely misnamed as 'Ashoka' in common parlance, but completely unrelated to true Saraca asoca.",
        "confusable_species": [
            "Saraca asoca (True Ashoka) - rounded spreading canopy with pinnate compound leaves and brilliant orange-red flower trusses"
        ]
    },
    {
        "id": "santalu-album",
        "scientific_name": "Santalum album L.",
        "canonical_name": "Santalum album",
        "family": "Santalaceae",
        "genus": "Santalum",
        "species": "album",
        "synonyms": [],
        "common_names": ["Indian Sandalwood", "White Sandalwood", "Chandan"],
        "regional_names": {
            "hi": ["चंदन (Chandan)", "श्वेत चंदन (Shwet Chandan)"],
            "bn": ["চন্দন (Chandan)"],
            "ta": ["சந்தன மரம் (Santhanam)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Dry deciduous scrub forests of Karnataka, Tamil Nadu, and Kerala; semi-parasitic on host roots",
        "flowering_season": "March to April and August to September",
        "description": "A small to medium hemiparasitic evergreen tree 4–10 m high, famous worldwide for its precious fragrant golden-brown heartwood and essential oil.",
        "distinguishing_characteristics": "Hemiparasitic roots with haustoria attaching to neighbor plants; opposite thin glabrous elliptic-lanceolate leaves with shiny upper face and pale underside; small unscented flowers turning from straw-yellow to deep red-purple; fragrant heartwood.",
        "safety_notes": "Heartwood paste is safe topically. Highly regulated protected species under Indian forest law.",
        "confusable_species": [
            "Pterocarpus santalinus (Red Sandalwood) - alternate trifoliate leaves, non-fragrant dark blood-red timber",
            "Wrightia tinctoria (Ivory tree / Pala) - opposite leaves with white star flowers and long pendulous pods"
        ]
    },
    {
        "id": "neolamarckia-cadamba",
        "scientific_name": "Neolamarckia cadamba (Roxb.) Bosser",
        "canonical_name": "Neolamarckia cadamba",
        "family": "Rubiaceae",
        "genus": "Neolamarckia",
        "species": "cadamba",
        "synonyms": ["Anthocephalus cadamba (Roxb.) Miq."],
        "common_names": ["Kadam", "Kadamba", "Burflower Tree"],
        "regional_names": {
            "hi": ["कदम (Kadam)", "कदंब (Kadamba)"],
            "bn": ["কদম গাছ (Kadam Gachh)"],
            "ta": ["கடம்பு (Kadambu)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Alluvial moist plains, streamsides, village courtyards across Bengal, Assam, and South India",
        "flowering_season": "June to August (peak monsoon celebration)",
        "description": "A majestic fast-growing evergreen tree 15–30 m tall with broad spreading horizontal branches and magical spherical golden-orange flower balls that perfume the monsoon air.",
        "distinguishing_characteristics": "Large opposite glossy ovate-elliptic leaves (15–30 cm long) with prominent pinkish-green veins; iconic dense spherical globular flowerheads (like scented orange ping-pong balls) with projecting white stigmas; horizontal tiered branching.",
        "safety_notes": "Non-toxic sacred tree celebrated in Krishna mythology. Ripe fruit is pleasantly acidic and eaten by wildlife and cattle.",
        "confusable_species": [
            "Mitragyna parvifolia (Kaim) - much smaller pale yellow-white flower balls and smaller leaves",
            "Tectona grandis (Teak) - leaves are sandpapery, flowers in massive loose panicles"
        ]
    },
    {
        "id": "eucalyptus-globulus",
        "scientific_name": "Eucalyptus globulus Labill.",
        "canonical_name": "Eucalyptus globulus",
        "family": "Myrtaceae",
        "genus": "Eucalyptus",
        "species": "globulus",
        "synonyms": [],
        "common_names": ["Blue Gum", "Tasmanian Blue Gum", "Eucalyptus", "Nilgiri Tree"],
        "regional_names": {
            "hi": ["यूकेलिप्टस (Eucalyptus)", "नीलगिरी (Nilgiri)"],
            "bn": ["ইউক্যালিপটাস (Eucalyptus)"],
            "ta": ["நீலகிரி மரம் (Neelagiri Maram)"]
        },
        "category": "tree",
        "growth_type": "tree",
        "habitat": "Plantations across Punjab, Haryana, Nilgiri hills, and forestry plantations across India",
        "flowering_season": "September to December",
        "description": "A gigantic fast-growing aromatic evergreen tree reaching 30–55 m with peeling ribbon-like bark and sickle-shaped blue-grey leaves that smell intensely of cineole/eucalyptol.",
        "distinguishing_characteristics": "Tall pale trunk with smooth peeling ribbons of bark; alternate pendulous sickle-shaped (falcate) leathery leaves with strong medicinal eucalyptus scent when crushed; woody warty topshaped fruit capsules with prominent 4-lobed valves.",
        "safety_notes": "Foliage oil is used for inhalation in congestion. Pure eucalyptus oil is TOXIC if swallowed internally in quantity; keep away from small children.",
        "confusable_species": [
            "Eucalyptus tereticornis (Forest red gum) - common plains species with smooth mottled bark and smaller horn-capped buds",
            "Melaleuca leucadendra (Tea tree) - spongy papery thick bark"
        ]
    },
    {
        "id": "bambusa-vulgaris",
        "scientific_name": "Bambusa vulgaris Schrad. ex J.C.Wendl.",
        "canonical_name": "Bambusa vulgaris",
        "family": "Poaceae",
        "genus": "Bambusa",
        "species": "vulgaris",
        "synonyms": [],
        "common_names": ["Common Bamboo", "Golden Bamboo", "Bans", "Baash"],
        "regional_names": {
            "hi": ["बांस (Bans)"],
            "bn": ["বাঁশ (Baash)"],
            "ta": ["மூங்கில் (Moongil)"]
        },
        "category": "wild_grass",
        "growth_type": "herb",
        "habitat": "Riverbanks, village homesteads, moist tropical forests across Bengal, Assam, and South India",
        "flowering_season": "Extremely rare monocarpic flowering (decades between blooms)",
        "description": "The world's largest grass: an open clump-forming giant bamboo 10–20 m high with thick hollow green or yellow-striped woody culms.",
        "distinguishing_characteristics": "Woody hollow jointed culms (stems) with distinct nodal rings and hairy culm sheaths; dense feathery foliage of linear-lanceolate leaves; rapid vegetative growth via underground pachymorph rhizome network.",
        "safety_notes": "Shoots must be boiled before eating to eliminate naturally occurring cyanogenic glycosides. Stiff culm hairs can irritate skin.",
        "confusable_species": [
            "Dendrocalamus strictus (Solid bamboo / Male bamboo) - solid culms adapted to drier deciduous forests",
            "Arundo donax (Giant reed) - unbranched reed with leaves clasping along entire stem"
        ]
    },

    # =========================================================================
    # 4. FRUIT PLANTS & TREES (18 Species)
    # =========================================================================
    {
        "id": "mangifera-indica",
        "scientific_name": "Mangifera indica L.",
        "canonical_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "genus": "Mangifera",
        "species": "indica",
        "synonyms": [],
        "common_names": ["Mango", "King of Fruits", "Aam"],
        "regional_names": {
            "hi": ["आम (Aam)"],
            "bn": ["আম (Aam)"],
            "ta": ["மாமரம் (Maamaram)"],
            "te": ["మామిడి (Mamidi)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Cultivated across the tropical plains of India, native to northeastern India and Myanmar",
        "flowering_season": "January to March",
        "description": "The National Fruit of India: a large handsome evergreen fruit tree 15–30 m tall with dense dome-shaped canopy and rich sweet summer drupe fruits.",
        "distinguishing_characteristics": "Alternate simple leathery lanceolate-oblong leaves with wavy margins, emerging coppery-purple before turning dark glossy green; large branched terminal panicles of tiny yellowish fragrant flowers; large fleshy oval drupe with sweet pulp and fibrous stone.",
        "safety_notes": "Fruit is universally celebrated and safe. The clear/milky sap from mango stems and peel contains urushiol-like contact allergens that can trigger skin rash around the mouth (mango dermatitis).",
        "confusable_species": [
            "Polyalthia longifolia (False Ashoka) - leaves look similar but tree is tall and narrow with wavy leaves that never smell of turpentine",
            "Anacardium occidentale (Cashew) - obovate rounded leaves and swollen pear-like cashew apple"
        ]
    },
    {
        "id": "psidium-guajava",
        "scientific_name": "Psidium guajava L.",
        "canonical_name": "Psidium guajava",
        "family": "Myrtaceae",
        "genus": "Psidium",
        "species": "guajava",
        "synonyms": [],
        "common_names": ["Guava", "Common Guava", "Amrood", "Peyara"],
        "regional_names": {
            "hi": ["अमरूद (Amrood)"],
            "bn": ["পেয়ারা (Peyara)"],
            "ta": ["கொய்யா (Koyya)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Orchards and home compounds throughout India, especially famous in Prayagraj (Allahabad)",
        "flowering_season": "April to June and September to November",
        "description": "A small evergreen or sub-deciduous tree 3–8 m tall with attractive mottled smooth copper-green bark that peels in thin paper curls.",
        "distinguishing_characteristics": "Very smooth reddish-brown bark that flakes off in thin plates; opposite elliptic-oval leaves with prominent impressed veins on upper side; solitary or clustered white flowers with a central brush of white stamens; round or pear-shaped fruit with sweet/sour white or pink pulp packed with hard seeds.",
        "safety_notes": "Leaves and fruit are completely non-toxic and nutritious (exceptionally high in Vitamin C). Leaves are chewed for oral care.",
        "confusable_species": [
            "Syzygium cumini (Jamun) - larger tree with dark purple berries and non-peeling bark",
            "Punica granatum (Pomegranate) - thorny branches with red flowers and leathery seeded fruit"
        ]
    },
    {
        "id": "musa-acuminata",
        "scientific_name": "Musa acuminata Colla",
        "canonical_name": "Musa acuminata",
        "family": "Musaceae",
        "genus": "Musa",
        "species": "acuminata",
        "synonyms": ["Musa paradisiaca L. (hybrid)"],
        "common_names": ["Banana", "Plantain", "Kela", "Kola"],
        "regional_names": {
            "hi": ["केला (Kela)"],
            "bn": ["কলা গাছ (Kola Gachh)"],
            "ta": ["வாழைமரம் (Vazhaimaram)"]
        },
        "category": "fruit",
        "growth_type": "herb",
        "habitat": "Cultivated across tropical homesteads, river plains, and orchards across South Asia",
        "flowering_season": "Year-round upon maturity (9–12 months)",
        "description": "One of the world's largest giant herbaceous plants (not a true woody tree): produces a fleshy pseudostem 3–7 m high made of tightly overlapping leaf sheaths.",
        "distinguishing_characteristics": "Massive spirally arranged arching leaves (up to 2–3 m long) that shred naturally in wind along lateral veins; large terminal inflorescence with fleshy purple-red bracts opening to reveal tiers (hands) of tubular flowers; pendulous bunch of curved yellow/green fruits.",
        "safety_notes": "All parts (fruit, raw green cooking banana, blossom/mocha, inner stem/thor) are edible and non-toxic.",
        "confusable_species": [
            "Ensete ventricosum (Abyssinian banana) - monocarpic non-suckering giant herb with red-ribbed leaves",
            "Ravenala madagascariensis (Traveller's palm) - leaves arranged in a single flat vertical fan"
        ]
    },
    {
        "id": "carica-papaya",
        "scientific_name": "Carica papaya L.",
        "canonical_name": "Carica papaya",
        "family": "Caricaceae",
        "genus": "Carica",
        "species": "papaya",
        "synonyms": [],
        "common_names": ["Papaya", "Pawpaw", "Papita", "Pepe"],
        "regional_names": {
            "hi": ["पपीता (Papita)"],
            "bn": ["পেঁপে (Pepe)"],
            "ta": ["பப்பாளி (Pappali)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Domestic kitchen gardens, tropical backyards, and commercial orchards across India",
        "flowering_season": "Year-round",
        "description": "A fast-growing sparsely branched tree-like herb 3–10 m tall with hollow soft succulent trunk marked by prominent leaf scars, crowned by an umbrella of massive palmately lobed leaves.",
        "distinguishing_characteristics": "Single unbranched hollow green-grey trunk with conspicuous leaf scars; giant deeply 7-lobed palmate leaves (50–70 cm broad) on long hollow petioles; copious white latex sap; large oblong-globular fruits with orange flesh and central cavity lined with peppery black seeds.",
        "safety_notes": "Ripe fruit is nutritious and safe. Unripe green papaya contains high levels of raw papain latex, which can stimulate uterine contractions and is contraindicated in pregnancy.",
        "confusable_species": [
            "Ricinus communis (Castor bean) - palmate leaves with serrate lobes and spiny fruit capsules containing deadly ricin seeds",
            "Manihot esculenta (Cassava) - woody shrub with deeply parted narrow leaflets"
        ]
    },
    {
        "id": "cocos-nucifera",
        "scientific_name": "Cocos nucifera L.",
        "canonical_name": "Cocos nucifera",
        "family": "Arecaceae",
        "genus": "Cocos",
        "species": "nucifera",
        "synonyms": [],
        "common_names": ["Coconut Palm", "Coconut Tree", "Kalpavriksha", "Nariyal"],
        "regional_names": {
            "hi": ["नारियल (Nariyal)"],
            "bn": ["নারকেল গাছ (Narkel Gachh)"],
            "ta": ["தென்னை மரம் (Thennai Maram)"],
            "ml": ["തെങ്ങ് (Thengu)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Coastal belts, river deltas, and tropical homesteads across southern and eastern India",
        "flowering_season": "Year-round upon maturity",
        "description": "The quintessential tropical palm: a tall solitary unbranched feather palm reaching 20–30 m with curved ringed trunk, crowned by arching feathery pinnate fronds.",
        "distinguishing_characteristics": "Tall ringed trunk swollen at base; magnificent terminal crown of 30–40 arching pinnate fronds (4–6 m long); large woody boat-shaped spathe enclosing branched inflorescence; fibrous oval drupe containing liquid endosperm (coconut water) and white meat.",
        "safety_notes": "Completely non-toxic. Beware of physical hazard from falling heavy coconuts beneath tall palms.",
        "confusable_species": [
            "Borassus flabellifer (Palmyra palm / Taal) - fan-shaped leaves, not pinnate feather fronds",
            "Areca catechu (Areca / Betel palm) - much thinner, perfectly straight slender trunk with smaller orange oval nuts"
        ]
    },
    {
        "id": "citrus-limon",
        "scientific_name": "Citrus limon (L.) Osbeck",
        "canonical_name": "Citrus limon",
        "family": "Rutaceae",
        "genus": "Citrus",
        "species": "limon",
        "synonyms": [],
        "common_names": ["Lemon", "Nimbu", "Kagzi Nimbu", "Lebu"],
        "regional_names": {
            "hi": ["नींबू (Nimbu)", "कागज़ी नींबू (Kagzi Nimbu)"],
            "bn": ["লেবু (Lebu)", "কাগজি লেবু (Kagji Lebu)"],
            "ta": ["எலுமிச்சை (Elumichai)"]
        },
        "category": "fruit",
        "growth_type": "shrub",
        "habitat": "Cultivated across gardens and citrus orchards across Andhra Pradesh, Maharashtra, and Assam",
        "flowering_season": "February to April and August to October",
        "description": "A small spiny evergreen shrub or tree 3–6 m tall bearing fragrant white flowers and juicy acidic oval fruits celebrated for culinary and beverage use.",
        "distinguishing_characteristics": "Stout sharp spines on branchlets; alternate dark green ovate-elliptic leaves with narrowly winged petioles and translucent citrus-oil glands; fragrant 4–5 petaled white flowers with pinkish buds; yellow/green oval hesperidium fruit with nipple-like apex and acidic pulp.",
        "safety_notes": "Safe culinary fruit. Peel oil contains psoralens which can cause mild phytophotodermatitis on skin exposed to bright sunlight.",
        "confusable_species": [
            "Citrus aurantiifolia (Key Lime) - smaller round thin-skinned green fruit with sharp spine tips",
            "Citrus maxima (Pomelo / Batabi Lebu) - massive fruit (15–25 cm) with broadly winged petioles"
        ]
    },
    {
        "id": "punica-granatum",
        "scientific_name": "Punica granatum L.",
        "canonical_name": "Punica granatum",
        "family": "Lythraceae",
        "genus": "Punica",
        "species": "granatum",
        "synonyms": [],
        "common_names": ["Pomegranate", "Anar", "Dalim", "Anaar"],
        "regional_names": {
            "hi": ["अनार (Anar)"],
            "bn": ["ডালিম (Dalim)", "বেদানা (Bedana)"],
            "ta": ["மாதுளை (Mathulai)"]
        },
        "category": "fruit",
        "growth_type": "shrub",
        "habitat": "Semi-arid to subtropical tracts of Maharashtra, Gujarat, Rajasthan, and Mediterranean zones",
        "flowering_season": "April to June",
        "description": "A multi-stemmed deciduous spiny shrub or small tree 3–6 m high bearing brilliant scarlet-orange waxy flowers and ruby-jeweled arillate fruits.",
        "distinguishing_characteristics": "Slender spine-tipped twigs; opposite or clustered small glossy oblong leaves (3–7 cm long); brilliant waxy scarlet-red crinkled flowers with thick leathery calyx; spherical brownish-red fruit crowned by persistent calyx, packed with ruby-red juicy arils around seeds.",
        "safety_notes": "Fruit arils are exceptionally rich in antioxidants and completely safe. Root bark contains pelletierine alkaloids and is toxic in excess.",
        "confusable_species": [
            "Psidium guajava (Guava) - white flowers with brush stamens, non-spiny twigs",
            "Lawsonia inermis (Henna) - tiny cream flowers with non-fleshy capsule fruits"
        ]
    },
    {
        "id": "artocarpus-heterophyllus",
        "scientific_name": "Artocarpus heterophyllus Lam.",
        "canonical_name": "Artocarpus heterophyllus",
        "family": "Moraceae",
        "genus": "Artocarpus",
        "species": "heterophyllus",
        "synonyms": [],
        "common_names": ["Jackfruit", "Kathal", "Kanthal", "Jak"],
        "regional_names": {
            "hi": ["कटहल (Kathal)"],
            "bn": ["কাঁঠাল (Kanthal)"],
            "ta": ["பலாமரம் (Pala Maram)"],
            "ml": ["പ്ലാവ് (Plavu)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Evergreen rainforests of the Western Ghats and homesteads throughout Bengal, Assam, and Kerala",
        "flowering_season": "December to March",
        "description": "The largest tree-borne fruit in the world: a massive evergreen tree 10–20 m high with thick leathery leaves and enormous cauliflorous spiky fruits emerging straight from trunk and main limbs.",
        "distinguishing_characteristics": "Entire dark green obovate leathery leaves with white milky sap; cauliflory: massive green syncarp fruits (up to 30–50 kg) covered in hard conical pyramid points emerging directly from main trunk; sweet aromatic yellow bulbs inside.",
        "safety_notes": "Both raw unripe fruit (vegetable/enchor) and ripe sweet fruit are safe and highly nutritious. Seeds must be cooked before eating. Sticky latex requires oil on hands when cutting.",
        "confusable_species": [
            "Artocarpus lakoocha (Badhal / Dephal) - much smaller velvety irregularly lobed fruit without hard pyramid points",
            "Artocarpus altilis (Breadfruit) - leaves are deeply pinnatifid with large lobes"
        ]
    },
    {
        "id": "syzygium-cumini",
        "scientific_name": "Syzygium cumini (L.) Skeels",
        "canonical_name": "Syzygium cumini",
        "family": "Myrtaceae",
        "genus": "Syzygium",
        "species": "cumini",
        "synonyms": ["Eugenia jambolana Lam."],
        "common_names": ["Jamun", "Black Plum", "Java Plum", "Jambolan"],
        "regional_names": {
            "hi": ["जामुन (Jamun)"],
            "bn": ["জাম (Jaam)"],
            "ta": ["நாவல் பழம் (Naval Pazham)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Along riverbanks, moist deciduous forests, and roadside avenues across India",
        "flowering_season": "March to May",
        "description": "A magnificent large evergreen tree reaching 15–30 m with greyish-white bark, leathery opposite leaves with turpentine scent, and deep purple-black sweet-astringent summer berries.",
        "distinguishing_characteristics": "Smooth grey bark; opposite oblong-elliptic leathery leaves with translucent dots and close parallel veins converging into an intramarginal vein; fragrant greenish-white flowers in clusters; oblong deep-purple berries that stain the tongue violet.",
        "safety_notes": "Fruit is safe, astringent, and famous for helping regulate blood sugar in traditional diets. Seeds are dried and powdered.",
        "confusable_species": [
            "Syzygium jambos (Rose apple) - yellow pear-shaped fruit smelling of roses",
            "Psidium guajava (Guava) - peeling copper bark and hard seeded fruit"
        ]
    },
    {
        "id": "annona-squamosa",
        "scientific_name": "Annona squamosa L.",
        "canonical_name": "Annona squamosa",
        "family": "Annonaceae",
        "genus": "Annona",
        "species": "squamosa",
        "synonyms": [],
        "common_names": ["Sugar Apple", "Sweetsop", "Custard Apple", "Sitaphal"],
        "regional_names": {
            "hi": ["सीताफल (Sitaphal)", "शरीफ़ा (Sharifa)"],
            "bn": ["আতা ফল (Ata Phol)"],
            "ta": ["சீத்தாப்பழம் (Seetha Pazham)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Rocky dry soils, deciduous scrub, and backyard orchards across Deccan plateau and central India",
        "flowering_season": "April to July",
        "description": "A small deciduous to semi-evergreen tree 3–6 m high bearing unique knobby knobby-segmented fruits filled with creamy aromatic sweet custard pulp.",
        "distinguishing_characteristics": "Alternate thin oblong-lanceolate leaves smelling faintly of petroleum/anise when crushed; pendulous greenish-yellow 3-angled narrow flowers; composite fruit composed of loosely adhering rounded fleshy knobby tubercles; delicious creamy white pulp.",
        "safety_notes": "Flesh is safe and delicious. Hard black seeds contain toxic annonacin (neurotoxin) and must NOT be chewed, crushed, or swallowed.",
        "confusable_species": [
            "Annona reticulata (Ramphal / Bullock's heart) - smooth brownish-red netted surface without distinct knobby tubercles",
            "Annona muricata (Soursop / Lakshmanphal) - large dark green fruit with soft fleshy spines"
        ]
    },
    {
        "id": "tamarindus-indica",
        "scientific_name": "Tamarindus indica L.",
        "canonical_name": "Tamarindus indica",
        "family": "Fabaceae",
        "genus": "Tamarindus",
        "species": "indica",
        "synonyms": [],
        "common_names": ["Tamarind", "Indian Tamarind", "Imli", "Tetul"],
        "regional_names": {
            "hi": ["इमली (Imli)"],
            "bn": ["তেঁতুল (Tetul)"],
            "ta": ["புளியமரம் (Puliyamaram)"]
        },
        "category": "fruit",
        "growth_type": "tree",
        "habitat": "Dry tropical plains, ancient roadside avenues throughout South and Central India",
        "flowering_season": "May to July",
        "description": "A massive long-lived evergreen tree 12–25 m tall with dark fissured bark, graceful feathery foliage, and curved brown pods packed with tart sour-sweet pulp.",
        "distinguishing_characteristics": "Dense rounded spreading crown; alternate pinnate leaves with 10–18 pairs of tiny oblong leaflets (1–2 cm) that fold up at night; small yellow flowers with red streaks; curved cinnamon-brown brittle pods filled with acidic brown pulp and hard shiny seeds.",
        "safety_notes": "Pulp is safe, edible, and a staple souring agent across Indian cooking. Safe and non-toxic.",
        "confusable_species": [
            "Phyllanthus emblica (Amla) - produces round green berries, not brown bean pods",
            "Acacia nilotica (Babool) - armed with sharp white spines and yellow puffball flowers"
        ]
    },

    # =========================================================================
    # 5. VEGETABLES & CROPS (18 Species)
    # =========================================================================
    {
        "id": "solanum-lycopersicum",
        "scientific_name": "Solanum lycopersicum L.",
        "canonical_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "genus": "Solanum",
        "species": "lycopersicum",
        "synonyms": ["Lycopersicon esculentum Mill."],
        "common_names": ["Tomato", "Tamatar"],
        "regional_names": {
            "hi": ["टमाटर (Tamatar)"],
            "bn": ["টমেটো (Tomato)"],
            "ta": ["தக்காளி (Thakkali)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Domestic kitchen gardens and agricultural vegetable fields globally",
        "flowering_season": "Year-round in cultivation",
        "description": "A glandular-pubescent sprawling annual or short-lived perennial herb bearing lobed foliage with a characteristic pungent smell and succulent red berries.",
        "distinguishing_characteristics": "Hairy glandular stems with strong distinctive pungent nightshade odor; pinnately compound/lobed leaves; small yellow 5-lobed nodding flowers with pointed anther cone; fleshy round or plum-shaped red fruit with gelatinous seeds.",
        "safety_notes": "Ripe fruit is nutritious and completely safe. Green stems and leaves contain solanine alkaloids and should not be eaten.",
        "confusable_species": [
            "Solanum melongena (Brinjal) - larger broad leaves and purple flowers",
            "Physalis philadelphica (Tomatillo) - fruit enclosed in a papery lantern calyx"
        ]
    },
    {
        "id": "solanum-melongena",
        "scientific_name": "Solanum melongena L.",
        "canonical_name": "Solanum melongena",
        "family": "Solanaceae",
        "genus": "Solanum",
        "species": "melongena",
        "synonyms": [],
        "common_names": ["Brinjal", "Eggplant", "Aubergine", "Baingan", "Begun"],
        "regional_names": {
            "hi": ["बैंगन (Baingan)"],
            "bn": ["বেগুন (Begun)"],
            "ta": ["கத்தரிக்காய் (Kathirikkai)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Native to India; cultivated across vegetable fields throughout the subcontinent",
        "flowering_season": "Year-round in cultivation",
        "description": "A bushy perennial herb cultivated as an annual 40–120 cm high with large woolly lobed leaves, star-shaped purple blossoms, and glossy edible berries in diverse shapes.",
        "distinguishing_characteristics": "Stems and calyces often armed with sharp prickles; alternate large ovate coarsely lobed leaves with star-shaped hairs; violet-purple star flowers with prominent yellow central anther column; glossy purple, green, or white fleshy berry.",
        "safety_notes": "Cooked fruit is a safe staple vegetable. Raw leaves and green calyces contain solanine; do not consume raw green parts.",
        "confusable_species": [
            "Solanum torvum (Turkey berry / Sundakkai) - larger spiny shrub with small clusters of round green marble-like berries",
            "Datura stramonium - upright trumpets with spiny capsules, deadly toxic"
        ]
    },
    {
        "id": "capsicum-annuum",
        "scientific_name": "Capsicum annuum L.",
        "canonical_name": "Capsicum annuum",
        "family": "Solanaceae",
        "genus": "Capsicum",
        "species": "annuum",
        "synonyms": [],
        "common_names": ["Chilli Pepper", "Green Chilli", "Mirch", "Lanka"],
        "regional_names": {
            "hi": ["हरी मिर्च (Hari Mirch)", "लाल मिर्च (Lal Mirch)"],
            "bn": ["লঙ্কা (Lanka)", "মরিচ (Morich)"],
            "ta": ["பச்சை மிளகாய் (Pachai Milagai)"]
        },
        "category": "vegetable_crop",
        "growth_type": "shrub",
        "habitat": "Agricultural fields, kitchen gardens throughout India",
        "flowering_season": "Year-round",
        "description": "A branched subshrub 40–100 cm tall bearing solitary white flowers and pungent hollow elongated berries containing capsaicin.",
        "distinguishing_characteristics": "Smooth angular stems; alternate simple ovate-lanceolate leaves with entire margins; nodding solitary white flowers with purple or white anthers; hollow elongated or conical berry fruit ripening from green to red, containing pungent seeds on central placenta.",
        "safety_notes": "Edible pungent spice and vegetable. Capsaicin causes intense burning pain if rubbed in eyes or on mucous membranes; wash hands after handling.",
        "confusable_species": [
            "Capsicum frutescens (Bird's eye chilli) - smaller upright pungent fruit clusters",
            "Solanum nigrum - black non-pungent round berry clusters"
        ]
    },
    {
        "id": "abelmoschus-esculentus",
        "scientific_name": "Abelmoschus esculentus (L.) Moench",
        "canonical_name": "Abelmoschus esculentus",
        "family": "Malvaceae",
        "genus": "Abelmoschus",
        "species": "esculentus",
        "synonyms": ["Hibiscus esculentus L."],
        "common_names": ["Okra", "Lady's Finger", "Bhindi", "Dherosh"],
        "regional_names": {
            "hi": ["भिंडी (Bhindi)"],
            "bn": ["ঢেঁড়শ (Dherosh)"],
            "ta": ["வெண்டைக்காய் (Vendaikkai)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Vegetable plots, warm alluvial agricultural fields across South Asia",
        "flowering_season": "June to October and March to May",
        "description": "A stout erect annual herb 1–2 m tall with bristly stems, palmately lobed leaves, yellow hibiscus-like flowers with red centers, and edible mucilaginous ridged pods.",
        "distinguishing_characteristics": "Hairy bristly erect stem; alternate large palmately 5–7 lobed leaves; large showy pale yellow flowers with deep purple-red center; elongated 5–8 angled pyramidal beaked capsule containing white seeds in mucilage.",
        "safety_notes": "Pods are completely non-toxic and nutritious. Bristles on stems and leaves can cause mild mechanical skin itch in harvesters.",
        "confusable_species": [
            "Hibiscus sabdariffa (Roselle) - fleshy red calyx, distinct sour leaves",
            "Abelmoschus moschatus (Musk mallow) - sprawling habit with musky aromatic seeds"
        ]
    },
    {
        "id": "oryza-sativa",
        "scientific_name": "Oryza sativa L.",
        "canonical_name": "Oryza sativa",
        "family": "Poaceae",
        "genus": "Oryza",
        "species": "sativa",
        "synonyms": [],
        "common_names": ["Asian Rice", "Paddy", "Dhan", "Chawal"],
        "regional_names": {
            "hi": ["धान (Dhan)", "चावल (Chawal)"],
            "bn": ["ধান (Dhan)"],
            "ta": ["நெல் (Nel)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Submerged wetlands, irrigated paddy fields, river deltas across India and Asia",
        "flowering_season": "Autumn (Aman) and Spring (Boro) crops",
        "description": "The primary staple food crop of over half the world's human population: an annual semi-aquatic grass growing 1–1.8 m tall in flooded wetland terraces.",
        "distinguishing_characteristics": "Tufted hollow culms rooting in mud; long linear flat leaf blades with distinct prominent membranous ligule and hairy auricles; terminal arching panicle of 1-flowered spikelets ripening into golden-yellow husked grains.",
        "safety_notes": "Safe staple food grain.",
        "confusable_species": [
            "Echinochloa crus-galli (Barnyard grass / Sanwa) - common paddy weed lacking ligules and auricles",
            "Triticum aestivum (Wheat) - upland dry crop with dense unbranched terminal spike"
        ]
    },
    {
        "id": "triticum-aestivum",
        "scientific_name": "Triticum aestivum L.",
        "canonical_name": "Triticum aestivum",
        "family": "Poaceae",
        "genus": "Triticum",
        "species": "aestivum",
        "synonyms": [],
        "common_names": ["Common Wheat", "Bread Wheat", "Gehun"],
        "regional_names": {
            "hi": ["गेहूं (Gehun)"],
            "bn": ["গম (Gom)"],
            "ta": ["கோதுமை (Godhumai)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Temperate to subtropical agricultural plains of Punjab, Haryana, Uttar Pradesh, and Madhya Pradesh",
        "flowering_season": "January to March (Rabi season)",
        "description": "The world's foremost cereal grain: an erect annual grass 60–120 cm tall with narrow linear leaves and a dense terminal bearded spike.",
        "distinguishing_characteristics": "Hollow jointed stems; alternate linear flat leaves with claw-like auricles clasping the stem; dense upright terminal spike (8–15 cm) bearing zigzag rachis and multi-flowered spikelets with long awns (beards); golden grain.",
        "safety_notes": "Safe staple food. Contains gluten (problematic for individuals with celiac disease).",
        "confusable_species": [
            "Hordeum vulgare (Barley / Jau) - has much longer prominent auricles and 3 spikelets at each rachis node",
            "Avena sativa (Oat) - loose spreading open panicle, not a dense spike"
        ]
    },
    {
        "id": "brassica-juncea",
        "scientific_name": "Brassica juncea (L.) Czern.",
        "canonical_name": "Brassica juncea",
        "family": "Brassicaceae",
        "genus": "Brassica",
        "species": "juncea",
        "synonyms": [],
        "common_names": ["Indian Mustard", "Brown Mustard", "Sarson", "Rai"],
        "regional_names": {
            "hi": ["सरसों (Sarson)", "राई (Rai)"],
            "bn": ["সরিষা (Shorishe)"],
            "ta": ["கடுகு (Kadugu)"]
        },
        "category": "vegetable_crop",
        "growth_type": "herb",
        "habitat": "Winter agricultural fields across northern and eastern India, famous for golden blooming landscapes",
        "flowering_season": "December to February",
        "description": "An erect multi-branched annual herb 1–1.5 m high with lyrate lower leaves and brilliant yellow 4-petaled cross-shaped flowers, cultivated for pungent seeds and mustard oil.",
        "distinguishing_characteristics": "Lower leaves large and lyrate-pinnatifid, upper leaves lanceolate and non-clasping; bright yellow 4-petaled cruciform flowers in terminal racemes with 6 stamens (tetradynamous: 4 long, 2 short); slender cylindrical beaked silique pods with pungent brown seeds.",
        "safety_notes": "Leaves (sarson ka saag) and oil are edible and nutritious. Mustard oil is pungent; pure allyl isothiocyanate can irritate eyes.",
        "confusable_species": [
            "Brassica campestris / napus (Rapeseed / Tori) - upper leaves deeply clasp around stem with auricles",
            "Raphanus sativus (Radish / Mooli) - white to lilac-veined flowers and spongy conical pods"
        ]
    },
    {
        "id": "momordica-charantia",
        "scientific_name": "Momordica charantia L.",
        "canonical_name": "Momordica charantia",
        "family": "Cucurbitaceae",
        "genus": "Momordica",
        "species": "charantia",
        "synonyms": [],
        "common_names": ["Bitter Gourd", "Bitter Melon", "Karela", "Karola"],
        "regional_names": {
            "hi": ["करेला (Karela)"],
            "bn": ["করলা (Korola)", "উচ্ছে (Uchhe)"],
            "ta": ["பாகற்காய் (Pavakkai)"]
        },
        "category": "vegetable_crop",
        "growth_type": "climber",
        "habitat": "Kitchen gardens, trellised vegetable farms across India",
        "flowering_season": "May to October",
        "description": "A slender tendril-bearing climbing vine with deeply palmately lobed leaves, solitary yellow flowers, and distinctly warty oblong green bitter fruits.",
        "distinguishing_characteristics": "Slender climbing stem with unbranched simple tendrils; deeply 5–7 lobed palmate leaves with pungent musky smell; solitary yellow 5-petaled flowers with a small rounded green bract mid-pedicel; warty ribbed tuberculate fruit containing seeds enclosed in red arils when overripe.",
        "safety_notes": "Cooked fruit is safe and renowned for blood-glucose regulation. High doses of raw juice can induce hypoglycemia or uterine contractions; avoid in pregnancy.",
        "confusable_species": [
            "Momordica dioica (Kantola / Spiny gourd) - dense soft spines on fruit, small dioecious climber",
            "Luffa acutangula (Ridge gourd) - deeply 10-angled long fruit without warts"
        ]
    },

    # =========================================================================
    # 6. WILD PLANTS, WEEDS, SUCCULENTS & AQUATICS (16 Species)
    # =========================================================================
    {
        "id": "mimosa-pudica",
        "scientific_name": "Mimosa pudica L.",
        "canonical_name": "Mimosa pudica",
        "family": "Fabaceae",
        "genus": "Mimosa",
        "species": "pudica",
        "synonyms": [],
        "common_names": ["Touch-Me-Not", "Sensitive Plant", "Shameplant", "Chhui Mui"],
        "regional_names": {
            "hi": ["छुई-मुई (Chhui-Mui)", "लाजवंती (Lajwanti)"],
            "bn": ["লজ্জাবতী লতা (Lajjabati Lata)"],
            "ta": ["தொட்டால் சிணுங்கி (Thottal Sinungi)"]
        },
        "category": "wild_grass",
        "growth_type": "herb",
        "habitat": "Wastelands, open grasslands, roadsides, disturbed soils across tropical India",
        "flowering_season": "July to November",
        "description": "A low-growing creeping or sub-erect thorny perennial herb famous for rapid thigmonastic leaf movement: leaves fold inward and droop immediately upon touch.",
        "distinguishing_characteristics": "Reddish-brown prickly stems with curved prickles; bipinnate sensitive leaves with 1–2 pairs of pinnae; leaflets rapidly fold together when touched (seismonastic movement) and reopen after minutes; fluffy pink-purple globular puffball flowerheads.",
        "safety_notes": "Non-toxic to handle. Stems bear sharp prickles that can scratch bare feet. Contains mimosine; not suitable for large-scale livestock grazing.",
        "confusable_species": [
            "Biophytum sensitivum (Little tree plant) - unbranched miniature palm-like herb with yellow flowers",
            "Neptunia oleracea (Water mimosa) - floating aquatic weed with spongy white stems"
        ]
    },
    {
        "id": "pontederia-crassipes",
        "scientific_name": "Pontederia crassipes Mart.",
        "canonical_name": "Pontederia crassipes",
        "family": "Pontederiaceae",
        "genus": "Pontederia",
        "species": "crassipes",
        "synonyms": ["Eichhornia crassipes (Mart.) Solms"],
        "common_names": ["Water Hyacinth", "Terror of Bengal", "Jal Kumbhi"],
        "regional_names": {
            "hi": ["जलकुंभी (Jal Kumbhi)"],
            "bn": ["কচুরিপানা (Kochuripana)"],
            "ta": ["ஆகாயத்தாமரை (Aagaya Thamarai)"]
        },
        "category": "aquatic",
        "growth_type": "aquatic_herb",
        "habitat": "Freshwater lakes, canals, drainage wetlands, and slow-moving rivers across the tropics",
        "flowering_season": "August to November",
        "description": "A notorious free-floating invasive aquatic perennial that forms dense suffocating mats over water bodies, famous in Bengal history as the 'Terror of Bengal'.",
        "distinguishing_characteristics": "Free-floating aquatic habit with spongy bulbous swollen air-filled petioles (acting as buoyancy floats); dark feathery fibrous roots hanging in water; rosette of glossy dark green rounded leaves; upright spike of 8–15 pale violet-blue flowers with a yellow spot surrounded by blue on upper petal.",
        "safety_notes": "Invasive weed. Non-toxic to touch, but harbors mosquitoes and chokes aquatic ecosystems. Leaves contain calcium oxalate crystals; not suitable for raw human consumption.",
        "confusable_species": [
            "Pistia stratiotes (Water lettuce) - velvety ribbed pale green rosette without violet flowers",
            "Monochoria vaginalis - rooted marsh herb with non-swollen petioles"
        ]
    },
    {
        "id": "lantana-camara",
        "scientific_name": "Lantana camara L.",
        "canonical_name": "Lantana camara",
        "family": "Verbenaceae",
        "genus": "Lantana",
        "species": "camara",
        "synonyms": [],
        "common_names": ["Lantana", "Wild Sage", "Raimuniya", "Ghaneri"],
        "regional_names": {
            "hi": ["रायमुनिया (Raimuniya)", "कुर्री (Kurri)"],
            "bn": ["পুতুস (Putus)", "লান্টানা (Lantana)"],
            "ta": ["உன்னிச்செடி (Unni Chedi)"]
        },
        "category": "wild_grass",
        "growth_type": "shrub",
        "habitat": "Invasive across Indian national parks, forest edges, wastelands, and roadsides",
        "flowering_season": "Year-round",
        "description": "A notorious invasive prickly evergreen scrambling shrub 1–3 m tall forming impenetrable thickets, bearing multicolored flat flower clusters and pungent foliage.",
        "distinguishing_characteristics": "Tetragonal (4-angled) stems armed with recurved prickles; opposite ovate rough sandpapery leaves with pungent citrus-herbal aroma; compact flat-topped floral heads with flowers that shift color from yellow to orange, pink, or red as they mature; small fleshy black drupes.",
        "safety_notes": "POISONOUS: Unripe green berries contain triterpenoids (lantadene A and B) that cause fatal liver failure and photosensitization in livestock and children.",
        "confusable_species": [
            "Lantana montevidensis (Trailing lantana) - prostrate thornless shrub with uniform lavender/purple flowers",
            "Verbena bonariensis - tall slender square stems with purple flowers, non-woody"
        ]
    },
    {
        "id": "parthenium-hysterophorus",
        "scientific_name": "Parthenium hysterophorus L.",
        "canonical_name": "Parthenium hysterophorus",
        "family": "Asteraceae",
        "genus": "Parthenium",
        "species": "hysterophorus",
        "synonyms": [],
        "common_names": ["Congress Grass", "Carrot Grass", "Santa Maria Feverfew", "Gajar Ghas"],
        "regional_names": {
            "hi": ["गाजर घास (Gajar Ghas)", "कांग्रेस घास (Congress Ghas)"],
            "bn": ["গাজর ঘাস (Gajor Ghas)", "পার্থেনিয়াম (Parthenium)"],
            "ta": ["பார்த்தீனியம் (Parthenium)"]
        },
        "category": "wild_grass",
        "growth_type": "herb",
        "habitat": "Invasive agricultural wasteland weed, vacant urban plots, and roadsides across all states of India",
        "flowering_season": "Year-round",
        "description": "A highly aggressive invasive annual weed 0.5–1.5 m tall with deeply lobed carrot-like foliage and thousands of tiny white flowerheads.",
        "distinguishing_characteristics": "Longitudinally grooved hairy stems; deeply pinnatifid leaves closely resembling carrot foliage; profusely branched panicles of tiny (3–5 mm) pentagonal star-shaped white flowerheads; prolific seed producer.",
        "safety_notes": "HEALTH HAZARD: High concentration of sesquiterpene lactone (parthenin). Airborne pollen causes severe allergic rhinitis and asthma; plant contact causes severe allergic contact dermatitis and eczema.",
        "confusable_species": [
            "Daucus carota (Wild carrot) - edible root with flat white umbels, not tiny star flowerheads",
            "Ambrosia artemisiifolia (Ragweed) - greenish spicate flowers without white petals"
        ]
    },
    {
        "id": "cynodon-dactylon",
        "scientific_name": "Cynodon dactylon (L.) Pers.",
        "canonical_name": "Cynodon dactylon",
        "family": "Poaceae",
        "genus": "Cynodon",
        "species": "dactylon",
        "synonyms": [],
        "common_names": ["Bermuda Grass", "Doob Grass", "Scutch Grass", "Durva"],
        "regional_names": {
            "hi": ["दूब घास (Doob Ghas)", "दुर्वा (Durva)"],
            "bn": ["দুর্বা ঘাস (Durba Ghash)"],
            "ta": ["அறுகம்புல் (Arugampul)"],
            "sa": ["दूर्वा (Durva)"]
        },
        "category": "wild_grass",
        "growth_type": "herb",
        "habitat": "Lawns, pastures, river embankments, cracks in pavements, sacred worship throughout India",
        "flowering_season": "Year-round",
        "description": "A tough creeping sod-forming perennial grass with deep stolons and rhizomes, revered in Hindu rituals dedicated to Lord Ganesha.",
        "distinguishing_characteristics": "Prostrate branching stolons rooting at every node; short linear flat-folded leaves (2–10 cm long) with hairy ligule; terminal digitately clustered seed head with 3–5 slender radiating spikes resembling a bird's foot.",
        "safety_notes": "Safe natural grass. Widely extracted for cooling traditional green juice (Arugampul juice).",
        "confusable_species": [
            "Eleusine indica (Goosegrass) - coarser bunchgrass with thicker stiff spikes",
            "Digitaria sanguinalis (Crabgrass) - wider leaves with distinct purplish hue and taller habit"
        ]
    },
    {
        "id": "dracaena-trifasciata",
        "scientific_name": "Dracaena trifasciata (Prain) Mabb.",
        "canonical_name": "Dracaena trifasciata",
        "family": "Asparagaceae",
        "genus": "Dracaena",
        "species": "trifasciata",
        "synonyms": ["Sansevieria trifasciata Prain"],
        "common_names": ["Snake Plant", "Mother-in-Law's Tongue", "Viper's Bowstring Hemp"],
        "regional_names": {
            "hi": ["स्नेक प्लांट (Snake Plant)"],
            "bn": ["স্নেক প্ল্যান্ট (Snake Plant)"],
            "ta": ["பாம்புச்செடி (Pambu Chedi)"]
        },
        "category": "succulent",
        "growth_type": "succulent",
        "habitat": "Ubiquitous indoor houseplant and outdoor ornamental border across India and the globe",
        "flowering_season": "Rare indoors; occasionally winter to spring",
        "description": "An indestructible architectural stemless succulent perennial forming erect clusters of stiff sword-shaped fleshy leaves with horizontal grey-green banding.",
        "distinguishing_characteristics": "Stiff erect sword-shaped succulent leaves (30–90 cm tall) with sharp points; dark green background with horizontal light greyish-green undulating zig-zag bands (and golden margins in cv. Laurentii); pale greenish-white fragrant nocturnal flowers in slender racemes.",
        "safety_notes": "Contains saponins. Mildly toxic to cats and dogs if chewed (causes salivation and vomiting); non-fatal to humans.",
        "confusable_species": [
            "Sansevieria cylindrica - leaves are round and cylindrical like spears",
            "Agave americana - leaves form open spreading rosette with vicious edge teeth"
        ]
    },
    {
        "id": "epipremnum-aureum",
        "scientific_name": "Epipremnum aureum (Linden & André) G.S.Bunting",
        "canonical_name": "Epipremnum aureum",
        "family": "Araceae",
        "genus": "Epipremnum",
        "species": "aureum",
        "synonyms": ["Scindapsus aureus (Linden & André) Engl."],
        "common_names": ["Golden Pothos", "Money Plant", "Devil's Ivy"],
        "regional_names": {
            "hi": ["मनी प्लांट (Money Plant)"],
            "bn": ["মানি প্ল্যান্ট (Money Plant)"],
            "ta": ["மணி பிளான்ட் (Money Plant)"]
        },
        "category": "climber",
        "growth_type": "climber",
        "habitat": "Ubiquitous household vine in water bottles and pots across almost every Indian home; climbs up trees outdoors",
        "flowering_season": "Extremely rare in cultivation (shy flowering)",
        "description": "An evergreen climbing vine that scrambles up trees and walls using aerial rootlets, renowned as the 'Money Plant' in Indian homes for good fortune.",
        "distinguishing_characteristics": "Heart-shaped glossy alternate leaves with yellow or white marble variegation; aerial roots at nodes; in juvenile indoor form leaves are 10–15 cm; when climbing outdoor tree trunks leaves become gigantic (up to 90 cm) with natural perforations and pinnatifid splits.",
        "safety_notes": "Contains insoluble calcium oxalate raphide crystals. Chewing stems or leaves causes immediate burning, swelling of lips and tongue; keep away from pets.",
        "confusable_species": [
            "Philodendron hederaceum (Heartleaf philodendron) - smooth non-variegated green leaves with distinct cataphylls (sheaths)",
            "Syngonium podophyllum (Arrowhead vine) - leaves become arrow-shaped then 3–5 lobed"
        ]
    },
    {
        "id": "opuntia-ficus-indica",
        "scientific_name": "Opuntia ficus-indica (L.) Mill.",
        "canonical_name": "Opuntia ficus-indica",
        "family": "Cactaceae",
        "genus": "Opuntia",
        "species": "ficus-indica",
        "synonyms": ["Cactus ficus-indica L."],
        "common_names": ["Prickly Pear", "Barbary Fig", "Nagphani", "Haththokana"],
        "regional_names": {
            "hi": ["नागफनी (Nagphani)"],
            "bn": ["নাগফণী (Nagphani)"],
            "ta": ["சப்பாத்திக்கள்ளி (Sappathikkalli)"]
        },
        "category": "succulent",
        "growth_type": "succulent",
        "habitat": "Dry arid scrub, rocky wastelands, field fencing across Rajasthan, Gujarat, and dry Deccan",
        "flowering_season": "March to June",
        "description": "A drought-hardy succulent shrub 1–3 m tall composed of flattened fleshy green pads (cladodes) bearing edible spiny pear-shaped fruits.",
        "distinguishing_characteristics": "Flat oval paddle-like green stem segments (cladodes); areoles bearing sharp spines and tiny barbed micro-bristles (glochids); bright yellow or orange flowers with numerous stamens; barrel-shaped spiny edible fruit ripening to purple-red.",
        "safety_notes": "CAUTION: Glochids (microscopic barbed bristles) easily detach into skin causing severe irritation and pain. Must be burned or peeled off fruit before handling.",
        "confusable_species": [
            "Euphorbia antiquorum (Tridhara / Triangular spurge) - produces toxic white latex and has 3-angled ribbed stems, not flat pads",
            "Opuntia elatior - wild naturalized species with dense vicious spines and dark red flowers"
        ]
    },
    {
        "id": "datura-stramonium",
        "scientific_name": "Datura stramonium L.",
        "canonical_name": "Datura stramonium",
        "family": "Solanaceae",
        "genus": "Datura",
        "species": "stramonium",
        "synonyms": [],
        "common_names": ["Jimsonweed", "Thorn Apple", "Datura", "Dhatura"],
        "regional_names": {
            "hi": ["धतूरा (Dhatura)"],
            "bn": ["ধুতুরা (Dhutura)"],
            "ta": ["ஊமத்தை (Umathai)"],
            "sa": ["धत्तूर (Dhattura)"]
        },
        "category": "wild_grass",
        "growth_type": "herb",
        "habitat": "Wastelands, rubbish heaps, roadsides, disturbed soils throughout India",
        "flowering_season": "July to November",
        "description": "A stout foul-smelling annual herb 60–150 cm tall with coarse dark green leaves, erect white or purple trumpet flowers, and fiercely spined walnut-sized fruit capsules.",
        "distinguishing_characteristics": "Dichotomously branched green or purple stems; alternate ovate coarsely sinuate-toothed leaves with unpleasant smell; large upright trumpet-shaped white/purple flowers (7–10 cm long); spiny egg-shaped 4-valved capsule (thorn apple) filled with pitted black kidney seeds.",
        "safety_notes": "EXTREMELY DANGEROUS / DEADLY: Contains potent tropane alkaloids (scopolamine, hyoscyamine, atropine). Ingestion induces severe delirium, hallucinations, hyperthermia, tachycardia, and fatal respiratory failure.",
        "confusable_species": [
            "Datura metel (Kala Dhatura / Devil's trumpet) - larger plant with downy leaves and purple double/triple trumpet flowers",
            "Brugmansia suaveolens (Angel's trumpet) - woody shrub with giant pendulous hanging flowers"
        ]
    },
    {
        "id": "ricinus-communis",
        "scientific_name": "Ricinus communis L.",
        "canonical_name": "Ricinus communis",
        "family": "Euphorbiaceae",
        "genus": "Ricinus",
        "species": "communis",
        "synonyms": [],
        "common_names": ["Castor Oil Plant", "Castor Bean", "Arandi", "Bherenda"],
        "regional_names": {
            "hi": ["अरंडी (Arandi)"],
            "bn": ["ভেরেণ্ডা (Bherenda)", "রেড়ী (Redi)"],
            "ta": ["ஆமணக்கு (Amanakku)"]
        },
        "category": "wild_grass",
        "growth_type": "shrub",
        "habitat": "Waste ground, railway embankments, riverbeds, and agricultural oilseed fields in Gujarat and Rajasthan",
        "flowering_season": "Year-round",
        "description": "A robust fast-growing soft-woody shrub or small tree 2–5 m tall with distinctive umbrella-like palmately lobed leaves and spiny seed capsules.",
        "distinguishing_characteristics": "Hollow glaucous purplish or green stems; giant alternate peltate palmately 7–11 lobed leaves (up to 50 cm wide) with serrate margins; terminal panicles with female flowers above male flowers; soft-spiny green to red 3-lobed capsules containing shiny mottled bean-like seeds.",
        "safety_notes": "DEADLY TOXIC SEEDS: Raw seeds contain RICIN, one of the most potent plant toxins known. Ingesting even 2–4 crushed seeds can be fatal to an adult. Cold-pressed castor oil is safe as ricin is not oil-soluble and is denatured during heat processing.",
        "confusable_species": [
            "Carica papaya (Papaya) - hollow unbranched trunk with large sweet fruits, not spiny capsules",
            "Jatropha curcas (Ratanjyot) - smaller 3–5 lobed leaves and smooth green capsule fruit"
        ]
    },
{   'canonical_name': 'Euphorbia pulcherrima',
    'category': 'ornamental',
    'common_names': ['Poinsettia', 'Christmas Star', 'Lalpata', 'Mexican Flame Leaf'],
    'confusable_species': [   'Euphorbia cotinifolia (Red spurge) - leaves completely burgundy all year round, not '
                              'just top bracts in winter'],
    'description': 'A popular winter ornamental shrub famed for its fiery scarlet floral bracts surrounding '
                   'inconspicuous central cyathia.',
    'distinguishing_characteristics': 'Large vibrant red (or cream/pink) ovate modified upper leaves (bracts); milky '
                                      'white latex exuded when wounded; small central greenish-yellow cup-like cyathia '
                                      'with single yellow nectar glands.',
    'family': 'Euphorbiaceae',
    'flowering_season': 'November to February (winter)',
    'genus': 'Euphorbia',
    'growth_type': 'shrub',
    'habitat': 'Widely cultivated in Indian hill stations, garden borders, and winter seasonal pots across India',
    'id': 'euphorbia-pulcherrima',
    'regional_names': {'bn': ['লালপাতা (Lalpata)'], 'hi': ['लालपत्ता (Lalpatta)']},
    'safety_notes': 'Mildly toxic: Milky sap contains diterpene esters that can cause skin irritation, contact '
                    'dermatitis, and mild stomach upset if ingested. Keep away from pets.',
    'scientific_name': 'Euphorbia pulcherrima Willd. ex Klotzsch',
    'species': 'pulcherrima',
    'synonyms': ['Poinsettia pulcherrima']},
{   'canonical_name': 'Monstera deliciosa',
    'category': 'ornamental',
    'common_names': ['Swiss Cheese Plant', 'Monstera', 'Split-leaf Philodendron', 'Fruit Salad Plant'],
    'confusable_species': [   'Epipremnum pinnatum (Dragon Tail) - thinner leaves with different fenestration pattern',
                              'Thaumatophyllum bipinnatifidum (Split-leaf Philodendron) - deeply cut leaves without '
                              'closed window perforations'],
    'description': 'An iconic tropical climbing epiphyte prized for its gigantic glossy heart-shaped leaves bearing '
                   'natural artistic perforations and pinnatifid splits.',
    'distinguishing_characteristics': 'Heavy aerial roots descending from nodes; mature leaves leathery, glossy dark '
                                      'green, perforated with oval fenestrations along the midrib and deep marginal '
                                      'lobes; spathe creamy white enclosing a spadix.',
    'family': 'Araceae',
    'flowering_season': 'Summer (rarely blooms indoors)',
    'genus': 'Monstera',
    'growth_type': 'climber',
    'habitat': 'Indoor potted plant and shaded tropical garden epiphyte throughout urban India',
    'id': 'monstera-deliciosa',
    'regional_names': {'bn': ['মনস্টেরা (Monstera)'], 'hi': ['मॉन्स्टेरा (Monstera)']},
    'safety_notes': 'All green parts contain needle-like insoluble calcium oxalate raphides. Chewing foliage causes '
                    'intense mouth burning, tongue swelling, and drooling. Ripe fruit (when scales naturally fall off) '
                    'is edible, but unripe fruit causes extreme throat irritation.',
    'scientific_name': 'Monstera deliciosa Liebm.',
    'species': 'deliciosa',
    'synonyms': ['Philodendron pertusum']},
{   'canonical_name': 'Spathiphyllum wallisii',
    'category': 'ornamental',
    'common_names': ['Peace Lily', 'White Sails', 'Spathe Flower'],
    'confusable_species': [   'Anthurium andraeanum (Flamingo Flower) - brightly colored glossy red or pink '
                              'heart-shaped spathes',
                              'Aglaonema (Chinese Evergreen) - variegated leaves with green and silver patterns'],
    'description': 'A very popular air-purifying indoor perennial with glossy deep-green arching leaves and elegant '
                   'white sail-like spathes.',
    'distinguishing_characteristics': 'Stemless clump-forming habit; dark green lanceolate ribbed leaves on long '
                                      'slender petioles; pure white sheath-like bract (spathe) arching behind a '
                                      'textured creamy-yellow spadix; spathes gradually turn green with age.',
    'family': 'Araceae',
    'flowering_season': 'Spring and monsoon',
    'genus': 'Spathiphyllum',
    'growth_type': 'herb',
    'habitat': 'Indoor office and home potted plant in indirect light; shaded moist garden verandas',
    'id': 'spathiphyllum-wallisii',
    'regional_names': {'bn': ['পিস লিলি (Peace Lily)'], 'hi': ['पीस लिली (Peace Lily)']},
    'safety_notes': 'Contains insoluble calcium oxalate crystals. Toxic to dogs and cats; causes mouth irritation, '
                    'excessive drooling, and difficulty swallowing if chewed.',
    'scientific_name': 'Spathiphyllum wallisii Regel',
    'species': 'wallisii',
    'synonyms': []},
{   'canonical_name': 'Chlorophytum comosum',
    'category': 'ornamental',
    'common_names': ['Spider Plant', 'Airplane Plant', 'Ribbon Plant', 'Spider Ivy'],
    'confusable_species': [   'Ophiopogon jaburan (Variegated Lilyturf) - stiffer leaves and lilac flower spikes, '
                              'lacks trailing runners with plantlets',
                              'Pandanus baptistii - much larger spiny margins or stiffer fibrous sword leaves'],
    'description': 'A resilient clump-forming grassy ornamental with arching green and white striped foliage that '
                   'produces long stolons bearing miniature plantlets.',
    'distinguishing_characteristics': 'Rosettes of linear, ribbon-like leaves usually with cream/white central '
                                      'stripes; long yellow-green runners (stolons) cascading outward with small '
                                      "star-shaped white 6-petaled flowers and tufted baby plantlets ('spiders'); "
                                      'thick fleshy tuberous white roots.',
    'family': 'Asparagaceae',
    'flowering_season': 'Year-round in cultivation',
    'genus': 'Chlorophytum',
    'growth_type': 'herb',
    'habitat': 'Hanging baskets, indoor tabletops, and garden borders throughout Indian cities',
    'id': 'chlorophytum-comosum',
    'regional_names': {'bn': ['স্পাইডার প্ল্যান্ট (Spider Plant)'], 'hi': ['स्पाइडर प्लांट (Spider Plant)']},
    'safety_notes': 'Safe and non-toxic to dogs, cats, and humans. Known for mild hallucinogenic or curiosity-inducing '
                    'effects in cats, but medically non-hazardous.',
    'scientific_name': 'Chlorophytum comosum (Thunb.) Jacques',
    'species': 'comosum',
    'synonyms': ['Anthericum comosum']},
{   'canonical_name': 'Zamioculcas zamiifolia',
    'category': 'ornamental',
    'common_names': ['ZZ Plant', 'Zanzibar Gem', 'Eternity Plant', 'Aroid Palm'],
    'confusable_species': [   'Zamia furfuracea (Cardboard Palm) - a cycad with fuzzy matte cardboard-textured leaves '
                              'and cone reproduction'],
    'description': 'An exceptionally drought-tolerant indoor plant recognized by its erect succulent stems carrying '
                   'glossy feather-like dark green leaflets.',
    'distinguishing_characteristics': 'Swollen potato-like underground rhizomes; thick succulent swollen bases on '
                                      'upright petioles; pinnately arranged opposite pairs of leathery, highly '
                                      'reflective dark green elliptical leaflets; handles weeks without water.',
    'family': 'Araceae',
    'flowering_season': 'Rarely flowers indoors; small brown-yellow spadix at ground level in late summer',
    'genus': 'Zamioculcas',
    'growth_type': 'herb',
    'habitat': 'Indoor low-light environments, modern living rooms, and corporate offices across India',
    'id': 'zamioculcas-zamiifolia',
    'regional_names': {'bn': ['জেডজেড প্ল্যান্ট (ZZ Plant)'], 'hi': ['ज़ीज़ी प्लांट (ZZ Plant)']},
    'safety_notes': 'Contains calcium oxalate crystals throughout its tissues. May cause localized skin irritation in '
                    'sensitive individuals and mucosal discomfort if ingested. Wash hands after handling broken stems.',
    'scientific_name': 'Zamioculcas zamiifolia (Lodd.) Engl.',
    'species': 'zamiifolia',
    'synonyms': ['Caladium zamiifolium']},
{   'canonical_name': 'Coffea arabica',
    'category': 'commercial_crop',
    'common_names': ['Arabian Coffee', 'Coffee Shrub', 'Kapi', 'Kafi'],
    'confusable_species': [   'Coffea canephora (Robusta Coffee) - larger, flatter leaves, rounder beans, grown at '
                              'lower elevations',
                              'Ixora coccinea (Jungle Geranium) - similar opposite leaves but compact red/orange '
                              'flower umbels'],
    'description': 'An evergreen tropical shrub producing delightfully fragrant star-like white blossoms and glossy '
                   'red cherries housing two flat-sided coffee beans.',
    'distinguishing_characteristics': 'Opposite, glossy, dark green elliptic leaves with prominent wavy margins; '
                                      'clusters of intensely jasmine-scented star-shaped white flowers at leaf axils; '
                                      "berries turn from green to bright crimson 'cherries' containing two seeds "
                                      'pressed face to face with a groove.',
    'family': 'Rubiaceae',
    'flowering_season': 'March to April (blossom showers)',
    'genus': 'Coffea',
    'growth_type': 'shrub',
    'habitat': 'High-altitude shade-grown plantations in the Western Ghats (Chikkamagaluru, Kodagu, Wayanad, Nilgiris)',
    'id': 'coffea-arabica',
    'regional_names': {   'bn': ['কফি (Coffee)'],
                          'hi': ['कॉफ़ी (Coffee)', 'कहवा (Kahwa)'],
                          'kn': ['ಕಾಫಿ (Kafi)'],
                          'ta': ['காபி (Kapi)']},
    'safety_notes': 'Roasted coffee beans are universally consumed. Concentrated caffeine from raw berries or high '
                    'intake is stimulating and toxic to pets (dogs and cats cannot metabolize caffeine).',
    'scientific_name': 'Coffea arabica L.',
    'species': 'arabica',
    'synonyms': []},
{   'canonical_name': 'Camellia sinensis',
    'category': 'commercial_crop',
    'common_names': ['Tea Plant', 'Tea Bush', 'Chai', 'Cha'],
    'confusable_species': [   'Camellia japonica (Ornamental Camellia) - much larger showy multi-petaled red or pink '
                              'flowers',
                              'Eurya nitida - small montane forest shrub with similar foliage but different fruit'],
    'description': 'A dense evergreen shrub trimmed to waist height in tea estates, whose tender young bud and two '
                   'leaves are hand-plucked to produce white, green, oolong, and black tea.',
    'distinguishing_characteristics': 'Alternate glossy dark green obovate leaves with serrate edges and soft hairs on '
                                      'young underside shoots; small solitary white nodding flowers with 7–8 petals '
                                      'and numerous bright yellow stamens; woody 3-lobed seed capsules.',
    'family': 'Theaceae',
    'flowering_season': 'October to December',
    'genus': 'Camellia',
    'growth_type': 'shrub',
    'habitat': 'Extensive rolling contour terraces in Darjeeling, Assam, Dooars, Munnar, and Kangra Valley',
    'id': 'camellia-sinensis',
    'regional_names': {'as': ['চাহ (Chah)'], 'bn': ['চা (Cha)'], 'hi': ['चाय (Chai)'], 'ta': ['தேயிலை (Theeyilai)']},
    'safety_notes': 'Safe and globally consumed as tea. High consumption of concentrated tea extracts or raw leaves '
                    'contains caffeine and tannins which may irritate sensitive stomachs.',
    'scientific_name': 'Camellia sinensis (L.) Kuntze',
    'species': 'sinensis',
    'synonyms': ['Thea sinensis']},
{   'canonical_name': 'Gossypium hirsutum',
    'category': 'commercial_crop',
    'common_names': ['Upland Cotton', 'Cotton Plant', 'Kapas', 'Tula'],
    'confusable_species': [   'Gossypium arboreum (Desi Cotton) - narrower leaf lobes and smaller bolls',
                              'Hibiscus sabdariffa (Roselle) - fleshy red calyces rather than fibrous bolls'],
    'description': 'The premier textile crop of India, a branched annual shrub that produces creamy yellow flowers '
                   'that turn pink, followed by bursting capsules of fluffy white cellulose fibers.',
    'distinguishing_characteristics': 'Alternate cordate leaves with 3–5 broad lobes covered in fine hairs; cup-shaped '
                                      'creamy white/yellow flowers with three large fringed involucral bracts '
                                      '(epicalyx) that turn reddish-pink after pollination; 3–5 locular capsule '
                                      "('boll') bursting open to reveal soft white fibers enclosing dark seeds.",
    'family': 'Malvaceae',
    'flowering_season': 'August to November',
    'genus': 'Gossypium',
    'growth_type': 'shrub',
    'habitat': 'Black cotton soil (regur) plains of Maharashtra, Gujarat, Telangana, and Punjab',
    'id': 'gossypium-hirsutum',
    'regional_names': {   'bn': ['তুলা (Tula)', 'কার্পাস (Karpas)'],
                          'gu': ['કપાસ (Kapas)'],
                          'hi': ['कपास (Kapas)'],
                          'mr': ['कापूस (Kapoos)']},
    'safety_notes': 'Cotton lint is an inert fiber. Cottonseed contains gossypol, a polyphenol toxic to non-ruminants '
                    'and humans unless properly refined and cooked into cottonseed oil.',
    'scientific_name': 'Gossypium hirsutum L.',
    'species': 'hirsutum',
    'synonyms': []},
{   'canonical_name': 'Saccharum officinarum',
    'category': 'commercial_crop',
    'common_names': ['Sugarcane', 'Noble Cane', 'Ganna', 'Ikh', 'Aakh'],
    'confusable_species': [   'Saccharum spontaneum (Kans grass) - wild uncultivated relative with much thinner dry '
                              'pithy stalks and prominent white tassels',
                              'Sorghum bicolor (Sweet sorghum) - hollower stems with large grain head'],
    'description': 'A massive perennial tropical clump grass growing 3–6 m high, famous for its sweet, juicy, fibrous '
                   'stalks used to produce gur (jaggery) and refined sugar.',
    'distinguishing_characteristics': 'Stout, solid jointed fibrous stalks (culms) 3–5 cm in diameter, banded in '
                                      'yellow, green, or purple rings with white waxy bloom; prominent swollen nodes '
                                      'with bud eyes; long sharp-edged linear leaves with a thick white midrib; '
                                      "plume-like silvery silky terminal panicles ('arrow').",
    'family': 'Poaceae',
    'flowering_season': 'Winter (October to January), rarely flowers under commercial harvest',
    'genus': 'Saccharum',
    'growth_type': 'grass',
    'habitat': 'River valley irrigation belts across Uttar Pradesh, Maharashtra, Karnataka, and Tamil Nadu',
    'id': 'saccharum-officinarum',
    'regional_names': {   'bn': ['আখ (Aakh)', 'ইক্ষু (Ikkshu)'],
                          'hi': ['गन्ना (Ganna)', 'ईख (Ikh)'],
                          'mr': ['ऊस (Oos)'],
                          'ta': ['கரும்பு (Karumbu)']},
    'safety_notes': 'Stalk juice is sweet and edible. Leaf margins are finely serrate with silica and can cause '
                    'painful skin paper-cuts when passing through sugarcane fields.',
    'scientific_name': 'Saccharum officinarum L.',
    'species': 'officinarum',
    'synonyms': []},
{   'canonical_name': 'Cicer arietinum',
    'category': 'commercial_crop',
    'common_names': ['Chickpea', 'Bengal Gram', 'Garbanzo', 'Chana', 'Chhola'],
    'confusable_species': [   'Lens culinaris (Lentil / Masoor) - smaller leaflets with terminal tendrils',
                              'Pisum sativum (Field Pea / Matar) - smooth glaucous leaves with pronounced curling '
                              'tendrils'],
    'description': 'An important Indian pulse, a branched low bushy annual herb blanketed with glandular hairs that '
                   'secrete sour dew (malic and oxalic acids) prized in folk medicine.',
    'distinguishing_characteristics': 'Pinnately compound leaves with 9–17 small serrate leaflets covered in glandular '
                                      'hairs; solitary pea-like pink, purple, or white flowers in leaf axils; swollen '
                                      "oval hairy pods containing 1–2 beaked angular seeds ('ram's head' shape).",
    'family': 'Fabaceae',
    'flowering_season': 'December to February',
    'genus': 'Cicer',
    'growth_type': 'herb',
    'habitat': 'Winter rabi season crop across Madhya Pradesh, Rajasthan, Maharashtra, and Uttar Pradesh',
    'id': 'cicer-arietinum',
    'regional_names': {   'bn': ['ছোলা (Chhola)', 'চানা (Chana)'],
                          'gu': ['ચણા (Chana)'],
                          'hi': ['चना (Chana)'],
                          'ta': ['கொண்டைக்கடலை (Kondaikkadalai)']},
    'safety_notes': 'Universally edible pulse. The acidic dew collected from morning plants is caustic in high '
                    'concentration due to malic and oxalic acid.',
    'scientific_name': 'Cicer arietinum L.',
    'species': 'arietinum',
    'synonyms': []},
{   'canonical_name': 'Zea mays',
    'category': 'commercial_crop',
    'common_names': ['Maize', 'Corn', 'Indian Corn', 'Makka', 'Bhutta'],
    'confusable_species': [   'Sorghum bicolor (Jowar) - terminal compact grain head, no separate cob with silk',
                              'Pennisetum glaucum (Bajra) - compact cylindrical cattail-like spike'],
    'description': 'A tall, robust annual cereal grass growing up to 3 m tall, producing terminal male tassels and '
                   'axillary female ears packed with kernels wrapped in protective husks.',
    'distinguishing_characteristics': 'Single stout erect unbranched stem with prop roots near base; broad ribbon-like '
                                      "arching leaves with wavy margins; terminal staminate panicle ('tassel'); "
                                      'axillary pistillate inflorescence enclosed in husks with long silky styles '
                                      "('corn silk') emerging from the tip.",
    'family': 'Poaceae',
    'flowering_season': 'July to September / January to March',
    'genus': 'Zea',
    'growth_type': 'grass',
    'habitat': 'Warm Kharif and rabi grain fields in Karnataka, Bihar, Madhya Pradesh, and Andhra Pradesh',
    'id': 'zea-mays',
    'regional_names': {   'bn': ['ভুট্টা (Bhutta)'],
                          'gu': ['મકાઈ (Makai)'],
                          'hi': ['मक्का (Makka)', 'भुट्टा (Bhutta)'],
                          'te': ['మొక్కజొన్న (Mokkajonna)']},
    'safety_notes': 'Kernels and roasted cobs are completely edible. Raw corn silk is traditionally used as a mild '
                    'diuretic herbal tea.',
    'scientific_name': 'Zea mays L.',
    'species': 'mays',
    'synonyms': []},
{   'canonical_name': 'Allium cepa',
    'category': 'commercial_crop',
    'common_names': ['Onion', 'Garden Onion', 'Pyaz', 'Peyaj', 'Kanda'],
    'confusable_species': [   'Allium sativum (Garlic) - solid flat leaves and composite bulb with cloves',
                              'Allium tuberosum (Garlic chives) - flat solid leaves and star-shaped white flowers'],
    'description': 'The quintessential culinary bulb, a biennial herb producing hollow tubular bluish-green leaves and '
                   'a layered tunic-covered underground bulb rich in pungent organosulfur compounds.',
    'distinguishing_characteristics': 'Tunicated round or flattened bulb with papery red, yellow, or white skin; '
                                      'hollow cylindrical leaves with flattened inside surfaces; tall hollow swollen '
                                      'scape bearing a spherical umbel of greenish-white 6-parted flowers enclosed '
                                      'initially in a papery spathe.',
    'family': 'Amaryllidaceae',
    'flowering_season': 'February to April (bolting)',
    'genus': 'Allium',
    'growth_type': 'herb',
    'habitat': 'Winter vegetable beds and commercial market gardens in Nashik (Maharashtra), Gujarat, and Bengal',
    'id': 'allium-cepa',
    'regional_names': {   'bn': ['পেঁয়াজ (Peyaj)'],
                          'hi': ['प्याज (Pyaz)'],
                          'mr': ['कांदा (Kanda)'],
                          'ta': ['வெங்காயம் (Vengayam)']},
    'safety_notes': 'Culinary staple for humans. TOXIC TO DOGS AND CATS: Contains n-propyl disulfide which causes '
                    'oxidative damage to red blood cells resulting in hemolytic anemia.',
    'scientific_name': 'Allium cepa L.',
    'species': 'cepa',
    'synonyms': []},
{   'canonical_name': 'Allium sativum',
    'category': 'medicinal',
    'common_names': ['Garlic', 'Lahsun', 'Rosun', 'Lassan'],
    'confusable_species': [   'Allium cepa (Onion) - round single layered bulb and hollow tubular leaves',
                              'Allium ampeloprasum (Elephant garlic) - much larger milder single cloves'],
    'description': 'A revered spice and medicinal bulb comprising a cluster of curved cloves wrapped in thin '
                   'parchment, famed for allicin with antibacterial and cardiovascular benefits.',
    'distinguishing_characteristics': "Compound bulb consisting of 8–20 crescent-shaped bulblets ('cloves') enclosed "
                                      'in a common white or purplish papery tunic; flat, solid linear leaves (not '
                                      'hollow like onions) with a sharp keel; erect scape occasionally topped by '
                                      'bulblets mixed with sterile pinkish flowers.',
    'family': 'Amaryllidaceae',
    'flowering_season': 'Spring (often sterile)',
    'genus': 'Allium',
    'growth_type': 'herb',
    'habitat': 'Winter vegetable garden plots across Madhya Pradesh, Gujarat, and Rajasthan',
    'id': 'allium-sativum',
    'regional_names': {   'bn': ['রসুন (Rosun)'],
                          'gu': ['લસણ (Lasan)'],
                          'hi': ['लहसुन (Lahsun)'],
                          'ta': ['பூண்டு (Poondu)']},
    'safety_notes': 'Safe in culinary and standard medicinal use. Pungent raw garlic can cause contact dermatitis or '
                    'gastric burn in sensitive individuals. TOXIC TO CATS AND DOGS.',
    'scientific_name': 'Allium sativum L.',
    'species': 'sativum',
    'synonyms': []},
{   'canonical_name': 'Piper betle',
    'category': 'medicinal',
    'common_names': ['Betel Vine', 'Betel Pepper', 'Paan', 'Tambula'],
    'confusable_species': [   'Piper nigrum (Black pepper) - stiffer leathery leaves and pendulous fruit spikes '
                              'turning red',
                              'Piper longum (Pippali) - creeping herb with upright cylindrical flower spikes'],
    'description': 'An evergreen dioecious climbing vine cultivated under moist thatched bamboo sheds for its glossy '
                   'heart-shaped aromatic leaves chewed as traditional Paan.',
    'distinguishing_characteristics': 'Semi-woody climbing vine with adventitious roots at swollen nodes; alternate '
                                      'glossy, bright green heart-shaped leaves with 5–7 prominent veins radiating '
                                      'from an asymmetrical cordate base; spicy clove-scented pungent aroma when torn.',
    'family': 'Piperaceae',
    'flowering_season': 'Rarely flowers under shade cultivation; spikes in monsoon',
    'genus': 'Piper',
    'growth_type': 'climber',
    'habitat': "Shaded humid conservatories ('Paan Baroj' or 'Bareja') in West Bengal, Odisha, Assam, and Tamil Nadu",
    'id': 'piper-betle',
    'regional_names': {   'bn': ['পান (Paan)'],
                          'hi': ['पान (Paan)'],
                          'ta': ['வெற்றிலை (Vettilai)'],
                          'te': ['తమలపాకు (Tamalapaku)']},
    'safety_notes': 'Fresh betel leaf alone is a digestive and antimicrobial masticatory. When combined with areca '
                    'nut, slaked lime (chuna), and tobacco, it is strongly associated with oral cancer and submucous '
                    'fibrosis.',
    'scientific_name': 'Piper betle L.',
    'species': 'betle',
    'synonyms': []},
{   'canonical_name': 'Areca catechu',
    'category': 'tree',
    'common_names': ['Areca Palm', 'Betel Nut Palm', 'Supari', 'Guwa'],
    'confusable_species': [   'Dypsis lutescens (Areca palm / Cane palm) - multi-stemmed clustering ornamental palm '
                              'with yellow petioles',
                              'Cocos nucifera (Coconut palm) - much thicker curving trunk and giant coconuts'],
    'description': 'A very tall, slender single-stemmed palm with a clean crownshaft and pinnate fronds, bearing '
                   'pendulous clusters of orange fibrous fruits containing the hard areca nut.',
    'distinguishing_characteristics': 'Extremely slender, ringed gray trunk (up to 20–30 m tall and only 15–20 cm '
                                      'diameter); smooth bright green crownshaft; crown of 8–12 pinnate fronds with '
                                      'crowded leaflets; large branched spadix below crownshaft bearing orange oval '
                                      'fibrous drupes.',
    'family': 'Arecaceae',
    'flowering_season': 'Year-round',
    'genus': 'Areca',
    'growth_type': 'tree',
    'habitat': 'Coastal belts and lush intercropped groves in Karnataka, Kerala, Assam, and coastal Bengal',
    'id': 'areca-catechu',
    'regional_names': {   'as': ['তামোল (Tamul)'],
                          'bn': ['সুপারি (Supari)'],
                          'hi': ['सुपारी (Supari)'],
                          'ta': ['பாக்கு (Paakku)']},
    'safety_notes': 'The nut contains arecoline, a psychoactive alkaloid. Chronic chewing of betel nut is classified '
                    'by IARC as a Group 1 human carcinogen, strongly linked to oral submucous fibrosis.',
    'scientific_name': 'Areca catechu L.',
    'species': 'catechu',
    'synonyms': []},
{   'canonical_name': 'Aegle marmelos',
    'category': 'medicinal',
    'common_names': ['Bael', 'Golden Apple', 'Wood Apple', 'Bilva', 'Bel'],
    'confusable_species': [   'Limonia acidissima (Wood Apple / Kaith) - pinnate leaves with winged rachis and rough '
                              'brown fruit with dark sour pulp',
                              'Citrus aurantiifolia (Key lime) - unifoliate winged leaves and soft rind'],
    'description': 'A sacred deciduous thorny tree of the citrus family, famous for its trifoliate leaves offered in '
                   'worship and hard woody-shelled aromatic medicinal fruit.',
    'distinguishing_characteristics': 'Sharp straight axillary spines (1–2 cm); alternate trifoliate leaves with a '
                                      'distinctive aromatic citrus smell when crushed; greenish-white fragrant flowers '
                                      'with 4 petals; large globose fruit (5–15 cm) with a hard woody grey-green shell '
                                      'and fragrant orange sweet fibrous pulp with mucilaginous seeds.',
    'family': 'Rutaceae',
    'flowering_season': 'April to May',
    'genus': 'Aegle',
    'growth_type': 'tree',
    'habitat': 'Dry deciduous forests and temple courtyards sacred to Lord Shiva throughout India',
    'id': 'aegle-marmelos',
    'regional_names': {   'bn': ['বেল (Bel)'],
                          'hi': ['बेल (Bel)', 'बिल्व (Bilva)'],
                          'ta': ['வில்வம் (Vilvam)'],
                          'te': ['మారేడు (Maredu)']},
    'safety_notes': 'Ripe fruit pulp is widely consumed as sherbet and is a renowned Ayurvedic remedy for dysentery '
                    'and constipation. Leaf juice should be taken in moderation.',
    'scientific_name': 'Aegle marmelos (L.) Corrêa',
    'species': 'marmelos',
    'synonyms': []},
{   'canonical_name': 'Butea monosperma',
    'category': 'tree',
    'common_names': ['Flame of the Forest', 'Palash', 'Dhak', 'Bastard Teak', 'Tesu'],
    'confusable_species': [   'Delonix regia (Gulmohar) - bipinnate fine ferny leaves and 5-petaled open flowers '
                              'blooming in summer',
                              'Erythrina variegata (Indian Coral Tree) - prickly trunk and upright scarlet sword-like '
                              'flower racemes'],
    'description': "The sensational 'Flame of the Forest', which sheds its leaves in spring to erupt in breathtaking "
                   'canopies of fiery scarlet-orange keel-shaped blooms used to make natural Holi colors.',
    'distinguishing_characteristics': 'Crooked gnarled trunk with dark fibrous bark; large alternate trifoliate '
                                      'leathery leaves with rhomboid leaflets; leafless flowering branches crowded '
                                      'with velvety black calyces and blazing orange-red papilionaceous flowers '
                                      "resembling a parrot's beak; single flat oblong pod.",
    'family': 'Fabaceae',
    'flowering_season': 'February to April (spring / Holi)',
    'genus': 'Butea',
    'growth_type': 'tree',
    'habitat': 'Dry deciduous forests, open plains, and ravines across central and northern India, especially Chota '
               'Nagpur and Bundelkhand',
    'id': 'butea-monosperma',
    'regional_names': {   'bn': ['পলাশ (Palash)'],
                          'hi': ['पलाश (Palash)', 'ढाक (Dhak)', 'टेसू (Tesu)'],
                          'mr': ['पळस (Palas)'],
                          'te': ['మోదుగ (Moduga)']},
    'safety_notes': 'Flowers produce a non-toxic natural yellow-orange dye traditionally used for Holi. Seeds contain '
                    'butin and palasonin and are vermifuge but mildly toxic if ingested in large quantities.',
    'scientific_name': 'Butea monosperma (Lam.) Taub.',
    'species': 'monosperma',
    'synonyms': ['Butea frondosa']},
{   'canonical_name': 'Cassia fistula',
    'category': 'tree',
    'common_names': ['Golden Shower Tree', 'Amaltas', 'Indian Laburnum', 'Sonalu', 'Bandarlathi'],
    'confusable_species': [   'Peltophorum pterocarpum (Yellow Gulmohar) - bipinnate leaves and upright flower '
                              'panicles, not hanging cascades',
                              'Senna siamea (Kassod tree) - upright terminal yellow clusters and flat pods'],
    'description': 'A magnificent medium-sized deciduous tree crowned in summer with pendulous cascades of bright '
                   'golden-yellow fragrant blossoms, followed by long cylindrical brown pipe-like pods.',
    'distinguishing_characteristics': 'Pinnate leaves with 4–8 pairs of large ovate leaflets; pendulous drooping '
                                      'racemes (30–60 cm long) packed with 5-petaled buttercup-yellow fragrant '
                                      'flowers; very long dark brown woody cylindrical pods (40–60 cm) containing dark '
                                      'sweet pulp partitioned into cells.',
    'family': 'Fabaceae',
    'flowering_season': 'April to June (peak summer)',
    'genus': 'Cassia',
    'growth_type': 'tree',
    'habitat': "Deciduous forests and roadside avenue trees across India; the sacred flower of Kerala's Vishu festival",
    'id': 'cassia-fistula',
    'regional_names': {   'bn': ['সোনালু (Sonalu)', 'বাঁদরলাঠি (Bandarlathi)'],
                          'hi': ['अमलतास (Amaltas)'],
                          'ml': ['കണിക്കൊന്ന (Kanikkonna)'],
                          'ta': ['கொன்றை (Kondrai)']},
    'safety_notes': 'Pod pulp is a classic Ayurvedic mild laxative. Seeds are emetic and should not be eaten raw in '
                    'quantity.',
    'scientific_name': 'Cassia fistula L.',
    'species': 'fistula',
    'synonyms': []},
{   'canonical_name': 'Bauhinia variegata',
    'category': 'tree',
    'common_names': ['Orchid Tree', 'Mountain Ebony', 'Kachnar', 'Kanchan'],
    'confusable_species': [   'Bauhinia purpurea (Purple Orchid Tree) - blooms in autumn (Sept–Nov) with narrower '
                              'petals and 3 stamens (variegata has 5)',
                              'Bauhinia acuminata (White Orchid Tree) - shrubby habit with pure white flowers and '
                              'pointed leaf lobes'],
    'description': "A graceful small-to-medium deciduous tree renowned for its distinctive twin-lobed 'camel's foot' "
                   'leaves and showy fragrant orchid-like blossoms.',
    'distinguishing_characteristics': 'Unique bilobed leaves cleft nearly halfway, resembling a hoofprint or '
                                      'butterfly; clusters of 5-petaled fragrant orchid-like flowers in shades of '
                                      'magenta, pink, or white, with one petal darker and variegated with purple '
                                      'veins; flat dehiscent pods.',
    'family': 'Fabaceae',
    'flowering_season': 'February to April (spring)',
    'genus': 'Bauhinia',
    'growth_type': 'tree',
    'habitat': 'Sub-Himalayan valleys, mixed deciduous forests, and ornamental garden avenues throughout India',
    'id': 'bauhinia-variegata',
    'regional_names': {   'bn': ['কাঞ্চন (Kanchan)', 'রক্তকাঞ্চন (Raktakanchan)'],
                          'hi': ['कचनार (Kachnar)'],
                          'ta': ['மந்தாரை (Mandharai)']},
    'safety_notes': "Floral buds ('Kachnar kali') are a celebrated edible culinary delicacy in North India cooked with "
                    'spices. Completely non-toxic.',
    'scientific_name': 'Bauhinia variegata L.',
    'species': 'variegata',
    'synonyms': []},
{   'canonical_name': 'Cestrum nocturnum',
    'category': 'flower',
    'common_names': ['Night-blooming Jasmine', 'Raat ki Rani', 'Hasnuhana', 'Queen of the Night'],
    'confusable_species': [   'Cestrum diurnum (Day-blooming Jasmine / Din ka Raja) - erect shrub with white flowers '
                              'blooming and fragrant during daytime',
                              'Nyctanthes arbor-tristis (Parijat) - tree with orange-tubed white flowers dropped at '
                              'dawn'],
    'description': 'A woody sprawling evergreen shrub legendary for its intensely sweet, intoxicating perfume released '
                   'exclusively after sunset.',
    'distinguishing_characteristics': 'Slender drooping green branches; alternate simple glossy lanceolate leaves; '
                                      'dense axillary cymes of narrow tubular greenish-white flowers (2 cm long) with '
                                      '5 star-like reflexed lobes that open only at dusk; small white globose berries.',
    'family': 'Solanaceae',
    'flowering_season': 'Monsoon to early winter (repeated flushes)',
    'genus': 'Cestrum',
    'growth_type': 'shrub',
    'habitat': 'Homestead courtyards, ornamental gardens, and compound walls across urban and rural India',
    'id': 'cestrum-nocturnum',
    'regional_names': {   'bn': ['হাসনুহানা (Hasnuhana)'],
                          'hi': ['रात की रानी (Raat ki Rani)'],
                          'ta': ['இரவு ராணி (Iravu Rani)']},
    'safety_notes': 'POISONOUS PARTS: All parts of the plant, especially the white berries, contain solanine and '
                    'anticholinergic alkaloids. Ingestion causes fever, rapid pulse, and vomiting. Intense fragrance '
                    'may trigger headaches or asthma in sensitive individuals.',
    'scientific_name': 'Cestrum nocturnum L.',
    'species': 'nocturnum',
    'synonyms': []},
{   'canonical_name': 'Senna tora',
    'category': 'wild_grass',
    'common_names': ['Sicklepod', 'Sickle Senna', 'Chakwad', 'Chakunda', 'Charota'],
    'confusable_species': [   'Senna occidentalis (Coffee Senna / Kasondi) - ovate pointed leaflets (4–5 pairs) and '
                              'straight flat pods'],
    'description': 'A very common annual monsoon herb with yellow flowers and long sickle-shaped pods, widely '
                   'harvested in tribal and rural areas as a leafy vegetable and Ayurvedic skin remedy.',
    'distinguishing_characteristics': 'Erect branching herb (30–90 cm) with a fetid scent when crushed; pinnate leaves '
                                      'with exactly 3 pairs of obovate leaflets (widest at tip) with a glandular rod '
                                      'between lowest pair; bright yellow small 5-petaled flowers in pairs; very '
                                      'slender curved sickle-like pods (15–20 cm).',
    'family': 'Fabaceae',
    'flowering_season': 'August to October (monsoon)',
    'genus': 'Senna',
    'growth_type': 'herb',
    'habitat': 'Widespread monsoon wasteland colonizer, roadsides, and fallow fields across rural India',
    'id': 'senna-tora',
    'regional_names': {   'bn': ['চাকুন্দা (Chakunda)'],
                          'hi': ['चकवड़ (Chakwad)', 'पवाड़ (Pawar)'],
                          'or': ['ଚକୁନ୍ଦା (Chakunda)'],
                          'ta': ['தகரை (Thagarai)']},
    'safety_notes': 'Tender young leaves are eaten cooked as saag in rural Bengal, Odisha, and Chhattisgarh. Seeds '
                    'contain anthraquinones and are purgative; excessive raw ingestion by cattle has been implicated '
                    'in toxic myopathy.',
    'scientific_name': 'Senna tora (L.) Roxb.',
    'species': 'tora',
    'synonyms': ['Cassia tora']},
{   'canonical_name': 'Codiaeum variegatum',
    'category': 'ornamental',
    'common_names': ['Garden Croton', 'Variegated Croton', 'Croton'],
    'confusable_species': [   'Acalypha wilkesiana (Copperleaf) - serrate soft papery leaves, lacks the thick waxy '
                              'texture of croton'],
    'description': 'A staple tropical foliage shrub celebrated for its stunningly kaleidoscopic, thick leathery leaves '
                   'splashed with bright yellow, red, orange, and emerald green patterns.',
    'distinguishing_characteristics': 'Woody shrub with thick leathery alternate leaves of wildly diverse shapes '
                                      '(linear, lobed, twisted, or fiddle-shaped); dazzling multicolored veins and '
                                      'blotches in scarlet, amber, and purple; exudes watery to milky sap when broken.',
    'family': 'Euphorbiaceae',
    'flowering_season': 'Summer (inconspicuous racemes)',
    'genus': 'Codiaeum',
    'growth_type': 'shrub',
    'habitat': 'Ubiquitous ornamental garden hedge, porch container plant, and landscaping shrub across India',
    'id': 'codiaeum-variegatum',
    'regional_names': {'bn': ['ক্রোটন (Croton)', 'পাতা বাহার (Pata Bahar)'], 'hi': ['क्रोटन (Croton)']},
    'safety_notes': 'Sap contains 5-deoxyingenol and related esters which cause contact dermatitis, eczema, and skin '
                    'blistering in sensitive persons. Ingesting foliage causes vomiting and colic in pets.',
    'scientific_name': 'Codiaeum variegatum (L.) Rumph. ex A.Juss.',
    'species': 'variegatum',
    'synonyms': ['Croton variegatus']},
{   'canonical_name': 'Caladium bicolor',
    'category': 'ornamental',
    'common_names': ['Heart of Jesus', 'Caladium', 'Angel Wings', 'Elephant Ear'],
    'confusable_species': [   'Colocasia esculenta (Taro / Kochu) - large velvety green leaves with water-repellent '
                              'surface, lacking bright pink/white translucent windows',
                              'Alocasia macrorrhizos (Giant taro) - much larger glossy upright green leaves'],
    'description': 'A stunning tuberous ornamental aroid with paper-thin translucent heart- or arrow-shaped leaves '
                   'painted in radiant mosaics of crimson, hot pink, and crisp white margins.',
    'distinguishing_characteristics': 'Tuberous perennial without above-ground stems; peltate heart-shaped leaves on '
                                      'long graceful petioles; leaf blades paper-thin with vividly colored central '
                                      'veins and mottled translucent patches; typical aroid spathe and spadix at base.',
    'family': 'Araceae',
    'flowering_season': 'Monsoon to autumn',
    'genus': 'Caladium',
    'growth_type': 'herb',
    'habitat': 'Potted veranda plants and shaded monsoon garden borders throughout India',
    'id': 'caladium-bicolor',
    'regional_names': {'bn': ['ক্যালাডিয়াম (Caladium)', 'রঙিন কচু (Rongin Kochu)'], 'hi': ['कैलेडियम (Caladium)']},
    'safety_notes': 'HIGH TOXICITY IF CHEWED: Contains sharp insoluble calcium oxalate raphides. Causes intense '
                    'burning of mouth, lips, and tongue, swelling of throat tissues, and respiratory distress in '
                    'children and pets.',
    'scientific_name': 'Caladium bicolor (Aiton) Vent.',
    'species': 'bicolor',
    'synonyms': []},
{   'canonical_name': 'Tradescantia zebrina',
    'category': 'ornamental',
    'common_names': ['Inchplant', 'Wandering Dude', 'Silver Inch Plant', 'Zebra Spiderwort'],
    'confusable_species': [   'Tradescantia pallida (Purple Secretia) - entirely solid deep purple leaves with no '
                              'silver stripes',
                              'Commelina benghalensis (Dayflower) - purely green oval leaves with bright blue flowers'],
    'description': 'A trailing succulent-stemmed perennial prized for its iridescent leaves striped with metallic '
                   'silver and deep magenta undersides.',
    'distinguishing_characteristics': 'Succulent creeping stems rooting freely at swollen nodes; alternate clasping '
                                      'ovate leaves with two broad glittering silver longitudinal bands on the upper '
                                      'green surface and deep violet-purple undersides; small 3-petaled bright magenta '
                                      'flowers.',
    'family': 'Commelinaceae',
    'flowering_season': 'Spring to monsoon',
    'genus': 'Tradescantia',
    'growth_type': 'climber',
    'habitat': 'Hanging baskets, window boxes, rockeries, and moist groundcover in Indian homes and gardens',
    'id': 'tradescantia-zebrina',
    'regional_names': {'bn': ['জেব্রিনা (Zebrina)'], 'hi': ['ज़ेब्रिना (Zebrina)']},
    'safety_notes': 'Mild irritant: Plant sap contains microscopic calcium oxalate crystals and can cause skin '
                    'irritation or itching in domestic pets (especially dogs that rub against hanging foliage).',
    'scientific_name': 'Tradescantia zebrina Bosse',
    'species': 'zebrina',
    'synonyms': ['Zebrina pendula']},
{   'canonical_name': 'Tridax procumbens',
    'category': 'wild_grass',
    'common_names': ['Coatbuttons', 'Tridax Daisy', 'Ghamra', 'Jayanti Veda', 'Ghaboot'],
    'confusable_species': [   'Eclipta prostrata (Bhringraj) - ray florets are numerous, tiny, pure white without 3 '
                              'teeth, and leaves are lanceolate',
                              'Parthenium hysterophorus (Congress grass) - tiny white flower heads in clusters and '
                              'fern-like leaves'],
    'description': "An extremely hardy, procumbent daisy-like weed known throughout India as the 'wound healer' due to "
                   "its crushed leaves' remarkable ability to arrest bleeding.",
    'distinguishing_characteristics': 'Creeping hairy stems with ascending branches; opposite coarsely toothed '
                                      'arrow-shaped hairy leaves; solitary daisy heads on very long slender leafless '
                                      'stalks; ray florets 5–6, creamy white or pale yellow with 3 distinct teeth at '
                                      'the apex; central disc florets bright yellow.',
    'family': 'Asteraceae',
    'flowering_season': 'Year-round',
    'genus': 'Tridax',
    'growth_type': 'herb',
    'habitat': 'Ubiquitous along roadsides, railway tracks, pavement cracks, and sunny lawns across all Indian states',
    'id': 'tridax-procumbens',
    'regional_names': {   'bn': ['জয়ন্তী (Jayanti)', 'ত্রিদক্ষ (Tridax)'],
                          'hi': ['घमरा (Ghamra)', 'खल-मूरिया (Khal-muriya)'],
                          'ta': ['வெட்டுக்காயப்பூண்டு (Vettukaya poondu)'],
                          'te': ['గాయపాకు (Gayapaku)']},
    'safety_notes': 'Completely non-toxic. Traditionally crushed as a poultice on fresh cuts and scrapes to stop '
                    'bleeding, with proven antiseptic and hemostatic properties.',
    'scientific_name': 'Tridax procumbens (L.) L.',
    'species': 'procumbens',
    'synonyms': []},
{   'canonical_name': 'Euphorbia hirta',
    'category': 'wild_grass',
    'common_names': ['Asthma Weed', 'Snakeweed', 'Dudhi', 'Dudhiya', 'Baridudhi'],
    'confusable_species': [   'Euphorbia thymifolia (Chhoti Dudhi) - tiny prostrate creeping herb lying flat against '
                              'soil with minute reddish leaves',
                              'Chamaesyce serpens - prostrate smooth stems without hairy reddish coats'],
    'description': 'A very common pantropical hairy weed containing milky latex, famous in Ayurveda and folk medicine '
                   'for treating bronchial asthma and respiratory complaints.',
    'distinguishing_characteristics': 'Hairy reddish-purple stems exuding white milky latex when snapped; opposite '
                                      'elliptic-oblong leaves with serrate edges and purplish blotches in the center; '
                                      'dense, button-like stalked axillary clusters of minute greenish-pink cyathia '
                                      '(flowers).',
    'family': 'Euphorbiaceae',
    'flowering_season': 'Year-round',
    'genus': 'Euphorbia',
    'growth_type': 'herb',
    'habitat': 'Open waste ground, pathway edges, agricultural bunds, and garden beds throughout tropical India',
    'id': 'euphorbia-hirta',
    'regional_names': {   'bn': ['দুধিয়া (Dudhiya)', 'দুধঘাস (Dudhghas)'],
                          'hi': ['दूधी (Dudhi)', 'बड़ी दूधी (Badi Dudhi)'],
                          'ta': ['அம்மான் பச்சரிசி (Amman Pacharisi)'],
                          'te': ['రెడ్డివారి నానుబాలు (Reddivari Nanubalu)']},
    'safety_notes': 'Milky latex can cause mild skin irritation and eye stinging. Widely used in traditional '
                    'decoctions for respiratory ailments, but excessive doses act as an emetic.',
    'scientific_name': 'Euphorbia hirta L.',
    'species': 'hirta',
    'synonyms': []}

]

def get_all_seeded_plants() -> List[Dict[str, Any]]:
    """Return the complete list of verified seeded plant profiles."""
    return PLANTS_SEED_DATA
