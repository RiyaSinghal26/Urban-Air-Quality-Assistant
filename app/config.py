import os
from typing import Dict, Any, List

# Core configuration for AuraShield AI
APP_TITLE = "AuraShield AI: Winter Smog & Urban Air Pollution Navigator"
APP_SUBTITLE = "GenAI-Powered Urban Air Defense, Low-Emission Daily Routines & Community Action"
VERSION = "2.0.0"

# WHO and EPA Ambient Air Quality Standards
AIR_STANDARDS = {
    "WHO_PM25_ANNUAL": 5.0,     # µg/m³
    "WHO_PM25_24H": 15.0,       # µg/m³
    "EPA_PM25_24H_GOOD": 12.0,  # µg/m³
    "BERKELEY_CIGARETTE_PM25_24H": 22.0  # µg/m³ daily average ≈ 1 cigarette
}

# Major Winter Smog Hotspot Cities with typical winter meteorological profiles
HOTSPOT_CITIES: Dict[str, Dict[str, Any]] = {
    "delhi": {
        "name": "Delhi NCR, India",
        "country": "India",
        "lat": 28.6139,
        "lon": 77.2090,
        "base_aqi": 385,
        "primary_smog_driver": "Crop stubble burning, low wind speed, nocturnal temperature inversion & vehicular NOx",
        "inversion_severity": "Extreme (Ground boundary layer drops to 60-100m)",
        "safest_window": "1:00 PM - 3:30 PM",
        "peak_hazard_window": "6:00 AM - 10:00 AM & 8:30 PM - 1:00 AM",
        "baseline_pm25": 290.0,
        "baseline_pm10": 420.0,
        "baseline_no2": 85.0
    },
    "lahore": {
        "name": "Lahore, Pakistan",
        "country": "Pakistan",
        "lat": 31.5204,
        "lon": 74.3587,
        "base_aqi": 410,
        "primary_smog_driver": "Brick kilns, low-grade fuel combustion, transboundary haze & severe winter stagnant air",
        "inversion_severity": "Severe (Dense yellow-gray haze ceiling at 80m)",
        "safest_window": "1:30 PM - 3:30 PM",
        "peak_hazard_window": "6:30 AM - 10:30 AM & 8:00 PM - 2:00 AM",
        "baseline_pm25": 330.0,
        "baseline_pm10": 480.0,
        "baseline_no2": 95.0
    },
    "salt_lake_city": {
        "name": "Salt Lake City, Utah, USA",
        "country": "United States",
        "lat": 40.7608,
        "lon": -111.8910,
        "base_aqi": 165,
        "primary_smog_driver": "Orographic cold-air pool (CAP) mountain valley inversion trapping mobile and wood-smoke emissions",
        "inversion_severity": "High (Multi-day bowl inversion capped by warm Pacific ridge)",
        "safest_window": "1:00 PM - 4:00 PM",
        "peak_hazard_window": "7:00 AM - 9:30 AM & 6:00 PM - 10:00 PM",
        "baseline_pm25": 78.0,
        "baseline_pm10": 95.0,
        "baseline_no2": 45.0
    },
    "london": {
        "name": "London, United Kingdom",
        "country": "United Kingdom",
        "lat": 51.5074,
        "lon": -0.1278,
        "base_aqi": 95,
        "primary_smog_driver": "Domestic wood-burning stoves, diesel soot & calm high-pressure winter anticyclones",
        "inversion_severity": "Moderate (Thames valley shallow radiation inversions)",
        "safest_window": "11:30 AM - 3:30 PM",
        "peak_hazard_window": "7:30 AM - 9:30 AM & 6:00 PM - 9:30 PM",
        "baseline_pm25": 34.0,
        "baseline_pm10": 52.0,
        "baseline_no2": 58.0
    },
    "beijing": {
        "name": "Beijing, China",
        "country": "China",
        "lat": 39.9042,
        "lon": 116.4074,
        "base_aqi": 195,
        "primary_smog_driver": "Regional winter district heating, industrial sulfur/nitrogen secondary aerosols & calm southerly winds",
        "inversion_severity": "High (Yanshan-Taihang mountain basin block)",
        "safest_window": "12:00 PM - 3:00 PM",
        "peak_hazard_window": "6:30 AM - 9:30 AM & 7:00 PM - 11:30 PM",
        "baseline_pm25": 115.0,
        "baseline_pm10": 160.0,
        "baseline_no2": 62.0
    },
    "krakow": {
        "name": "Krakow, Poland",
        "country": "Poland",
        "lat": 50.0647,
        "lon": 19.9450,
        "base_aqi": 175,
        "primary_smog_driver": "Suburban coal/wood 'smokers' (boilers), Vistula river valley basin trapping benzo(a)pyrene",
        "inversion_severity": "High (River valley bowl trapping ground smoke)",
        "safest_window": "12:30 PM - 3:30 PM",
        "peak_hazard_window": "7:00 AM - 10:00 AM & 6:30 PM - 11:00 PM",
        "baseline_pm25": 88.0,
        "baseline_pm10": 130.0,
        "baseline_no2": 48.0
    },
    "milan": {
        "name": "Milan / Po Valley, Italy",
        "country": "Italy",
        "lat": 45.4642,
        "lon": 9.1900,
        "base_aqi": 155,
        "primary_smog_driver": "Po Valley Alpine enclosure, thermal inversion, agricultural ammonia + traffic NOx ammonium nitrate secondary aerosols",
        "inversion_severity": "High (Persistent multi-week low wind stagnation)",
        "safest_window": "1:00 PM - 4:00 PM",
        "peak_hazard_window": "7:00 AM - 9:30 AM & 7:00 PM - 10:30 PM",
        "baseline_pm25": 68.0,
        "baseline_pm10": 98.0,
        "baseline_no2": 54.0
    }
}

# Lifestyle Profiles
LIFESTYLE_PROFILES: Dict[str, Dict[str, Any]] = {
    "toddler_family": {
        "title": "Family with Newborns / Toddlers",
        "vulnerability": "Extreme (Lungs still forming, breaths 2x faster per kg body weight)",
        "critical_advice": "Never take stroller out before 11 AM; avoid floor-level dust agitation; seal nursery door bottom; deploy DIY Corsi-Rosenthal box 24/7.",
        "breathing_rate": 0.65, # m3/hr relative equivalent
        "typical_commute": "School runs / preschool drop-off",
        "primary_exposure_risk": "Early morning drop-off exhaust plumes at child stroller height (0.5m)"
    },
    "elderly_asthma": {
        "title": "Multigenerational / Elderly with Asthma/COPD",
        "vulnerability": "Severe (High acute risk for bronchospasm, arrhythmia, and stroke from PM2.5 entering bloodstream)",
        "critical_advice": "Strict cancellation of morning walks; pre-medicate inhalers before essential transit; wet-wipe all living spaces; clean indoor air bubble.",
        "breathing_rate": 0.55,
        "typical_commute": "Medical appointments, pharmacy visits, localized shopping",
        "primary_exposure_risk": "Morning cold air + particulate shock inducing bronchial constriction"
    },
    "daily_commuter": {
        "title": "Urban Commuter (Car / Bike / Public Transit)",
        "vulnerability": "High (Direct exposure to high-concentration street canyons, diesel soot, tire wear)",
        "critical_advice": "Switch car HVAC to 100% Recirculation mode; add HEPA cabin filter; wear fit-tested N95 during transit; shift departure time to after 10 AM.",
        "breathing_rate": 1.15,
        "typical_commute": "1-2 hours daily in heavy highway and urban traffic",
        "primary_exposure_risk": "Tunnel and intersection exhaust tunnels, ultrafine black carbon"
    },
    "budget_renter": {
        "title": "Budget-Conscious Apartment Renter / Student",
        "vulnerability": "Moderate to High (Leaky single-pane windows, central un-filtered ductwork, limited funds)",
        "critical_advice": "Build $35 DIY Corsi-Rosenthal fan box; install $4 plastic weather seal shrink wrap on windows; crack window only 1:30-2:30 PM; towel-seal hallway door.",
        "breathing_rate": 0.70,
        "typical_commute": "Walking / public transit / shared rides",
        "primary_exposure_risk": "Apartment infiltration from drafty windows and corridor smoke drift"
    },
    "active_athlete": {
        "title": "Outdoor Fitness Enthusiast / Runner",
        "vulnerability": "Very High during workouts (Breathing rate jumps 400%, bypasses nasal filtration directly to deep alveoli)",
        "critical_advice": "Move all cardio workouts indoors next to a running HEPA/CR-box; if outdoors, strictly restrict to 1:30 PM - 3:30 PM when inversion ceiling is maximum.",
        "breathing_rate": 3.0,
        "typical_commute": "Active transport / cycling / outdoor jogs",
        "primary_exposure_risk": "Extreme deep-lung particle deposition during vigorous respiration"
    }
}
