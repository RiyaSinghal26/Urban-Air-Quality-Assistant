from typing import Dict, Any, List

def calculate_corsi_rosenthal_box(
    fan_size_inches: int = 20,
    filter_count: int = 4,
    filter_thickness_inches: int = 2,
    room_sqft: float = 350.0,
    ceiling_height_ft: float = 8.5,
    fan_speed: str = "medium"
) -> Dict[str, Any]:
    """
    Calculates CADR (Clean Air Delivery Rate), ACH (Air Changes per Hour),
    cost breakdown, and comparison against commercial HEPA purifiers.
    
    Physics:
    - 20" box fan on medium pushes ~1200-1400 CFM free air.
    - Adding 4x MERV 13 filters in a cube drastically reduces backpressure compared to 1 filter!
    - 2" thick filters have 2.5x the surface area of 1" filters, reducing face velocity and resistance.
    - Adding a 14-15" circular cardboard shroud increases airflow by 20-25% by preventing vortex recirculation.
    """
    speed_factors = {
        "low": 0.65,
        "medium": 0.85,
        "high": 1.05
    }
    speed_mult = speed_factors.get(fan_speed.lower(), 0.85)
    
    thickness_mult = 1.18 if filter_thickness_inches >= 2 else 1.0
    filter_count_mult = 1.0 if filter_count >= 4 else 0.72 # 4-filter cube vs 1-filter taped
    
    base_cadr_cfm = 520.0 # Standard 4-filter 20" CR-box with shroud
    effective_cadr = round(base_cadr_cfm * speed_mult * thickness_mult * (filter_count / 4.0), 1)
    
    room_volume_cuft = room_sqft * ceiling_height_ft
    ach = round((effective_cadr * 60.0) / room_volume_cuft, 2)
    
    # Time to reduce indoor PM2.5 by 90% (based on exponential decay equation: t = -ln(0.10) / ACH hours)
    clean_time_minutes = round((2.3026 / max(ach, 0.1)) * 60.0, 1) if ach > 0 else 999
    
    # Cost Comparison
    fan_cost = 25.0
    filter_unit_cost = 14.0 if filter_thickness_inches >= 2 else 9.0
    filters_total = filter_unit_cost * filter_count
    duct_tape_cost = 6.0
    total_diy_cost = round(fan_cost + filters_total + duct_tape_cost, 2)
    
    # Comparable commercial HEPA unit (500 CFM CADR requires 2-3 units like Coway or Blueair, ~$450-$700)
    commercial_equiv_cost = 520.0
    savings = round(commercial_equiv_cost - total_diy_cost, 2)
    
    return {
        "fan_size_inches": fan_size_inches,
        "filter_count": filter_count,
        "filter_thickness_inches": filter_thickness_inches,
        "room_sqft": room_sqft,
        "ceiling_height_ft": ceiling_height_ft,
        "fan_speed": fan_speed,
        "effective_cadr_cfm": effective_cadr,
        "ach": ach,
        "ach_rating": "Medical / Wildfire Grade (Optimal)" if ach >= 6.0 else ("Excellent Protection" if ach >= 4.0 else ("Adequate" if ach >= 2.5 else "Underpowered for Room Size")),
        "clean_90pct_time_mins": clean_time_minutes,
        "total_diy_cost_usd": total_diy_cost,
        "commercial_equivalent_cost_usd": commercial_equiv_cost,
        "savings_usd": savings,
        "power_consumption_watts": 45 if fan_speed == "low" else (65 if fan_speed == "medium" else 90),
        "filter_lifespan_months": 5 if filter_thickness_inches >= 2 else 3,
        "step_by_step_instructions": [
            "Step 1: Place the 20-inch box fan flat, facing upward (air will blow toward ceiling).",
            "Step 2: Position 4x MERV 13 filters vertically around the four perimeter edges of the fan with arrows pointing INWARD toward the fan center.",
            "Step 3: Tape all vertical seams tightly using duct tape or painters tape to eliminate unfiltered leaks.",
            "Step 4: Cut a 20x20-inch piece of cardboard for the bottom base and tape it securely to seal the cube.",
            "Step 5: CRITICAL EFFICIENCY HACK - The Shroud: Cut a circular hole (approx. 14-15 inches diameter) out of cardboard and tape it to the front face of the box fan. This prevents corner vortex backflow and boosts airflow output by 20%!"
        ]
    }

def get_all_iaq_hacks() -> List[Dict[str, Any]]:
    """Returns curated, science-validated indoor air quality hacks and protocols."""
    return [
        {
            "id": "cr_box",
            "title": "DIY Corsi-Rosenthal (C-R) Box Purifier",
            "category": "Filtration Hardware",
            "impact_rating": "5/5 Stars",
            "cost": "$45 - $80",
            "summary": "High-volume MERV-13 air cleaner that out-cleans $500 commercial HEPA units at a fraction of the cost.",
            "science": "Provides 450-550 CFM CADR because 4 filters drastically reduce air resistance compared to single-filter purifiers.",
            "best_practice": "Run on Medium speed continuously during smog inversions. Place in central living space 2 feet from walls."
        },
        {
            "id": "inversion_ventilation",
            "title": "Solar-Window Aeration Protocol",
            "category": "Ventilation Timing",
            "impact_rating": "4.5/5 Stars",
            "cost": "Free",
            "summary": "Never open windows in the early morning (6-10 AM). Only ventilate between 1:00 PM and 3:30 PM for 15-20 minutes.",
            "science": "Ground inversion layers break down around midday due to solar heating of the earth's surface, creating a temporary vertical chimney of cleaner air.",
            "best_practice": "Crack two opposing windows for a brief cross-breeze between 1:15 PM and 2:00 PM, then immediately reseal and blast air cleaner on High for 20 minutes."
        },
        {
            "id": "wet_cleaning",
            "title": "Microfiber Wet-Mopping vs. Dry Sweeping",
            "category": "Cleaning Method",
            "impact_rating": "4/5 Stars",
            "cost": "$5 - $10",
            "summary": "Strictly ban dry brooms, feather dusters, and unsealed vacuums during severe smog episodes.",
            "science": "Dry sweeping resuspends deposited toxic PM10 and PM2.5 directly into the human breathing zone, increasing inhalable indoor particulate by 300%.",
            "best_practice": "Use damp microfiber cloths and flat wet mops. Add a drop of mild liquid soap to lower surface tension and trap ultra-fine soot."
        },
        {
            "id": "kitchen_exhaust",
            "title": "Culinary Emission Suppression",
            "category": "Indoor Source Control",
            "impact_rating": "4.5/5 Stars",
            "cost": "Free",
            "summary": "Cooking generates massive spikes of PM2.5 and NOx. Lid cooking and back-burner hood exhaustion are vital.",
            "science": "Frying and open gas burners can spike indoor PM2.5 past 600 µg/m³ within 15 minutes, rivaling severe outdoor smog.",
            "best_practice": "Cook on the rear burners where range hoods capture 70% more plume; keep lids on pans; switch to electric induction or pressure cookers."
        },
        {
            "id": "draft_proofing",
            "title": "DIY Draft Snake & Window Film Sealing",
            "category": "Building Envelope",
            "impact_rating": "4/5 Stars",
            "cost": "$10 - $25",
            "summary": "Seal external door thresholds and leaky window frames with homemade towel draft snakes and removable foam tape.",
            "science": "Thermal stack effect draws cold, heavily polluted outside air through door bottoms and window sash cracks like a vacuum.",
            "best_practice": "Roll heavy damp bath towels along exterior door bottoms. Apply removable blue painter's tape along leaky sliding window joints."
        },
        {
            "id": "mask_filtration",
            "title": "Respiratory Protection Seal Hierarchy",
            "category": "Personal Protection",
            "impact_rating": "5/5 Stars",
            "cost": "$1 - $3 per mask",
            "summary": "Understand that cloth masks filter <25% of PM2.5; certified N95 / FFP2 with tight seal is mandatory.",
            "science": "PM2.5 particles are 0.3-2.5 micrometers in aerodynamic diameter. Only electrostatic meltblown non-woven fibers trap them efficiently.",
            "best_practice": "Perform a fit check: breathe in sharply; the mask should collapse inward slightly without leaking air around the bridge of the nose."
        },
        {
            "id": "plant_reality",
            "title": "Houseplants: Myth vs. Scientific Reality",
            "category": "Scientific Education",
            "impact_rating": "2/5 Stars (for PM2.5)",
            "cost": "Variable",
            "summary": "Houseplants do NOT filter PM2.5 particulate matter and can increase indoor mold spores if overwatered.",
            "science": "NASA clean air studies examined VOCs in sealed miniature chambers, not particulate matter in open rooms. You would need 1,000 plants per room to equal one small HEPA filter.",
            "best_practice": "Enjoy houseplants for aesthetic and humidity balance, but NEVER rely on them to clean winter smog. Depend on mechanical MERV/HEPA filtration."
        }
    ]

def get_mask_comparison_data() -> List[Dict[str, Any]]:
    """Returns comparative data on mask types against winter PM2.5 pollution."""
    return [
        {
            "type": "Bandana / Cloth Scarf",
            "pm25_efficiency": 18,
            "seal_quality": "Very Poor",
            "leakage_rate": "80%+",
            "verdict": "Ineffective against toxic smog. Provides false sense of security."
        },
        {
            "type": "Standard Surgical Mask",
            "pm25_efficiency": 38,
            "seal_quality": "Poor (Side gaps)",
            "leakage_rate": "60%",
            "verdict": "Designed to stop outbound droplets, not inbound aerosolized fine PM2.5."
        },
        {
            "type": "KN95 / KF94 (Ear-loop)",
            "pm25_efficiency": 88,
            "seal_quality": "Moderate to Good",
            "leakage_rate": "10 - 15%",
            "verdict": "Solid everyday protection; ensure nose wire is molded firmly."
        },
        {
            "type": "N95 / FFP2 (Headband)",
            "pm25_efficiency": 96,
            "seal_quality": "Excellent",
            "leakage_rate": "< 5%",
            "verdict": "Gold standard for smog commutes and outdoor transit."
        },
        {
            "type": "Elastomeric Respirator (P100 / N100)",
            "pm25_efficiency": 99.9,
            "seal_quality": "Airtight Silicone Seal",
            "leakage_rate": "< 0.5%",
            "verdict": "Maximum protection for high-risk individuals, cyclists, and traffic officers."
        }
    ]
