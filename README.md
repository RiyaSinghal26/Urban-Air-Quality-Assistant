# 🛡️ AuraShield AI: Winter Smog & Urban Air Pollution Navigator

> **A GenAI-Powered Urban Air Defense System, Low-Emission Daily Routine Planner, and Community Clean-Air Action Hub.**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688.svg)](https://fastapi.tiangolo.com)
[![GenAI](https://img.shields.io/badge/GenAI-Dual%20Engine%20(Gemini%20%2B%20Cognitive)-cyan.svg)](https://ai.google.dev)
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20Passed%20(100%25)-brightgreen.svg)]()

---

## 🌟 Overview & Problem Statement

Severe winter smog in major metropolitan basins (such as Delhi NCR, Lahore, Salt Lake City, Beijing, Krakow, London, and Milan) is driven by **thermal boundary layer inversions**. Radiative cooling at night traps vehicular exhaust, wood smoke, industrial emissions, and dust in a shallow ground pool (often capped at 60–100 meters).

Standard air quality apps only report static AQI numbers without explaining *why* morning hours are lethal, *how* simple lifestyle adjustments cut exposure by 85%, or *what direct measurable impact* family and community choices create.

**AuraShield AI** solves this by fusing atmospheric physics, pulmonology, open-source DIY hardware engineering, and Generative AI into an interactive, multi-persona daily navigator.

---

## 🎯 Key Capabilities

### 1. 📡 Live Inversion Radar & 24-Hour Diurnal Forecast
- **Inversion Layer Modeling**: Simulates hourly planetary boundary layer ceiling height ($H_{inv}$) vs ground-level $PM_{2.5}$ concentration.
- **The "Solar Window" Secret**: Identifies the critical midday window (**12:30 PM – 3:30 PM**) when solar surface heating breaks the inversion lid, diluting ground smog by up to 70%—the only safe time for essential outdoor errands and home aeration.
- **7 Hotspot Presets + Custom Inputs**: Tailored presets for Delhi NCR, Lahore, Salt Lake City, London, Beijing, Krakow, and Milan Po Valley.

### 2. 📅 Tailored Low-Emission Daily Routine Planner
- **Vulnerability-Aware Customization**:
  - *Families with Newborns & Toddlers*: Halts morning stroller use where toxic tire dust and exhaust pool at child height (0.5m); secures nursery microclimates.
  - *Multigenerational Homes & Asthmatic Elders*: Prevents morning cold-air bronchial shock; guides indoor stretching and mucosal hydration.
  - *Daily Urban Commuters*: Prescribes cabin HVAC 100% Recirculation mode, N95 platform protection, and departure time-shifts.
  - *Budget Renters & Students*: High-impact low-cost hacks ($4 shrink wrap, towel draft snakes, $35 DIY filters).
  - *Athletes & Runners*: Inversion-timed indoor cardio protocols.
- **Hour-by-Hour Timeline**: Actionable color-coded directives from 06:00 to 22:00.
- **Sustainable Habit Transitions**: Replaces solo ICE driving with school carpool pods, wood fireplaces with inverter heat pumps, and open gas frying with induction simmering.

### 3. 🛠️ Indoor Air Quality (IAQ) Hacks Lab & DIY Corsi-Rosenthal Box
- **Open-Source C-R Box Configurator**:
  - Calculates Clean Air Delivery Rate (CADR, 450–550+ CFM) and Air Changes per Hour (ACH).
  - Simulates 90% particle clearance time (often under 18 minutes).
  - Demonstrates cost savings: **$70–$85 DIY build vs $520 commercial HEPA units**.
  - Highlights the critical **Cardboard Shroud Hack** (14" diameter circular cutout) that eliminates blade vortex stall and boosts clean airflow by 20%.
- **Science-Backed IAQ Protocols**:
  - *Microfiber Wet-Mopping vs Dry Sweeping*: Prevents 300% resuspension of toxic heavy-metal soot.
  - *Culinary Emission Suppression*: Back-burner cooking and rear range hood exhaustion to capture 70% of gas burner $NO_x$ and oil aerosol spikes.
  - *Mask Filtration Hierarchy*: Compares cloth (18%), surgical (38%), KN95 (88%), and certified headband N95 (96%) with 5-second fit-check instructions.
  - *Houseplants Myth vs Reality*: Clarifies why plants do not filter particulate matter ($PM_{2.5}$) and can harbor mold spores.

### 4. 📊 Direct Impact & Health Metrics Simulator
- **Alveolar Mass Spared**: Quantifies exact micrograms ($\mu g$) of $PM_{2.5}$ kept out of lung tissue per day and per 90-day winter season.
- **Berkeley Earth Cigarette Equivalents**: Converts invisible fine particulate doses into cigarette equivalents ($22 \, \mu g/m^3$ over 24h $\approx$ 1 cigarette).
- **Clinical Symptom Mitigation**:
  - Reduction in acute bronchospasm / wheezing risk (%)
  - Reduction in pediatric emergency room admission probability (%)
  - Reduction in cardiovascular autonomic stress (%)
- **Community Multiplier & Emissions Mitigated**:
  - Kilograms of $CO_2$ and grams of tailpipe $PM_{2.5}$ saved by transit / carpooling.
  - Neighborhood ripple model: Simulates local curb-level ambient $PM_{2.5}$ drops when 10, 50, 100, or 500 households adopt the routine.

### 5. 🤝 Community Smog Watch & Clean Air Mutual Aid
- **Hyperlocal Pledges Ledger**: Track collective neighborhood commitments (school carpools, clean heat switches, DIY purifiers).
- **Smog Violation & Open Burning Reporter**: One-click reporting dispatch for leaf burning, construction dust, or idling diesel generators.
- **Clean Air Public Sanctuaries**: Directory of filtered public sanctuaries (public libraries, metro concourses) for vulnerable citizens during smog emergencies.

### 6. 🤖 GenAI Smog Copilot (Multi-Persona Dual Engine)
- **Three Specialized Personas**:
  - **Dr. Vayu** (Pulmonologist & Respiratory Health Advisor)
  - **Engineer Bob** (DIY Hardware, HVAC & Atmospheric Physics Specialist)
  - **Aura Strategist** (Community Mutual Aid & Low-Emission Policy Advocate)
- **Dual Engine Architecture**:
  1. *Built-in Local Cognitive Synthesis Engine*: 100% offline-ready, instant response, domain-trained on WHO/EPA air guidelines and inversion physics.
  2. *Live Google Gemini API Integration*: Optional connection to `gemini-2.5-flash` or `gemini-1.5-flash` with customizable user API key.

---

## 🔬 Scientific Foundations & Formulas

### 1. Personal Inhaled Dose Equation
$$\text{Dose}_{\text{inhaled}} (\mu g) = \sum_{i} \left[ C_i \times (1 - \eta_{\text{mask}}) \times \text{BR} \times T_i \right]$$
Where:
- $C_i$ = microenvironment concentration ($\mu g/m^3$)
- $\eta_{\text{mask}}$ = mask filtration efficiency ($0.0$ for none, $0.96$ for N95)
- $\text{BR}$ = respiration volume rate ($m^3/h$)
- $T_i$ = duration spent in hours

### 2. Berkeley Earth Cigarette Equivalent Conversion
$$\text{Cigarette Equivalent} = \frac{\text{PM}_{2.5} \text{ Inhaled Dose } (\mu g)}{22 \, \mu g/m^3 \times 15 \, m^3/\text{day}} = \frac{\text{Dose } (\mu g)}{330 \, \mu g}$$

### 3. Corsi-Rosenthal Box Air Changes per Hour (ACH)
$$\text{ACH} = \frac{\text{CADR}_{\text{CFM}} \times 60}{\text{Room Volume}_{\text{cu ft}}}$$
$$\text{Time to 90\% Clearance (minutes)} = \left( \frac{2.3026}{\text{ACH}} \right) \times 60$$

---

## 🚀 Quickstart & Deployment

### Deploy on Render (Free & 1-Click)
This project is pre-configured with `render.yaml`, `Procfile`, and `requirements.txt` for instant deployment on [Render](https://render.com):

1. **Log in** to your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Connect your GitHub repository: `https://github.com/RiyaSinghal26/Urban-Air-Quality-Assistant`.
4. Configure the settings:
   - **Name**: `urban-air-quality-assistant` (or your choice)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. (Optional) Under **Environment Variables**, add:
   - `GEMINI_API_KEY`: *(Your Google Gemini API Key if you want live Google AI reasoning; otherwise built-in offline GenAI engine will run automatically)*
6. Click **Deploy Web Service**! Render will build and launch your live application at `https://urban-air-quality-assistant.onrender.com`.

---

### Local Quickstart Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- No Node.js required! (All interactive frontend assets are bundled with lightweight zero-build static architecture)

### Installation
```bash
# Clone or navigate to the directory
cd d:\Challenge6

# (Optional) Set your Gemini API key if desired for live model inference
set GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the Application
```bash
# Option 1: Using the runner (auto-allocates free port and opens browser)
python run.py

# Option 2: Using Uvicorn directly
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser to: **`http://127.0.0.1:8000`**

---

## 🧪 Automated Test Suite

A comprehensive test suite is included in `tests/test_api.py`, covering all physics calculations, API routes, and GenAI synthesis:

```bash
python -m pytest tests/test_api.py -v
```

### Test Coverage Highlights:
- `test_aqi_categories`: Standard WHO/EPA threshold bands & emergency alerts.
- `test_hourly_inversion_curve`: Verifies boundary layer diurnal inversion curve (morning stagnation vs solar breakdown).
- `test_corsi_rosenthal_box_calculation`: CADR, ACH, clean time, and cost savings formulas.
- `test_routine_generator`: Timeline scheduling and lifestyle vulnerability adaptation.
- `test_impact_calculator`: Personal PM2.5 lung mass spared, cigarette equivalents, and community ripple multipliers.
- `test_community_watch`: Incident reporting, pledge submissions, and sanctuary directory.
- `test_genai_local_cognitive_engine`: Multi-persona reasoning and domain accuracy.
- `test_fastapi_endpoints`: End-to-end REST API verification.

---

## 📁 Project Architecture

```
d:\Challenge6\
├── app\
│   ├── __init__.py
│   ├── config.py                # Hotspot cities, lifestyle profiles, WHO standards
│   ├── main.py                  # FastAPI application with REST endpoints
│   ├── services\
│   │   ├── __init__.py
│   │   ├── aqi_engine.py        # Diurnal inversion physics & AQI curves
│   │   ├── iaq_hacks.py         # Corsi-Rosenthal Box configurator & IAQ science
│   │   ├── routine_planner.py   # Tailored 24h low-emission routines
│   │   ├── impact_calculator.py # PM2.5 lung dose spared & community ripple
│   │   ├── community_watch.py   # Pledges, violation reports, clean air sanctuaries
│   │   └── genai_assistant.py   # Multi-persona GenAI (Gemini + Local Cognitive)
│   ├── static\
│   │   ├── css\
│   │   │   └── styles.css       # Glassmorphism styling, animations, responsive design
│   │   └── js\
│   │       └── app.js          # Reactive UI logic, Chart.js, calculators, AI chat
│   └── templates\
│       └── index.html           # Single-Page Interactive Application UI
├── tests\
│   └── test_api.py              # Automated test suite (100% passing)
├── run.py                       # One-command runner script
└── README.md                    # System documentation and user guide
```

---

## 🛡️ License & Attribution
Built for families and communities combating toxic winter smog. Open-source under the Apache 2.0 License. Grounded in research from the World Health Organization (WHO), US EPA, and atmospheric boundary layer aerosol studies.
