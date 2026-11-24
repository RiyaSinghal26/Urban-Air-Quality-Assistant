from typing import Dict, Any, List
from app.config import AIR_STANDARDS

# Mask filtration efficiencies
MASK_EFFICIENCIES = {
    "none": 0.0,
    "cloth": 0.20,
    "surgical": 0.40,
    "kn95": 0.88,
    "n95": 0.96,
    "p100": 0.999
}

# Commute emission factors per passenger-km
COMMUTE_FACTORS = {
    "solo_car": {"co2_g_km": 192.0, "pm25_g_km": 0.12, "nox_g_km": 0.45},
    "carpool": {"co2_g_km": 64.0, "pm25_g_km": 0.04, "nox_g_km": 0.15},
    "bus_transit": {"co2_g_km": 75.0, "pm25_g_km": 0.05, "nox_g_km": 0.22},
    "electric_metro": {"co2_g_km": 28.0, "pm25_g_km": 0.005, "nox_g_km": 0.02},
    "ev": {"co2_g_km": 45.0, "pm25_g_km": 0.015, "nox_g_km": 0.03},
    "walking_cycling": {"co2_g_km": 0.0, "pm25_g_km": 0.0, "nox_g_km": 0.0}
}

def calculate_personal_and_community_impact(
    ambient_pm25: float = 280.0,
    outdoor_hours: float = 2.0,
    mask_type: str = "n95",
    commute_mode: str = "carpool",
    commute_distance_km: float = 15.0,
    baseline_commute_mode: str = "solo_car",
    has_cr_box_or_hepa: bool = True,
    indoor_hours: float = 22.0,
    breathing_rate_m3_h: float = 0.80, # Average adult mixed
    heating_choice: str = "electric_heat_pump", # vs "biomass_firewood" or "diesel_generator"
    community_multiplier: int = 50 # Number of participating community families
) -> Dict[str, Any]:
    """
    Computes rigorous personal lung dose reduction and community emission mitigation.
    """
    mask_eff = MASK_EFFICIENCIES.get(mask_type.lower(), 0.96)
    
    # 1. Unmitigated Scenario (No mask, leaky indoor home, solo driving)
    # Natural building infiltration factor for unsealed home during winter: ~0.70
    unmitigated_indoor_pm25 = ambient_pm25 * 0.70
    
    # Unmitigated Daily PM2.5 Inhalation (micrograms)
    unmit_outdoor_dose = outdoor_hours * ambient_pm25 * 0.0 * breathing_rate_m3_h # (1 - 0.0 mask eff)
    unmit_outdoor_dose = outdoor_hours * ambient_pm25 * (1.0 - 0.0) * breathing_rate_m3_h
    unmit_indoor_dose = (24.0 - outdoor_hours) * unmitigated_indoor_pm25 * breathing_rate_m3_h
    total_unmitigated_dose_ug = unmit_outdoor_dose + unmit_indoor_dose

    # 2. Optimized AuraShield Scenario
    # With sealed drafts and C-R Box / HEPA running: indoor PM2.5 drops to 12-25 µg/m³
    optimized_indoor_pm25 = 18.0 if has_cr_box_or_hepa else unmitigated_indoor_pm25
    
    mitigated_outdoor_dose = outdoor_hours * ambient_pm25 * (1.0 - mask_eff) * breathing_rate_m3_h
    mitigated_indoor_dose = (24.0 - outdoor_hours) * optimized_indoor_pm25 * breathing_rate_m3_h
    total_mitigated_dose_ug = mitigated_outdoor_dose + mitigated_indoor_dose

    # Daily PM2.5 Mass Prevented from Lungs
    pm25_saved_daily_ug = max(0.0, total_unmitigated_dose_ug - total_mitigated_dose_ug)
    pm25_saved_season_mg = round((pm25_saved_daily_ug * 90.0) / 1000.0, 1) # 90-day winter season in mg

    # Berkeley Earth Cigarette Equivalents
    # 1 cigarette equivalent ≈ 22 µg/m³ ambient for 24h at 15 m³/day respiration ≈ 330 µg inhaled
    dose_per_cigarette_ug = 22.0 * 15.0 # 330 µg
    cigs_saved_daily = round(pm25_saved_daily_ug / dose_per_cigarette_ug, 1)
    cigs_saved_weekly = round(cigs_saved_daily * 7.0, 1)
    cigs_saved_season = round(cigs_saved_daily * 90.0, 0)

    # Health Risk Reductions
    pct_reduction = round((pm25_saved_daily_ug / max(total_unmitigated_dose_ug, 1.0)) * 100.0, 1)
    pediatric_er_risk_reduction = min(88.0, round(pct_reduction * 0.92, 1))
    bronchial_inflammation_reduction = min(92.0, round(pct_reduction * 0.95, 1))
    cardiac_stress_drop = min(75.0, round(pct_reduction * 0.78, 1))

    # 3. Community Emissions Mitigated (Daily & Season)
    base_factor = COMMUTE_FACTORS.get(baseline_commute_mode, COMMUTE_FACTORS["solo_car"])
    opt_factor = COMMUTE_FACTORS.get(commute_mode, COMMUTE_FACTORS["carpool"])
    
    # Commute savings per day (2-way trip = 2 * commute_distance_km)
    daily_commute_km = commute_distance_km * 2.0
    co2_saved_commute_g = max(0.0, (base_factor["co2_g_km"] - opt_factor["co2_g_km"]) * daily_commute_km)
    pm25_saved_commute_g = max(0.0, (base_factor["pm25_g_km"] - opt_factor["pm25_g_km"]) * daily_commute_km)
    nox_saved_commute_g = max(0.0, (base_factor["nox_g_km"] - opt_factor["nox_g_km"]) * daily_commute_km)

    # Heating savings
    heating_co2_daily_kg = 0.0
    heating_pm25_daily_g = 0.0
    if heating_choice == "electric_heat_pump":
        # Avoided wood-smoke or diesel generator emissions
        heating_co2_daily_kg = 8.5 # kg CO2 avoided vs unoptimized fuel
        heating_pm25_daily_g = 18.0 # grams of ground-level toxic PM2.5 completely avoided
    elif heating_choice == "radiant_electric":
        heating_co2_daily_kg = 4.2
        heating_pm25_daily_g = 14.0

    total_co2_saved_daily_kg = round((co2_saved_commute_g / 1000.0) + heating_co2_daily_kg, 2)
    total_pm25_emissions_saved_daily_g = round(pm25_saved_commute_g + heating_pm25_daily_g, 2)
    total_nox_saved_daily_g = round(nox_saved_commute_g + (heating_pm25_daily_g * 1.8), 2)

    # 4. Community Ripple Multiplier
    community_co2_season_tons = round((total_co2_saved_daily_kg * 90.0 * community_multiplier) / 1000.0, 2)
    community_pm25_season_kg = round((total_pm25_emissions_saved_daily_g * 90.0 * community_multiplier) / 1000.0, 2)
    community_cigs_spared = int(cigs_saved_season * community_multiplier)

    return {
        "personal_metrics": {
            "pm25_saved_daily_ug": round(pm25_saved_daily_ug, 1),
            "pm25_saved_season_mg": pm25_saved_season_mg,
            "cigarette_equivalent_daily": cigs_saved_daily,
            "cigarette_equivalent_weekly": cigs_saved_weekly,
            "cigarette_equivalent_season": int(cigs_saved_season),
            "total_exposure_reduction_pct": pct_reduction,
            "pediatric_er_risk_reduction_pct": pediatric_er_risk_reduction,
            "bronchial_inflammation_reduction_pct": bronchial_inflammation_reduction,
            "cardiac_stress_drop_pct": cardiac_stress_drop,
            "unmitigated_dose_ug": round(total_unmitigated_dose_ug, 1),
            "optimized_dose_ug": round(total_mitigated_dose_ug, 1),
            "indoor_pm25_achieved": optimized_indoor_pm25
        },
        "community_emissions_mitigated": {
            "daily_co2_saved_kg": total_co2_saved_daily_kg,
            "season_co2_saved_kg": round(total_co2_saved_daily_kg * 90.0, 1),
            "daily_pm25_emissions_saved_g": total_pm25_emissions_saved_daily_g,
            "season_pm25_emissions_saved_g": round(total_pm25_emissions_saved_daily_g * 90.0, 1),
            "daily_nox_saved_g": total_nox_saved_daily_g
        },
        "community_ripple": {
            "participating_households": community_multiplier,
            "community_co2_season_tons": community_co2_season_tons,
            "community_pm25_season_kg": community_pm25_season_kg,
            "community_cigarettes_spared": community_cigs_spared,
            "neighborhood_ambient_pm25_reduction_estimate": f"~{min(28.0, round(community_multiplier * 0.045, 1))} µg/m³ local curb-level drop"
        }
    }
