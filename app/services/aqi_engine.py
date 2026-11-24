import math
import random
from datetime import datetime
from typing import Dict, Any, List
from app.config import HOTSPOT_CITIES, AIR_STANDARDS

def get_aqi_category(aqi_value: float) -> Dict[str, str]:
    """Returns standardized AQI category, color code, and health warning."""
    if aqi_value <= 50:
        return {
            "level": "Good",
            "color": "#10B981", # Emerald
            "badge": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
            "health_advice": "Air quality is considered satisfactory, and air pollution poses little or no risk.",
            "urgency": "Normal"
        }
    elif aqi_value <= 100:
        return {
            "level": "Moderate",
            "color": "#FBBF24", # Amber
            "badge": "bg-amber-500/20 text-amber-400 border-amber-500/30",
            "health_advice": "Acceptable air quality; however, sensitive individuals may experience minor symptoms.",
            "urgency": "Caution"
        }
    elif aqi_value <= 150:
        return {
            "level": "Unhealthy for Sensitive Groups",
            "color": "#F97316", # Orange
            "badge": "bg-orange-500/20 text-orange-400 border-orange-500/30",
            "health_advice": "Members of sensitive groups (children, elderly, asthmatics) should limit prolonged outdoor exertion.",
            "urgency": "Warning"
        }
    elif aqi_value <= 200:
        return {
            "level": "Unhealthy",
            "color": "#EF4444", # Red
            "badge": "bg-red-500/20 text-red-400 border-red-500/30",
            "health_advice": "Everyone may begin to experience health effects. Wear N95 outdoors, keep indoor air purified.",
            "urgency": "High Alert"
        }
    elif aqi_value <= 300:
        return {
            "level": "Very Unhealthy",
            "color": "#A855F7", # Purple
            "badge": "bg-purple-500/20 text-purple-400 border-purple-500/30",
            "health_advice": "Health alert: The risk of health effects is substantially increased for everyone. Avoid outdoor activity.",
            "urgency": "Severe Alert"
        }
    else:
        return {
            "level": "Hazardous / Severe Smog Emergency",
            "color": "#881337", # Dark Maroon / Crimson
            "badge": "bg-rose-950 text-rose-300 border-rose-700 animate-pulse",
            "health_advice": "Emergency condition: The entire population is more likely to be affected. Close all drafts, run air filtration continuously.",
            "urgency": "CRITICAL EMERGENCY"
        }

def calculate_hourly_inversion_curve(city_key: str, custom_base_aqi: float = None) -> List[Dict[str, Any]]:
    """
    Simulates a 24-hour diurnal profile of boundary layer inversion height and ground PM2.5/AQI.
    Physics:
    - Radiative cooling at night produces a shallow thermal inversion layer (lowest ~06:00-08:00 AM).
    - Emissions trapped near surface cause early morning peak PM2.5.
    - Solar insolation heats ground around midday, breaking the inversion layer (~13:00-15:30).
    - Evening traffic and cooling reform the inversion, causing second peak ~20:00-23:00.
    """
    city = HOTSPOT_CITIES.get(city_key, HOTSPOT_CITIES["delhi"])
    base_aqi = custom_base_aqi if custom_base_aqi is not None else city["base_aqi"]
    base_pm25 = city["baseline_pm25"] * (base_aqi / city["base_aqi"])

    hourly_data = []
    for hour in range(24):
        # Hourly Diurnal Multiplier for Ground Trapped Particulate
        # Low mixing height in morning (06-09) -> multiplier 1.25 to 1.45
        # High mixing height in afternoon (12-16) -> multiplier 0.45 to 0.65
        # Evening stagnation (19-23) -> multiplier 1.15 to 1.35
        if 0 <= hour < 5:
            mult = 1.15 + 0.1 * math.sin(hour / 5.0 * math.pi)
            inversion_m = 120 - hour * 8
        elif 5 <= hour < 10:
            # Morning peak smog inversion trap
            mult = 1.35 + 0.15 * math.sin((hour - 5) / 5.0 * math.pi)
            inversion_m = 80 - 15 * math.cos((hour - 5) / 4.0 * math.pi)
        elif 10 <= hour < 16:
            # Solar heating breaks inversion, vertical mixing increases
            solar_peak = math.sin((hour - 10) / 6.0 * math.pi)
            mult = 1.2 - 0.65 * solar_peak
            inversion_m = 150 + 650 * solar_peak
        elif 16 <= hour < 20:
            # Sunset, cooling starts, mixing height collapses
            mult = 0.75 + 0.4 * ((hour - 16) / 4.0)
            inversion_m = 450 - 320 * ((hour - 16) / 4.0)
        else:
            # Late night cold pool
            mult = 1.20 + 0.15 * math.sin((hour - 20) / 4.0 * math.pi)
            inversion_m = 110 - 20 * math.sin((hour - 20) / 4.0 * math.pi)

        # Apply realistic hourly variation
        curr_aqi = max(20.0, round(base_aqi * mult, 1))
        curr_pm25 = max(5.0, round(base_pm25 * mult, 1))
        curr_pm10 = round(curr_pm25 * 1.55, 1)
        curr_no2 = round(city["baseline_no2"] * (0.6 + 0.5 * mult), 1)

        is_safe_window = (12 <= hour <= 15) and (curr_aqi < base_aqi * 0.85)

        time_str = f"{hour:02d}:00"
        cat = get_aqi_category(curr_aqi)

        hourly_data.append({
            "hour": hour,
            "time_label": time_str,
            "aqi": curr_aqi,
            "pm25": curr_pm25,
            "pm10": curr_pm10,
            "no2": curr_no2,
            "inversion_height_meters": max(50, round(inversion_m)),
            "is_safe_window": is_safe_window,
            "level": cat["level"],
            "color": cat["color"],
            "recommendation": "Safest ventilation window" if is_safe_window else ("Extreme inversion trap - stay indoors" if mult > 1.3 else "Moderate outdoor caution")
        })

    return hourly_data

def get_current_smog_status(city_key: str, custom_aqi: float = None) -> Dict[str, Any]:
    """Retrieves current simulated meteorological and smog condition for a location."""
    city = HOTSPOT_CITIES.get(city_key, HOTSPOT_CITIES["delhi"])
    now = datetime.now()
    curr_hour = now.hour

    hourly = calculate_hourly_inversion_curve(city_key, custom_aqi)
    current_hour_data = hourly[curr_hour]

    cat = get_aqi_category(current_hour_data["aqi"])

    # Berkeley Earth cigarette equivalent for current PM2.5 over 24h
    cigs_equiv_24h = round(current_hour_data["pm25"] / AIR_STANDARDS["BERKELEY_CIGARETTE_PM25_24H"], 1)

    return {
        "city_key": city_key,
        "city_name": city["name"],
        "country": city["country"],
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "current_hour": curr_hour,
        "aqi": current_hour_data["aqi"],
        "pm25": current_hour_data["pm25"],
        "pm10": current_hour_data["pm10"],
        "no2": current_hour_data["no2"],
        "inversion_height_meters": current_hour_data["inversion_height_meters"],
        "category": cat["level"],
        "color": cat["color"],
        "badge": cat["badge"],
        "urgency": cat["urgency"],
        "health_advice": cat["health_advice"],
        "cigarette_equivalent_24h": cigs_equiv_24h,
        "primary_smog_driver": city["primary_smog_driver"],
        "inversion_severity": city["inversion_severity"],
        "safest_window": city["safest_window"],
        "peak_hazard_window": city["peak_hazard_window"],
        "hourly_forecast": hourly
    }
