import uuid
from datetime import datetime
from typing import Dict, Any, List

# In-memory community storage for dynamic session interactions
COMMUNITY_PLEDGES: List[Dict[str, Any]] = [
    {
        "id": "plg-1",
        "name": "The Sharma Family",
        "location": "South Delhi, Sector 4",
        "pledge_type": "School Carpool Cluster",
        "action": "Formed a 4-family electric carpool pod for DPS RK Puram, eliminating 3 solo SUV trips every morning.",
        "impact_label": "-12.8 kg CO2/day, zero school gate idling",
        "timestamp": "2026-11-24 14:15"
    },
    {
        "id": "plg-2",
        "name": "Gulberg Residents Association",
        "location": "Lahore, Block B",
        "pledge_type": "DIY Air Cleaners",
        "action": "Built 22 Corsi-Rosenthal boxes for the local community library and pediatric dispensary.",
        "impact_label": "Over 11,000 CFM clean air delivery created",
        "timestamp": "2026-11-24 15:30"
    },
    {
        "id": "plg-3",
        "name": "Marcus & Elena K.",
        "location": "Salt Lake City, Avenues",
        "pledge_type": "Clean Heating Switch",
        "action": "Pledged zero wood-stove burns during mandatory red-burn inversion alerts; switched to heat pump.",
        "impact_label": "Eliminated 100% of neighborhood wood-smoke PAHs",
        "timestamp": "2026-11-24 16:45"
    },
    {
        "id": "plg-4",
        "name": "Ananya & Rohit P.",
        "location": "Dwarka, New Delhi",
        "pledge_type": "Anti-Burning Watch",
        "action": "Reported 2 illegal horticultural waste fires to local municipal ward and coordinated municipal composting.",
        "impact_label": "Prevented dense localized smoke plume over 3 colonies",
        "timestamp": "2026-11-24 17:10"
    }
]

INCIDENT_REPORTS: List[Dict[str, Any]] = [
    {
        "id": "inc-101",
        "type": "Horticultural / Leaf Open Burning",
        "location": "Outer Ring Road Green Belt",
        "severity": "High (Dense black smoke drifting onto highway)",
        "status": "Forwarded to Municipal Flying Squad",
        "timestamp": "2026-11-24 16:20",
        "reporter": "Community Watch Volunteer #4"
    },
    {
        "id": "inc-102",
        "type": "Commercial Diesel Generator Idling",
        "location": "Commercial Plaza, Block C",
        "severity": "Medium (Continuous un-scrubbed exhaust)",
        "status": "Notice Issued for Dual-Fuel Conversion",
        "timestamp": "2026-11-24 15:05",
        "reporter": "CleanAir Neighborhood Scout"
    }
]

CLEAN_AIR_SANCTUARIES: List[Dict[str, Any]] = [
    {
        "name": "Central District Public Library",
        "type": "Public Reading Sanctuary",
        "features": "Central MERV-14 HVAC + 8x HEPA tower units. Free Wi-Fi, study desks.",
        "indoor_pm25": "8 µg/m³ (vs 320 outside)",
        "access": "Open to all, 09:00 AM - 08:00 PM",
        "distance": "1.2 km away"
    },
    {
        "name": "Underground Metro Central Concourse",
        "type": "Transit Air Oasis",
        "features": "Deep subterranean tunnel air filtration with electrostatic precipitators.",
        "indoor_pm25": "18 µg/m³",
        "access": "Ticketed transit zone, 06:00 AM - 11:30 PM",
        "distance": "0.6 km away"
    },
    {
        "name": "Community Health & Wellness Pavilion",
        "type": "Municipal Relief Center",
        "features": "Positive-pressure clean room, pediatric nebulizer stations, N95 distribution.",
        "indoor_pm25": "12 µg/m³",
        "access": "Free emergency public access during severe AQI > 300 alerts",
        "distance": "2.4 km away"
    }
]

def get_community_dashboard() -> Dict[str, Any]:
    """Returns community pledges, incidents, and sanctuaries."""
    return {
        "pledges": COMMUNITY_PLEDGES,
        "incidents": INCIDENT_REPORTS,
        "sanctuaries": CLEAN_AIR_SANCTUARIES,
        "total_pledges": len(COMMUNITY_PLEDGES) + 142, # Base historical + session
        "total_co2_spared_kg": 4350.0,
        "total_pm25_spared_kg": 182.5,
        "active_carpool_pods": 38
    }

def add_community_pledge(name: str, location: str, pledge_type: str, action: str) -> Dict[str, Any]:
    """Adds a new community pledge and updates the ledger."""
    new_pledge = {
        "id": f"plg-{uuid.uuid4().hex[:6]}",
        "name": name.strip() or "Anonymous Neighbor",
        "location": location.strip() or "Local Neighborhood",
        "pledge_type": pledge_type,
        "action": action.strip(),
        "impact_label": "High Community Clean-Air Contribution",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    COMMUNITY_PLEDGES.insert(0, new_pledge)
    return new_pledge

def report_smog_incident(incident_type: str, location: str, severity: str, details: str) -> Dict[str, Any]:
    """Logs a smog incident report and prepares notification dispatch."""
    new_incident = {
        "id": f"inc-{uuid.uuid4().hex[:6]}",
        "type": incident_type,
        "location": location.strip(),
        "severity": severity,
        "details": details.strip(),
        "status": "Logged & Transmitted to Air Quality Authority",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reporter": "AuraShield Citizen Sentinel"
    }
    INCIDENT_REPORTS.insert(0, new_incident)
    return new_incident
