from typing import Dict, Any, List
from app.config import HOTSPOT_CITIES, LIFESTYLE_PROFILES
from app.services.aqi_engine import calculate_hourly_inversion_curve, get_aqi_category

def generate_daily_routine(
    city_key: str = "delhi",
    lifestyle_key: str = "toddler_family",
    home_type: str = "apartment",
    heating_source: str = "heat_pump_electric",
    commute_mode: str = "transit",
    has_air_cleaner: bool = True
) -> Dict[str, Any]:
    """
    Generates an optimized, low-emission, health-protective 24-hour routine
    aligned with temperature inversion mechanics and personal family lifestyle.
    """
    city = HOTSPOT_CITIES.get(city_key, HOTSPOT_CITIES["delhi"])
    lifestyle = LIFESTYLE_PROFILES.get(lifestyle_key, LIFESTYLE_PROFILES["toddler_family"])
    hourly_inversion = calculate_hourly_inversion_curve(city_key)

    timeline = []
    
    # 06:00 - 08:00 Early Morning
    timeline.append({
        "time_slot": "06:00 - 08:00 AM",
        "inversion_status": "Severe Ground Inversion Peak (Mixing height ~60-80m)",
        "hazard_level": "Extreme Danger",
        "badge_color": "bg-rose-500/20 text-rose-400 border-rose-500/30",
        "routine_action": "Strict indoor confinement. Seal all external doors and draft cracks.",
        "lifestyle_specific": (
            "Nursery air seal: Keep DIY C-R box or HEPA running on Medium in bedroom. Do NOT open morning balcony doors."
            if "toddler" in lifestyle_key else
            "Cancel any morning outdoor walk or terrace exercises. Cold dry air + PM2.5 triggers severe bronchial spasms in elderly lungs."
            if "elderly" in lifestyle_key else
            "Pre-filter bedroom air. Prepare sealed N95 mask before stepping outside."
        ),
        "low_emission_action": "Avoid electric kettle / high-draw appliances during peak coal-grid morning surge if possible; use clean electric heating rather than wood or gas."
    })

    # 08:00 - 10:00 Morning Commute / School Run
    timeline.append({
        "time_slot": "08:00 - 10:00 AM",
        "inversion_status": "Traffic Rush Hour trapped in cold boundary pool",
        "hazard_level": "High Exposure Risk",
        "badge_color": "bg-red-500/20 text-red-400 border-red-500/30",
        "routine_action": "Enclosed transit with tight N95 mask. Zero idling at school drop-offs.",
        "lifestyle_specific": (
            "Never use open strollers on main roads (exhaust settles at child breathing height 0.5m). Use rain/smog stroller canopy with portable mini-HEPA or vehicle carpool."
            if "toddler" in lifestyle_key else
            "Reschedule medical appointments to after 11:30 AM to bypass the morning smog wall."
            if "elderly" in lifestyle_key else
            "Set car HVAC to 100% Recirculation. If riding metro, keep N95 tightly fitted at station platforms."
        ),
        "low_emission_action": "Join a neighborhood school carpool cluster or ride electric mass transit. Avoid engine idling while waiting."
    })

    # 10:00 - 12:30 Midday Transition
    timeline.append({
        "time_slot": "10:00 AM - 12:30 PM",
        "inversion_status": "Solar heating begins expanding boundary layer mixing",
        "hazard_level": "Moderate Transition",
        "badge_color": "bg-amber-500/20 text-amber-400 border-amber-500/30",
        "routine_action": "Indoor light activities; prepare for midday solar ventilation window.",
        "lifestyle_specific": (
            "Indoor play area: Damp microfiber wipe nursery floors to pick up settled fine dust without resuspending it."
            if "toddler" in lifestyle_key else
            "Gentle indoor stretching or yoga in clean-air room. Maintain hydration to support mucosal cilia clearance."
            if "elderly" in lifestyle_key else
            "Office / indoor workspace: Check if commercial HVAC filters are running; place desk mini-filter if air smells smoky."
        ),
        "low_emission_action": "Run dishwasher or high-efficiency laundry now when solar grid generation is highest."
    })

    # 12:30 - 15:30 Solar Window (Safest Hours)
    timeline.append({
        "time_slot": "12:30 - 03:30 PM",
        "inversion_status": "Inversion Layer Breaks! Maximum Vertical Atmospheric Dilution",
        "hazard_level": "Safest Activity Window of the Day",
        "badge_color": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
        "routine_action": "Brief solar ventilation window (15-20 mins) & essential outdoor errands.",
        "lifestyle_specific": (
            "Safe outdoor window: If AQI is <200, take children out for 20-30 minutes for sunshine and mental wellbeing, away from main arterials."
            if "toddler" in lifestyle_key else
            "Best time for garden time or porch sit. Sun exposure boosts Vitamin D, which regulates respiratory immunity."
            if "elderly" in lifestyle_key else
            "Ideal window for outdoor movement, lunch break, and running outdoor errands."
        ),
        "low_emission_action": "Crack two opposing windows for 15 minutes of cross-ventilation to flush CO2 and VOCs, then reseal tightly before 3:30 PM."
    })

    # 15:30 - 18:00 Late Afternoon & Evening Commute
    timeline.append({
        "time_slot": "03:30 - 06:00 PM",
        "inversion_status": "Solar cooling starts; boundary layer collapses back toward ground",
        "hazard_level": "Escalating Smog Concentration",
        "badge_color": "bg-orange-500/20 text-orange-400 border-orange-500/30",
        "routine_action": "Reseal all windows; turn DIY C-R box back to High.",
        "lifestyle_specific": (
            "Bring children indoors by 3:45 PM before evening temperature inversion traps return commute exhaust."
            if "toddler" in lifestyle_key else
            "Transition into insulated living room; pre-warm room with ceramic heat pump."
            if "elderly" in lifestyle_key else
            "Evening commute: Wear N95. Take rail transit over street buses to avoid idling in gridlock particulate plumes."
        ),
        "low_emission_action": "Combine trips and errands into a single chain rather than cold-starting vehicle multiple times."
    })

    # 18:00 - 21:00 Dinner & Evening Stagnation
    timeline.append({
        "time_slot": "06:00 - 09:00 PM",
        "inversion_status": "Secondary Inversion Peak: Cooking plumes + domestic heating + low wind",
        "hazard_level": "Severe Exposure Risk",
        "badge_color": "bg-red-500/20 text-red-400 border-red-500/30",
        "routine_action": "Culinary emission control. Keep bedroom doors shut.",
        "lifestyle_specific": (
            "Cook with lids on pots; run kitchen exhaust fan; keep toddlers completely out of the kitchen while stove is active."
            if "toddler" in lifestyle_key else
            "Avoid gas burner exposure (NO2 triggers nighttime asthma awakenings). Use electric slow cooker or induction."
            if "elderly" in lifestyle_key else
            "Indoor cardio/workout only in room with operating HEPA/C-R box."
        ),
        "low_emission_action": "Switch cooking to induction cooktop or microwave. If heating, use radiant electric or heat pump rather than wood fireplace or diesel generator."
    })

    # 21:00 - 06:00 Nighttime Sleep Defense
    timeline.append({
        "time_slot": "09:00 PM - 06:00 AM",
        "inversion_status": "Cold Ground Pool Stagnation (Continuous nocturnal inversion)",
        "hazard_level": "Continuous Indoor Seepage Threat",
        "badge_color": "bg-purple-500/20 text-purple-400 border-purple-500/30",
        "routine_action": "Clean-air sleeping sanctuary mode. Low-noise continuous filtration.",
        "lifestyle_specific": (
            "Keep bedroom door closed with DIY C-R box running on Quiet/Low setting. Safe sleep zone PM2.5 < 15 µg/m³."
            if "toddler" in lifestyle_key else
            "Keep saline nasal spray and prescribed reliever inhaler on nightstand. Maintain room temperature at 20-21°C."
            if "elderly" in lifestyle_key else
            "Position air cleaner 4 feet from bedhead, blowing filtered air toward sleep breathing zone."
        ),
        "low_emission_action": "Set thermostat 1-2°C lower and use warm quilts instead of running energy-intensive non-inverter space heaters all night."
    })

    # Sustainable low-emission alternatives tailored to lifestyle
    sustainable_alternatives = [
        {
            "category": "Mobility & School Run",
            "current_habit": "Solo vehicle trips / idling outside school gate",
            "sustainable_alternative": "Neighborhood 'Walking Bus' with N95s or 4-family Electric Carpool Cluster",
            "direct_impact": "Cuts local school gate PM2.5 spike by up to 65% and saves ~3.2 kg CO2 per day."
        },
        {
            "category": "Domestic Heating",
            "current_habit": "Wood-burning fireplace / diesel generator backup during outages",
            "sustainable_alternative": "Reverse-cycle Inverter Heat Pump + Portable LiFePO4 Power Station",
            "direct_impact": "Zero onsite combustion; eliminates 100% of toxic wood-smoke Benzo[a]pyrene and diesel soot from your home perimeter."
        },
        {
            "category": "Indoor Cooking",
            "current_habit": "High-heat open wok frying on unvented LPG gas stove",
            "sustainable_alternative": "Induction cooktop + back-burner rear exhaustion + tight lid simmering",
            "direct_impact": "Prevents 450+ µg/m³ indoor PM2.5 surge and drops toxic NO2 levels to near-zero."
        },
        {
            "category": "Dust Management",
            "current_habit": "Morning dry sweeping with nylon broom",
            "sustainable_alternative": "Damp microfiber electrostatic mopping with water and mild surfactant",
            "direct_impact": "Eliminates 85% of resuspension of toxic heavy-metal particles into children's breathing zone."
        }
    ]

    return {
        "city_name": city["name"],
        "lifestyle_title": lifestyle["title"],
        "vulnerability": lifestyle["vulnerability"],
        "critical_rule": lifestyle["critical_advice"],
        "primary_risk": lifestyle["primary_exposure_risk"],
        "timeline": timeline,
        "sustainable_alternatives": sustainable_alternatives
    }
