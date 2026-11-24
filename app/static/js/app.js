// AuraShield AI Interactive Application Script
let currentCity = "delhi";
let currentPersona = "dr_vayu";
let userApiKey = localStorage.getItem("aurashield_gemini_api_key") || "";
let inversionChart = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  updateApiKeyLabel();
  loadCurrentSmogData();
  generateRoutine();
  recalculateCRBox();
  loadIAQHacks();
  updateImpactSimulation();
  loadCommunityDashboard();
});

// --- Tab Management ---
function switchTab(tabId) {
  const tabs = ["radar", "routine", "iaq", "impact", "community", "copilot"];
  tabs.forEach(t => {
    const el = document.getElementById(`tab-${t}`);
    const btn = document.getElementById(`tab-btn-${t}`);
    if (el) el.classList.toggle("hidden", t !== tabId);
    if (btn) btn.classList.toggle("active", t === tabId);
  });
  
  if (tabId === "radar" && inversionChart) {
    inversionChart.resize();
  }
}

// --- City & Smog Radar ---
async function changeCity(cityKey) {
  currentCity = cityKey;
  await loadCurrentSmogData();
  await generateRoutine();
  await updateImpactSimulation();
}

async function refreshSmogData() {
  await loadCurrentSmogData();
}

async function loadCurrentSmogData() {
  try {
    const res = await fetch(`/api/smog/current?city=${currentCity}`);
    const data = await res.json();

    // Update Header Pill
    const aqiPill = document.getElementById("live-aqi-pill");
    document.getElementById("live-aqi-val").textContent = Math.round(data.aqi);
    document.getElementById("live-aqi-level").textContent = data.category;
    aqiPill.className = `flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium ${data.badge}`;

    // Update Hero Card
    document.getElementById("hero-city-title").textContent = data.city_name;
    document.getElementById("hero-health-advice").textContent = data.health_advice;
    document.getElementById("hero-pm25").textContent = data.pm25;
    document.getElementById("hero-inversion-m").textContent = `${data.inversion_height_meters}m`;
    document.getElementById("hero-cigarettes").textContent = data.cigarette_equivalent_24h;
    document.getElementById("hero-safest-window").textContent = data.safest_window;
    document.getElementById("hero-badge").textContent = `${data.urgency}: ${data.category.toUpperCase()}`;
    document.getElementById("hero-timestamp").textContent = `Updated at ${data.timestamp.split(" ")[1]}`;

    // Render Diurnal Inversion Chart
    renderInversionChart(data.hourly_forecast, data.safest_window);
  } catch (err) {
    console.error("Error loading smog data:", err);
  }
}

function renderInversionChart(hourlyForecast, safestWindowStr) {
  const ctx = document.getElementById("inversionChart").getContext("2d");
  
  const labels = hourlyForecast.map(h => h.time_label);
  const pm25Data = hourlyForecast.map(h => h.pm25);
  const inversionHeight = hourlyForecast.map(h => h.inversion_height_meters);
  const safeMask = hourlyForecast.map(h => h.is_safe_window ? h.pm25 : null);

  if (inversionChart) {
    inversionChart.destroy();
  }

  inversionChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "PM2.5 (µg/m³)",
          data: pm25Data,
          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.15)",
          fill: true,
          tension: 0.4,
          yAxisID: "y-pm25",
          borderWidth: 2.5,
          pointRadius: 2,
          pointHoverRadius: 6
        },
        {
          label: "Inversion Height (m)",
          data: inversionHeight,
          borderColor: "#22d3ee",
          borderDash: [5, 5],
          tension: 0.4,
          yAxisID: "y-inversion",
          borderWidth: 2,
          pointRadius: 0
        },
        {
          label: "Safest Solar Window",
          data: safeMask,
          borderColor: "#10b981",
          backgroundColor: "#10b981",
          pointRadius: 6,
          pointHoverRadius: 8,
          showLine: false,
          yAxisID: "y-pm25"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleColor: "#38bdf8",
          bodyColor: "#f1f5f9",
          borderColor: "#334155",
          borderWidth: 1,
          callbacks: {
            afterBody: (context) => {
              const hourIndex = context[0].dataIndex;
              const h = hourlyForecast[hourIndex];
              return `Status: ${h.recommendation}\nInversion Ceiling: ${h.inversion_height_meters}m`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { color: "#94a3b8", font: { size: 10 } }
        },
        "y-pm25": {
          type: "linear",
          position: "left",
          title: { display: true, text: "PM2.5 (µg/m³)", color: "#f87171", font: { size: 11 } },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { color: "#fca5a5", font: { size: 10 } }
        },
        "y-inversion": {
          type: "linear",
          position: "right",
          title: { display: true, text: "Inversion Height (m)", color: "#22d3ee", font: { size: 11 } },
          grid: { drawOnChartArea: false },
          ticks: { color: "#67e8f9", font: { size: 10 } }
        }
      }
    }
  });
}

// --- Tab 2: Routine Planner ---
async function generateRoutine() {
  const lifestyle = document.getElementById("routine-lifestyle").value;
  const homeType = document.getElementById("routine-home-type").value;
  const heating = document.getElementById("routine-heating").value;
  const commute = document.getElementById("routine-commute").value;

  try {
    const res = await fetch("/api/routine/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        city_key: currentCity,
        lifestyle_key: lifestyle,
        home_type: homeType,
        heating_source: heating,
        commute_mode: commute,
        has_air_cleaner: true
      })
    });
    const data = await res.json();

    document.getElementById("routine-lifestyle-title").textContent = data.lifestyle_title;
    document.getElementById("routine-vulnerability-badge").textContent = data.vulnerability;
    document.getElementById("routine-critical-rule").textContent = data.critical_rule;

    // Render Timeline
    const timelineContainer = document.getElementById("routine-timeline-container");
    timelineContainer.innerHTML = "";

    data.timeline.forEach((slot, idx) => {
      const card = document.createElement("div");
      card.className = "p-4 rounded-xl glass-panel-subtle border border-slate-800 space-y-2 hover:border-slate-700 transition";
      card.innerHTML = `
        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-1.5 border-b border-slate-800/80 pb-2">
          <div class="flex items-center gap-2">
            <span class="text-xs font-extrabold text-cyan-300 font-mono">${slot.time_slot}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${slot.badge_color}">${slot.hazard_level}</span>
          </div>
          <span class="text-[11px] text-slate-400 italic">${slot.inversion_status}</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-xs">
          <div>
            <span class="text-slate-400 font-medium block">🎯 Protective Routine Action:</span>
            <p class="text-slate-200 mt-0.5">${slot.routine_action}</p>
            <p class="text-cyan-300/90 mt-1.5 text-[11px]"><strong>For Your Family:</strong> ${slot.lifestyle_specific}</p>
          </div>
          <div class="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/60">
            <span class="text-emerald-400 font-semibold block text-[11px]">🌱 Low-Emission Habit Choice:</span>
            <p class="text-slate-300 mt-0.5">${slot.low_emission_action}</p>
          </div>
        </div>
      `;
      timelineContainer.appendChild(card);
    });

    // Render Sustainable Alternatives
    const altContainer = document.getElementById("sustainable-alternatives-container");
    altContainer.innerHTML = "";
    data.sustainable_alternatives.forEach(alt => {
      const el = document.createElement("div");
      el.className = "p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2";
      el.innerHTML = `
        <div class="flex justify-between items-center text-xs">
          <strong class="text-cyan-300">${alt.category}</strong>
          <span class="text-[10px] uppercase tracking-wider text-emerald-400 font-bold bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">Clean Alternative</span>
        </div>
        <div class="text-xs space-y-1">
          <p class="text-rose-300/80 line-through">Old Habit: ${alt.current_habit}</p>
          <p class="text-emerald-300 font-semibold">✨ Switch: ${alt.sustainable_alternative}</p>
          <p class="text-slate-400 text-[11px] pt-1"><strong>Direct Impact:</strong> ${alt.direct_impact}</p>
        </div>
      `;
      altContainer.appendChild(el);
    });
  } catch (err) {
    console.error("Error generating routine:", err);
  }
}

// --- Tab 3: IAQ Hacks & DIY Lab ---
async function recalculateCRBox() {
  const fanSize = parseInt(document.getElementById("cr-fan-size").value) || 20;
  const filterCount = parseInt(document.getElementById("cr-filter-count").value) || 4;
  const thickness = parseInt(document.getElementById("cr-filter-thickness").value) || 2;
  const roomSqft = parseFloat(document.getElementById("cr-room-sqft").value) || 350;
  const speed = document.getElementById("cr-fan-speed").value;

  try {
    const res = await fetch("/api/iaq/cr-box-calc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fan_size_inches: fanSize,
        filter_count: filterCount,
        filter_thickness_inches: thickness,
        room_sqft: roomSqft,
        ceiling_height_ft: 8.5,
        fan_speed: speed
      })
    });
    const data = await res.json();

    document.getElementById("cr-cadr-val").textContent = data.effective_cadr_cfm;
    document.getElementById("cr-ach-val").textContent = data.ach;
    document.getElementById("cr-ach-rating").textContent = data.ach_rating;
    document.getElementById("cr-time-val").textContent = data.clean_90pct_time_mins;
    document.getElementById("cr-cost-diy").textContent = `$${data.total_diy_cost_usd.toFixed(2)}`;
    document.getElementById("cr-savings-label").textContent = `You save $${data.savings_usd.toFixed(0)}!`;

    const costPct = Math.round((data.total_diy_cost_usd / data.commercial_equivalent_cost_usd) * 100);
    const diyBar = document.getElementById("cr-cost-bar-diy");
    diyBar.style.width = `${Math.max(15, costPct)}%`;
    diyBar.textContent = `DIY $${data.total_diy_cost_usd.toFixed(0)}`;

    const stepsList = document.getElementById("cr-steps-list");
    stepsList.innerHTML = "";
    data.step_by_step_instructions.forEach(step => {
      const li = document.createElement("li");
      li.className = "leading-relaxed";
      li.textContent = step;
      stepsList.appendChild(li);
    });
  } catch (err) {
    console.error("Error calculating C-R box:", err);
  }
}

async function loadIAQHacks() {
  try {
    const res = await fetch("/api/iaq/hacks");
    const data = await res.json();

    // Render Hacks Cards
    const hacksGrid = document.getElementById("iaq-hacks-grid");
    hacksGrid.innerHTML = "";
    data.hacks.forEach(h => {
      const card = document.createElement("div");
      card.className = "p-4 rounded-xl glass-panel-subtle border border-slate-800 space-y-2 hover:border-slate-700 transition flex flex-col justify-between";
      card.innerHTML = `
        <div class="space-y-1.5">
          <div class="flex justify-between items-start">
            <span class="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold">${h.category}</span>
            <span class="text-xs text-amber-400 font-semibold">${h.cost}</span>
          </div>
          <h4 class="text-sm font-bold text-slate-100">${h.title}</h4>
          <p class="text-xs text-slate-300">${h.summary}</p>
        </div>
        <div class="pt-2 border-t border-slate-800/60 text-[11px] space-y-1">
          <p class="text-slate-400"><strong>The Science:</strong> ${h.science}</p>
          <p class="text-emerald-300 font-medium"><strong>Best Practice:</strong> ${h.best_practice}</p>
        </div>
      `;
      hacksGrid.appendChild(card);
    });

    // Render Mask Comparison Table
    const maskBody = document.getElementById("mask-table-body");
    maskBody.innerHTML = "";
    data.mask_comparison.forEach(m => {
      const tr = document.createElement("tr");
      tr.className = "hover:bg-slate-900/40 transition";
      tr.innerHTML = `
        <td class="py-2.5 px-3 font-semibold text-slate-200">${m.type}</td>
        <td class="py-2.5 px-3">
          <span class="font-bold ${m.pm25_efficiency >= 90 ? 'text-emerald-400' : (m.pm25_efficiency >= 80 ? 'text-cyan-400' : 'text-rose-400')}">
            ${m.pm25_efficiency}%
          </span>
        </td>
        <td class="py-2.5 px-3 text-slate-300">${m.seal_quality}</td>
        <td class="py-2.5 px-3 text-slate-400">${m.leakage_rate}</td>
        <td class="py-2.5 px-3 text-slate-300">${m.verdict}</td>
      `;
      maskBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Error loading IAQ hacks:", err);
  }
}

// --- Tab 4: Impact Simulator ---
async function updateImpactSimulation() {
  const outdoorHours = parseFloat(document.getElementById("slider-outdoor").value) || 2.0;
  document.getElementById("slider-outdoor-val").textContent = `${outdoorHours.toFixed(1)} hrs`;

  const mask = document.getElementById("sim-mask").value;
  const commute = document.getElementById("sim-commute").value;
  const commuteKm = parseFloat(document.getElementById("sim-commute-km").value) || 15.0;
  const hasCR = document.getElementById("sim-indoor-filtration").value === "true";

  const multiplier = parseInt(document.getElementById("slider-multiplier").value) || 50;
  document.getElementById("slider-multiplier-val").textContent = `${multiplier} Households`;
  document.getElementById("sim-multiplier-pill").textContent = `${multiplier} Homes`;

  try {
    const res = await fetch("/api/impact/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ambient_pm25: 280.0,
        outdoor_hours: outdoorHours,
        mask_type: mask,
        commute_mode: commute,
        commute_distance_km: commuteKm,
        baseline_commute_mode: "solo_car",
        has_cr_box_or_hepa: hasCR,
        indoor_hours: 24.0 - outdoorHours,
        heating_choice: "electric_heat_pump",
        community_multiplier: multiplier
      })
    });
    const data = await res.json();
    const p = data.personal_metrics;
    const c = data.community_ripple;

    document.getElementById("sim-pm25-daily").textContent = Math.round(p.pm25_saved_daily_ug).toLocaleString();
    document.getElementById("sim-cigs-daily").textContent = p.cigarette_equivalent_daily;
    document.getElementById("sim-cigs-season").textContent = p.cigarette_equivalent_season.toLocaleString();

    document.getElementById("sim-reduction-pct").textContent = `${p.total_exposure_reduction_pct}%`;
    document.getElementById("sim-reduction-bar").style.width = `${Math.min(100, p.total_exposure_reduction_pct)}%`;

    document.getElementById("sim-bronchial-pct").textContent = `-${p.bronchial_inflammation_reduction_pct}%`;
    document.getElementById("sim-er-pct").textContent = `-${p.pediatric_er_risk_reduction_pct}%`;
    document.getElementById("sim-cardiac-pct").textContent = `-${p.cardiac_stress_drop_pct}%`;

    document.getElementById("sim-comm-co2").textContent = c.community_co2_season_tons.toFixed(1);
    document.getElementById("sim-comm-pm25").textContent = c.community_pm25_season_kg.toFixed(1);
    document.getElementById("sim-comm-cigs").textContent = c.community_cigarettes_spared.toLocaleString();
    document.getElementById("sim-comm-ambient-drop").textContent = `Estimated ${c.neighborhood_ambient_pm25_reduction_estimate} if ${multiplier} neighborhood families adopt this routine!`;
  } catch (err) {
    console.error("Error updating impact simulation:", err);
  }
}

// --- Tab 5: Community Watch ---
async function loadCommunityDashboard() {
  try {
    const res = await fetch("/api/community/dashboard");
    const data = await res.json();

    document.getElementById("comm-total-pledges").textContent = data.total_pledges;
    document.getElementById("comm-total-co2").textContent = `${data.total_co2_spared_kg.toLocaleString()} kg`;
    document.getElementById("comm-active-pods").textContent = data.active_carpool_pods;

    // Sanctuaries
    const sancGrid = document.getElementById("sanctuaries-grid");
    sancGrid.innerHTML = "";
    data.sanctuaries.forEach(s => {
      const el = document.createElement("div");
      el.className = "p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2";
      el.innerHTML = `
        <div class="flex justify-between items-center text-xs">
          <strong class="text-cyan-300">${s.name}</strong>
          <span class="text-[10px] text-slate-400">${s.distance}</span>
        </div>
        <p class="text-xs text-slate-300">${s.features}</p>
        <div class="flex justify-between items-center text-[11px] pt-1 border-t border-slate-800/80">
          <span class="text-emerald-400 font-bold">Indoor: ${s.indoor_pm25}</span>
          <span class="text-slate-400">${s.access}</span>
        </div>
      `;
      sancGrid.appendChild(el);
    });

    // Pledges List
    const pledgesList = document.getElementById("pledges-list");
    pledgesList.innerHTML = "";
    data.pledges.forEach(p => {
      const el = document.createElement("div");
      el.className = "p-3 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1 text-xs";
      el.innerHTML = `
        <div class="flex justify-between items-center">
          <strong class="text-emerald-400">${p.name}</strong>
          <span class="text-[10px] text-slate-500">${p.timestamp}</span>
        </div>
        <p class="text-slate-300">${p.action}</p>
        <div class="flex justify-between text-[11px] text-slate-400 pt-0.5">
          <span>📍 ${p.location}</span>
          <span class="text-cyan-300 font-semibold">${p.impact_label}</span>
        </div>
      `;
      pledgesList.appendChild(el);
    });

    // Incident Reports List
    const incidentsList = document.getElementById("incidents-list");
    incidentsList.innerHTML = "";
    data.incidents.forEach(inc => {
      const el = document.createElement("div");
      el.className = "p-3 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1 text-xs";
      el.innerHTML = `
        <div class="flex justify-between items-center">
          <strong class="text-rose-400">${inc.type}</strong>
          <span class="text-[10px] text-slate-500">${inc.timestamp}</span>
        </div>
        <p class="text-slate-300">${inc.details || inc.severity}</p>
        <div class="flex justify-between text-[11px] text-slate-400 pt-0.5">
          <span>📍 ${inc.location}</span>
          <span class="text-amber-400 font-medium">${inc.status}</span>
        </div>
      `;
      incidentsList.appendChild(el);
    });
  } catch (err) {
    console.error("Error loading community dashboard:", err);
  }
}

// Modals
function openApiKeyModal() {
  document.getElementById("user-gemini-key").value = userApiKey;
  document.getElementById("modal-apikey").classList.remove("hidden");
}
function closeApiKeyModal() {
  document.getElementById("modal-apikey").classList.add("hidden");
}
function saveApiKey(key) {
  userApiKey = key.trim();
  localStorage.setItem("aurashield_gemini_api_key", userApiKey);
  updateApiKeyLabel();
  closeApiKeyModal();
}
function updateApiKeyLabel() {
  const lbl = document.getElementById("api-status-label");
  if (userApiKey && userApiKey.length > 8) {
    lbl.textContent = "Gemini API: Live Active";
    lbl.classList.add("text-emerald-400");
  } else {
    lbl.textContent = "Gemini API: Auto/Offline";
    lbl.classList.remove("text-emerald-400");
  }
}

function openPledgeModal() {
  document.getElementById("modal-pledge").classList.remove("hidden");
}
function closePledgeModal() {
  document.getElementById("modal-pledge").classList.add("hidden");
}
async function submitPledgeForm() {
  const name = document.getElementById("pledge-name").value;
  const loc = document.getElementById("pledge-loc").value;
  const type = document.getElementById("pledge-type").value;
  const action = document.getElementById("pledge-action").value;

  if (!action.trim()) {
    alert("Please provide an action description for your pledge.");
    return;
  }

  try {
    await fetch("/api/community/pledge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, location: loc, pledge_type: type, action })
    });
    closePledgeModal();
    loadCommunityDashboard();
  } catch (err) {
    alert("Error saving pledge.");
  }
}

function openIncidentModal() {
  document.getElementById("modal-incident").classList.remove("hidden");
}
function closeIncidentModal() {
  document.getElementById("modal-incident").classList.add("hidden");
}
async function submitIncidentForm() {
  const type = document.getElementById("inc-type").value;
  const loc = document.getElementById("inc-loc").value;
  const severity = document.getElementById("inc-severity").value;
  const details = document.getElementById("inc-details").value;

  if (!loc.trim() || !details.trim()) {
    alert("Please fill in the location and incident details.");
    return;
  }

  try {
    await fetch("/api/community/report-incident", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ incident_type: type, location: loc, severity, details })
    });
    closeIncidentModal();
    loadCommunityDashboard();
    alert("Violation successfully logged and dispatched to air quality authorities!");
  } catch (err) {
    alert("Error logging incident.");
  }
}

// --- Tab 6: GenAI Copilot ---
function selectPersona(personaKey) {
  currentPersona = personaKey;
  ["dr_vayu", "engineer_bob", "community_strategist"].forEach(p => {
    const btn = document.getElementById(`btn-persona-${p}`);
    if (btn) {
      if (p === personaKey) {
        btn.className = "persona-btn active px-3 py-1 rounded-md text-xs font-semibold transition bg-cyan-600 text-white";
      } else {
        btn.className = "persona-btn px-3 py-1 rounded-md text-xs font-semibold transition text-slate-400 hover:text-white";
      }
    }
  });
}

function handleChatKey(e) {
  if (e.key === "Enter") {
    sendChatMessage();
  }
}

function sendQuickPrompt(promptText) {
  document.getElementById("chat-input").value = promptText;
  sendChatMessage();
}

async function sendChatMessage() {
  const inputEl = document.getElementById("chat-input");
  const prompt = inputEl.value.trim();
  if (!prompt) return;

  const chatContainer = document.getElementById("chat-messages");

  // User Message Bubble
  const userMsg = document.createElement("div");
  userMsg.className = "flex items-start gap-3 justify-end";
  userMsg.innerHTML = `
    <div class="rounded-2xl rounded-tr-none p-3.5 max-w-xl text-xs bg-cyan-600 text-white shadow leading-relaxed">
      ${prompt}
    </div>
    <div class="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-sm shadow">
      👤
    </div>
  `;
  chatContainer.appendChild(userMsg);
  inputEl.value = "";
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Assistant Loading Bubble
  const loadingMsg = document.createElement("div");
  loadingMsg.id = "temp-loading-bubble";
  loadingMsg.className = "flex items-start gap-3";
  const avatar = currentPersona === "dr_vayu" ? "🩺" : (currentPersona === "engineer_bob" ? "🛠️" : "🌱");
  loadingMsg.innerHTML = `
    <div class="w-8 h-8 rounded-full bg-cyan-600 flex items-center justify-center text-sm shadow">
      ${avatar}
    </div>
    <div class="glass-panel-subtle rounded-2xl rounded-tl-none p-3.5 max-w-xl text-xs text-slate-400 flex items-center gap-2">
      <span class="inline-block w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
      Synthesizing atmospheric & clinical air defense guidance...
    </div>
  `;
  chatContainer.appendChild(loadingMsg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const res = await fetch("/api/assistant/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: prompt,
        persona_key: currentPersona,
        api_key: userApiKey || null,
        context: {
          city_name: currentCity,
          aqi: parseInt(document.getElementById("live-aqi-val").textContent) || 350
        }
      })
    });
    const data = await res.json();
    loadingMsg.remove();

    // Assistant Response Bubble
    const aiMsg = document.createElement("div");
    aiMsg.className = "flex items-start gap-3";
    const renderedText = marked.parse(data.response);
    aiMsg.innerHTML = `
      <div class="w-8 h-8 rounded-full bg-cyan-600 flex items-center justify-center text-sm shadow">
        ${avatar}
      </div>
      <div class="glass-panel-subtle rounded-2xl rounded-tl-none p-4 max-w-2xl text-xs text-slate-200 leading-relaxed border-slate-700 space-y-2 prose prose-invert prose-xs">
        <div class="text-[10px] text-cyan-400/80 uppercase font-mono tracking-wider border-b border-slate-800 pb-1 flex justify-between">
          <span>${data.source}</span>
          <span>${data.persona.role}</span>
        </div>
        <div class="leading-relaxed mt-2">${renderedText}</div>
      </div>
    `;
    chatContainer.appendChild(aiMsg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (err) {
    if (loadingMsg) loadingMsg.remove();
    console.error("Chat error:", err);
  }
}
