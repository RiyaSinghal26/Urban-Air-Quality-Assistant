import os
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.config import (
    APP_TITLE, APP_SUBTITLE, VERSION, HOTSPOT_CITIES, LIFESTYLE_PROFILES, AIR_STANDARDS
)
from app.services.aqi_engine import get_current_smog_status, calculate_hourly_inversion_curve
from app.services.routine_planner import generate_daily_routine
from app.services.iaq_hacks import calculate_corsi_rosenthal_box, get_all_iaq_hacks, get_mask_comparison_data
from app.services.impact_calculator import calculate_personal_and_community_impact
from app.services.community_watch import (
    get_community_dashboard, add_community_pledge, report_smog_incident
)
from app.services.genai_assistant import get_assistant_response, PERSONAS

app = FastAPI(
    title=APP_TITLE,
    description=APP_SUBTITLE,
    version=VERSION
)

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Pydantic Request Models ---
class RoutineRequest(BaseModel):
    city_key: str = "delhi"
    lifestyle_key: str = "toddler_family"
    home_type: str = "apartment"
    heating_source: str = "heat_pump_electric"
    commute_mode: str = "transit"
    has_air_cleaner: bool = True

class CRBoxRequest(BaseModel):
    fan_size_inches: int = 20
    filter_count: int = 4
    filter_thickness_inches: int = 2
    room_sqft: float = 350.0
    ceiling_height_ft: float = 8.5
    fan_speed: str = "medium"

class ImpactRequest(BaseModel):
    ambient_pm25: float = 280.0
    outdoor_hours: float = 2.0
    mask_type: str = "n95"
    commute_mode: str = "carpool"
    commute_distance_km: float = 15.0
    baseline_commute_mode: str = "solo_car"
    has_cr_box_or_hepa: bool = True
    indoor_hours: float = 22.0
    heating_choice: str = "electric_heat_pump"
    community_multiplier: int = 50

class PledgeRequest(BaseModel):
    name: str = ""
    location: str = ""
    pledge_type: str = "DIY Air Cleaners"
    action: str

class IncidentRequest(BaseModel):
    incident_type: str
    location: str
    severity: str = "High"
    details: str

class ChatRequest(BaseModel):
    prompt: str
    persona_key: str = "dr_vayu"
    api_key: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

# --- UI Route ---
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Renders the main AuraShield web application interface."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": APP_TITLE,
            "subtitle": APP_SUBTITLE,
            "version": VERSION,
            "hotspot_cities": HOTSPOT_CITIES,
            "lifestyle_profiles": LIFESTYLE_PROFILES,
            "personas": PERSONAS
        }
    )

# --- API Endpoints ---
@app.get("/api/status")
async def get_system_status():
    """Returns application status and available city/lifestyle options."""
    return {
        "status": "healthy",
        "app": APP_TITLE,
        "version": VERSION,
        "cities": HOTSPOT_CITIES,
        "lifestyles": LIFESTYLE_PROFILES,
        "personas": PERSONAS,
        "standards": AIR_STANDARDS
    }

@app.get("/api/smog/current")
async def get_smog_current(city: str = "delhi", custom_aqi: Optional[float] = None):
    """Returns current real-time or simulated smog conditions and 24-hr diurnal inversion curve."""
    return get_current_smog_status(city, custom_aqi)

@app.post("/api/routine/generate")
async def generate_routine(req: RoutineRequest):
    """Generates customized daily low-emission and smog protection routine."""
    return generate_daily_routine(
        city_key=req.city_key,
        lifestyle_key=req.lifestyle_key,
        home_type=req.home_type,
        heating_source=req.heating_source,
        commute_mode=req.commute_mode,
        has_air_cleaner=req.has_air_cleaner
    )

@app.post("/api/iaq/cr-box-calc")
async def calculate_cr_box(req: CRBoxRequest):
    """Calculates Corsi-Rosenthal Box CADR, ACH, and cost comparison."""
    return calculate_corsi_rosenthal_box(
        fan_size_inches=req.fan_size_inches,
        filter_count=req.filter_count,
        filter_thickness_inches=req.filter_thickness_inches,
        room_sqft=req.room_sqft,
        ceiling_height_ft=req.ceiling_height_ft,
        fan_speed=req.fan_speed
    )

@app.get("/api/iaq/hacks")
async def get_iaq_hacks():
    """Returns science-backed indoor air quality hacks and mask comparison."""
    return {
        "hacks": get_all_iaq_hacks(),
        "mask_comparison": get_mask_comparison_data()
    }

@app.post("/api/impact/calculate")
async def calculate_impact(req: ImpactRequest):
    """Calculates personal PM2.5 lung dose prevented, cigarette equivalents, and community ripple."""
    return calculate_personal_and_community_impact(
        ambient_pm25=req.ambient_pm25,
        outdoor_hours=req.outdoor_hours,
        mask_type=req.mask_type,
        commute_mode=req.commute_mode,
        commute_distance_km=req.commute_distance_km,
        baseline_commute_mode=req.baseline_commute_mode,
        has_cr_box_or_hepa=req.has_cr_box_or_hepa,
        indoor_hours=req.indoor_hours,
        heating_choice=req.heating_choice,
        community_multiplier=req.community_multiplier
    )

@app.get("/api/community/dashboard")
async def get_community_info():
    """Returns community action ledger, smog incidents, and clean air sanctuaries."""
    return get_community_dashboard()

@app.post("/api/community/pledge")
async def submit_pledge(req: PledgeRequest):
    """Adds a new community pledge."""
    if not req.action:
        raise HTTPException(status_code=400, detail="Pledge action description is required.")
    return add_community_pledge(req.name, req.location, req.pledge_type, req.action)

@app.post("/api/community/report-incident")
async def submit_incident(req: IncidentRequest):
    """Submits an open burning or industrial smog violation report."""
    if not req.location or not req.details:
        raise HTTPException(status_code=400, detail="Location and details are required.")
    return report_smog_incident(req.incident_type, req.location, req.severity, req.details)

@app.post("/api/assistant/chat")
async def chat_with_assistant(req: ChatRequest):
    """Consults the GenAI Smog Assistant (Dr. Vayu, Engineer Bob, or Community Strategist)."""
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")
    return await get_assistant_response(
        prompt=req.prompt,
        persona_key=req.persona_key,
        api_key=req.api_key,
        context=req.context
    )
