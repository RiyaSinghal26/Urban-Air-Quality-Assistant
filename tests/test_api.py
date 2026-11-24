import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.aqi_engine import (
    get_aqi_category, calculate_hourly_inversion_curve, get_current_smog_status
)
from app.services.iaq_hacks import (
    calculate_corsi_rosenthal_box, get_all_iaq_hacks, get_mask_comparison_data
)
from app.services.routine_planner import generate_daily_routine
from app.services.impact_calculator import calculate_personal_and_community_impact
from app.services.community_watch import (
    get_community_dashboard, add_community_pledge, report_smog_incident
)
from app.services.genai_assistant import generate_local_cognitive_response

client = TestClient(app)

def test_aqi_categories():
    """Verifies standard WHO/EPA AQI color and category bands."""
    assert get_aqi_category(25)["level"] == "Good"
    assert get_aqi_category(75)["level"] == "Moderate"
    assert get_aqi_category(125)["level"] == "Unhealthy for Sensitive Groups"
    assert get_aqi_category(175)["level"] == "Unhealthy"
    assert get_aqi_category(250)["level"] == "Very Unhealthy"
    assert "Emergency" in get_aqi_category(420)["level"]

def test_hourly_inversion_curve():
    """Verifies that midday hours have higher mixing heights and lower ground PM2.5 than morning hours."""
    curve = calculate_hourly_inversion_curve("delhi")
    assert len(curve) == 24
    
    morning_pm25 = curve[7]["pm25"] # 7 AM
    afternoon_pm25 = curve[14]["pm25"] # 2 PM
    morning_inversion_h = curve[7]["inversion_height_meters"]
    afternoon_inversion_h = curve[14]["inversion_height_meters"]

    # Midday solar heating breaks inversion layer: height rises, ground PM2.5 falls
    assert afternoon_inversion_h > morning_inversion_h
    assert morning_pm25 > afternoon_pm25

def test_corsi_rosenthal_box_calculation():
    """Verifies physics of CADR, ACH, and cost savings."""
    res = calculate_corsi_rosenthal_box(
        fan_size_inches=20,
        filter_count=4,
        filter_thickness_inches=2,
        room_sqft=350,
        ceiling_height_ft=8.5,
        fan_speed="medium"
    )
    assert res["effective_cadr_cfm"] > 400.0
    assert res["ach"] >= 5.0
    assert res["total_diy_cost_usd"] < 100.0
    assert res["savings_usd"] > 350.0
    assert len(res["step_by_step_instructions"]) == 5

def test_routine_generator():
    """Verifies daily timeline and low-emission sustainable alternatives."""
    routine = generate_daily_routine(
        city_key="delhi",
        lifestyle_key="toddler_family",
        home_type="apartment",
        heating_source="heat_pump_electric",
        commute_mode="transit",
        has_air_cleaner=True
    )
    assert len(routine["timeline"]) >= 6
    assert len(routine["sustainable_alternatives"]) == 4
    assert "toddler" in routine["lifestyle_title"].lower() or "newborn" in routine["lifestyle_title"].lower()

def test_impact_calculator():
    """Verifies personal lung dose spared and Berkeley Earth cigarette calculations."""
    impact = calculate_personal_and_community_impact(
        ambient_pm25=280.0,
        outdoor_hours=2.0,
        mask_type="n95",
        commute_mode="carpool",
        commute_distance_km=15.0,
        has_cr_box_or_hepa=True,
        community_multiplier=50
    )
    p = impact["personal_metrics"]
    c = impact["community_ripple"]

    assert p["pm25_saved_daily_ug"] > 1000.0
    assert p["cigarette_equivalent_daily"] > 5.0
    assert p["total_exposure_reduction_pct"] > 75.0
    assert c["community_co2_season_tons"] > 10.0
    assert c["community_cigarettes_spared"] > 10000

def test_community_watch():
    """Verifies pledge submission and incident logging."""
    pledge = add_community_pledge("Test User", "Test City", "DIY Air Cleaners", "Built 2 C-R boxes")
    assert pledge["name"] == "Test User"
    
    incident = report_smog_incident("Leaf Burning", "Park Road", "High", "Heavy smoke")
    assert incident["type"] == "Leaf Burning"

    dash = get_community_dashboard()
    assert len(dash["pledges"]) >= 1
    assert len(dash["incidents"]) >= 1

def test_genai_local_cognitive_engine():
    """Verifies local GenAI synthesizer responses for key smog domains."""
    cr_resp = generate_local_cognitive_response("How to build a Corsi Rosenthal box?", "engineer_bob")
    assert "Corsi-Rosenthal" in cr_resp
    assert "shroud" in cr_resp.lower()

    toddler_resp = generate_local_cognitive_response("How to protect my baby from smog?", "dr_vayu")
    assert "Pediatric" in toddler_resp
    assert "stroller" in toddler_resp.lower()

    mask_resp = generate_local_cognitive_response("Is cloth mask ok for PM2.5?", "dr_vayu")
    assert "N95" in mask_resp

def test_fastapi_endpoints():
    """Verifies all REST API routes via TestClient."""
    # 1. UI Root
    res = client.get("/")
    assert res.status_code == 200
    assert "AuraShield AI" in res.text

    # 2. System Status
    res = client.get("/api/status")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # 3. Current Smog Telemetry
    res = client.get("/api/smog/current?city=delhi")
    assert res.status_code == 200
    data = res.json()
    assert "aqi" in data
    assert len(data["hourly_forecast"]) == 24

    # 4. Generate Routine Endpoint
    res = client.post("/api/routine/generate", json={
        "city_key": "delhi",
        "lifestyle_key": "daily_commuter",
        "home_type": "apartment",
        "heating_source": "heat_pump_electric",
        "commute_mode": "transit",
        "has_air_cleaner": True
    })
    assert res.status_code == 200
    assert "timeline" in res.json()

    # 5. C-R Box Calculator Endpoint
    res = client.post("/api/iaq/cr-box-calc", json={
        "fan_size_inches": 20,
        "filter_count": 4,
        "filter_thickness_inches": 2,
        "room_sqft": 400.0,
        "ceiling_height_ft": 9.0,
        "fan_speed": "high"
    })
    assert res.status_code == 200
    assert res.json()["effective_cadr_cfm"] > 400

    # 6. IAQ Hacks Endpoint
    res = client.get("/api/iaq/hacks")
    assert res.status_code == 200
    assert len(res.json()["hacks"]) >= 5

    # 7. Impact Simulator Endpoint
    res = client.post("/api/impact/calculate", json={
        "ambient_pm25": 300.0,
        "outdoor_hours": 3.0,
        "mask_type": "n95",
        "commute_mode": "carpool",
        "commute_distance_km": 20.0,
        "baseline_commute_mode": "solo_car",
        "has_cr_box_or_hepa": True,
        "indoor_hours": 21.0,
        "heating_choice": "electric_heat_pump",
        "community_multiplier": 100
    })
    assert res.status_code == 200
    assert "personal_metrics" in res.json()

    # 8. GenAI Chat Endpoint
    res = client.post("/api/assistant/chat", json={
        "prompt": "What is the safest hour to open windows during winter smog?",
        "persona_key": "engineer_bob"
    })
    assert res.status_code == 200
    assert "response" in res.json()
