import json
import math
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Prakriti-AI • Plant-to-Plant Risk",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# Sample plant-to-plant risk model
# ------------------------------------------------------------
random.seed(42)
ROWS, COLS = 14, 22

# These are simulated already-affected plants. In the real project,
# these anchors would come from the disease/pest detector.
anchors = [
    {"row": 5, "col": 7, "risk": 0.96, "cause": "Rice Blast", "type": "Disease"},
    {"row": 10, "col": 16, "risk": 0.93, "cause": "Stem Borer", "type": "Pest"},
    {"row": 4, "col": 19, "risk": 0.90, "cause": "Bacterial Blight", "type": "Disease"},
    {"row": 11, "col": 4, "risk": 0.85, "cause": "Brown Spot", "type": "Disease"},
]

plants = []

for r in range(1, ROWS + 1):
    for c in range(1, COLS + 1):
        risk = 0.03 + random.random() * 0.06
        closest = None
        closest_influence = 0.0

        for anchor in anchors:
            distance = math.hypot(c - anchor["col"], r - anchor["row"])
            influence = anchor["risk"] * math.exp(-(distance**2) / (2 * 2.4**2))
            risk += influence
            if influence > closest_influence:
                closest_influence = influence
                closest = anchor

        risk = min(0.98, risk)

        if risk >= 0.78:
            status = "Affected"
        elif risk >= 0.38:
            status = "At Risk"
        else:
            status = "Healthy"

        if closest and closest_influence > 0.10:
            cause = closest["cause"]
            source_distance = round(
                math.hypot(c - closest["col"], r - closest["row"]), 1
            )
        else:
            cause = "Low exposure"
            source_distance = None

        # Keep the seed plants visibly affected.
        for anchor in anchors:
            if r == anchor["row"] and c == anchor["col"]:
                risk = anchor["risk"]
                status = "Affected"
                cause = anchor["cause"]
                source_distance = 0.0

        plants.append(
            {
                "id": f"P-{r:02d}-{c:02d}",
                "row": r,
                "col": c,
                "risk": round(risk, 3),
                "status": status,
                "cause": cause,
                "source_distance": source_distance,
            }
        )

stats = {
    "total": len(plants),
    "healthy": sum(p["status"] == "Healthy" for p in plants),
    "risk": sum(p["status"] == "At Risk" for p in plants),
    "affected": sum(p["status"] == "Affected" for p in plants),
}

payload = json.dumps({"rows": ROWS, "cols": COLS, "plants": plants})

# ------------------------------------------------------------
# Light / green theme from the supplied reference screenshot
# ------------------------------------------------------------
st.markdown(
    """
    <style>
      .stApp { background:#f4f8f4; }
      [data-testid="stHeader"] { background:transparent; }
      [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
      .block-container { max-width:1240px; padding:1rem 2rem 2.5rem; }
      .badge { display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;background:#e7f4ee;color:#147855;font-size:13px;font-weight:750;margin-bottom:14px; }
      .badge i { width:9px;height:9px;border-radius:50%;display:inline-block;background:#31bd79; }
      .title { margin:0;color:#18262c;font-size:clamp(36px,4vw,54px);line-height:1.02;letter-spacing:-2px;font-weight:820; }
      .title span { color:#087d58; }
      .subtitle { color:#68777d;font-size:14px;line-height:1.7;max-width:780px;margin:12px 0 20px; }
      .stat-row { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px; }
      .stat { background:#fff;border:1px solid #dbe4e0;border-radius:14px;padding:13px 15px;box-shadow:0 7px 22px rgba(34,67,52,.04); }
      .stat small { display:block;color:#78878b;font-size:11px;margin-bottom:3px; }
      .stat strong { font-size:20px;color:#1d3439; }
      .stat.green strong { color:#087d58; }
      .stat.yellow strong { color:#c28a14; }
      .stat.red strong { color:#cc4c4c; }
      .guide { background:#eaf5ef;border:1px solid #d8ebe0;border-radius:14px;padding:11px 14px;color:#47625a;font-size:12px;margin-bottom:14px; }
      @media(max-width:800px){ .stat-row{grid-template-columns:repeat(2,1fr);} .block-container{padding-left:1rem;padding-right:1rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="badge"><i></i>Plant-to-Plant Risk Analysis • Sample</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">See how risk moves<br><span>from plant to plant.</span></h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Hover over any plant to inspect its estimated infection risk, likely nearby source, source distance and the number of neighbouring plants currently at risk.</p>',
    unsafe_allow_html=True,
)

healthy_pct = round(stats["healthy"] / stats["total"] * 100)
risk_pct = round(stats["risk"] / stats["total"] * 100)
affected_pct = 100 - healthy_pct - risk_pct

st.markdown(
    f'''
    <div class="stat-row">
      <div class="stat"><small>Plants monitored</small><strong>{stats["total"]}</strong></div>
      <div class="stat green"><small>Healthy</small><strong>{healthy_pct}%</strong></div>
      <div class="stat yellow"><small>At Risk</small><strong>{risk_pct}%</strong></div>
      <div class="stat red"><small>Affected</small><strong>{affected_pct}%</strong></div>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="guide"><b>Try it:</b> move your cursor over a plant. The plant is highlighted and a risk panel appears. Click a plant to keep its details selected.</div>',
    unsafe_allow_html=True,
)

html = r'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
:root{--ink:#193137;--line:#d7e2dd;--green:#159465;--yellow:#eab34b;--red:#e06468}
*{box-sizing:border-box}
body{margin:0;background:transparent;font-family:Inter,"Segoe UI",Arial,sans-serif;color:var(--ink)}
.frame{background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 16px 45px rgba(30,62,49,.07)}
.toolbar{min-height:54px;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 14px;border-bottom:1px solid #e2e9e5;background:#fbfdfb}
.toolbar-left{display:flex;align-items:center;gap:9px;min-width:0}.live-dot{width:8px;height:8px;border-radius:50%;background:#21a970;box-shadow:0 0 0 4px rgba(33,169,112,.10);flex:none}.toolbar-title{font-size:13px;font-weight:780;white-space:nowrap}.toolbar-sub{color:#8a989c;font-size:10px;white-space:nowrap}.toolbar-right{display:flex;align-items:center;gap:8px;color:#708085;font-size:10px;white-space:nowrap}
button{border:1px solid #d4dfda;background:#fff;color:#5b6d72;border-radius:9px;padding:7px 9px;cursor:pointer;font-size:10px}button:hover{border-color:#a9c9bb;color:#19694f}
#viewport{position:relative;height:590px;overflow:hidden;background:radial-gradient(circle at 13% 16%,rgba(74,170,112,.13),transparent 24%),radial-gradient(circle at 82% 78%,rgba(64,164,108,.10),transparent 27%),#edf5ef;cursor:default}
#field{position:absolute;left:50%;top:50%;width:850px;height:510px;transform:translate(-50%,-50%);border-radius:22px;overflow:hidden;border:1px solid rgba(83,127,104,.22);background:repeating-linear-gradient(0deg,rgba(31,104,65,.035) 0 2px,transparent 2px 30px),repeating-linear-gradient(90deg,rgba(31,104,65,.025) 0 1px,transparent 1px 40px),linear-gradient(145deg,#dfeee1,#d0e6d4 55%,#c6dfcb);box-shadow:inset 0 0 55px rgba(25,83,47,.10)}
.ridge{position:absolute;left:-10px;width:870px;height:30px;border-radius:50%;border-top:1px solid rgba(79,127,93,.15);border-bottom:1px solid rgba(79,127,93,.08);background:rgba(112,155,111,.055)}.r1{top:73px;transform:rotate(-1deg)}.r2{top:238px;transform:rotate(.8deg)}.r3{top:402px;transform:rotate(-.7deg)}
.water{position:absolute;width:132px;height:72px;right:18px;bottom:12px;border-radius:52% 48% 45% 55%;background:linear-gradient(135deg,#a8ced0,#8cbabc);opacity:.55}
.plant{position:absolute;width:34px;height:34px;transform:translate(-50%,-50%);cursor:pointer;z-index:3}
.stem{position:absolute;left:16px;top:12px;width:2px;height:20px;background:var(--plant-dark);border-radius:999px;transform:rotate(5deg);transform-origin:bottom}.leaf{position:absolute;width:16px;height:9px;border-radius:100% 0 100% 0;background:var(--plant);box-shadow:inset 1px 1px 0 rgba(255,255,255,.25)}.leaf.a{left:3px;top:11px;transform:rotate(25deg)}.leaf.b{left:16px;top:7px;transform:rotate(-27deg)}.leaf.c{left:7px;top:20px;transform:rotate(13deg)}.leaf.d{left:18px;top:18px;transform:rotate(-15deg)}
.healthy{--plant:#59b879;--plant-dark:#3c9361}.risk{--plant:#eab34b;--plant-dark:#ae7f23}.affected{--plant:#e06468;--plant-dark:#a83b42}
.plant .ring{position:absolute;left:50%;top:50%;width:46px;height:46px;transform:translate(-50%,-50%);border-radius:50%;border:2px solid transparent;pointer-events:none;transition:.12s ease}.plant:hover .ring,.plant.selected .ring{width:57px;height:57px;border-color:rgba(15,132,88,.55);box-shadow:0 0 0 6px rgba(15,132,88,.08)}
.heat{position:absolute;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;mix-blend-mode:multiply}.heat.red{background:radial-gradient(circle,rgba(225,81,87,.25),rgba(225,81,87,.12) 34%,transparent 70%)}
.scan{position:absolute;width:92px;height:92px;transform:translate(-50%,-50%);border-radius:50%;border:1px solid rgba(12,135,88,.50);box-shadow:0 0 0 1px rgba(12,135,88,.08),inset 0 0 25px rgba(12,135,88,.06);pointer-events:none;opacity:0;transition:opacity .10s;z-index:30}.scan.on{opacity:1}.scan:before{content:"";position:absolute;inset:13px;border-radius:50%;border:1px dashed rgba(12,135,88,.35)}.scan:after{content:"";position:absolute;left:50%;top:50%;width:8px;height:8px;transform:translate(-50%,-50%);border-radius:50%;background:#139565;box-shadow:0 0 0 4px rgba(19,149,101,.12)}
.tip{position:absolute;min-width:230px;max-width:275px;padding:12px 13px;border-radius:14px;background:rgba(255,255,255,.98);border:1px solid #d6e2dd;box-shadow:0 18px 45px rgba(30,63,48,.17);pointer-events:none;opacity:0;transform:translateY(5px);transition:.10s ease;z-index:100}.tip.show{opacity:1;transform:translateY(0)}.tip-title{display:flex;justify-content:space-between;gap:8px;align-items:center;margin-bottom:7px}.tip-name{font-size:13px;font-weight:820;color:#20383e}.status{padding:4px 7px;border-radius:999px;font-size:9px;font-weight:800;white-space:nowrap}.status.healthy{color:#138053;background:#e6f5ec}.status.risk{color:#a97913;background:#fcf2d9}.status.affected{color:#bd484d;background:#fae7e8}.tip-risk{font-size:23px;font-weight:850;color:#152f35;letter-spacing:-.5px}.tip-risk small{color:#77878b;font-size:10px;font-weight:650}.meter{height:7px;margin:7px 0 9px;background:#edf1ef;border-radius:999px;overflow:hidden}.meter>i{display:block;height:100%;border-radius:999px}.kv{display:flex;justify-content:space-between;gap:12px;font-size:10px;line-height:1.7}.kv span:first-child{color:#839095}.kv span:last-child{color:#33484d;font-weight:700;text-align:right}.tip-foot{border-top:1px solid #edf1ef;margin-top:8px;padding-top:8px;color:#6d7d81;font-size:9px;line-height:1.45}
.legend{min-height:47px;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:9px 14px;border-top:1px solid #e0e8e4;background:#fbfdfb;color:#728186;font-size:10px}.legend-left{display:flex;align-items:center;gap:15px}.legend-item{display:flex;align-items:center;gap:6px;white-space:nowrap}.legend-dot{width:9px;height:9px;border-radius:50%}.legend-dot.green{background:#57b779}.legend-dot.yellow{background:#eab34b}.legend-dot.red{background:#e06468}.legend-right{text-align:right}
@media(max-width:900px){#viewport{height:500px}#field{transform:translate(-50%,-50%) scale(.88)}.toolbar-sub,.legend-right{display:none}}
</style>
</head>
<body>
<div class="frame">
  <div class="toolbar">
    <div class="toolbar-left"><span class="live-dot"></span><span class="toolbar-title">Live field risk map</span><span class="toolbar-sub">Plant-to-plant propagation sample</span></div>
    <div class="toolbar-right"><span id="selectedText">Hover a plant</span><button id="reset">Reset</button></div>
  </div>
  <div id="viewport">
    <div id="field">
      <div class="ridge r1"></div><div class="ridge r2"></div><div class="ridge r3"></div><div class="water"></div>
      <div id="heatLayer"></div><div id="plantLayer"></div><div id="scan" class="scan"></div><div id="tip" class="tip"></div>
    </div>
  </div>
  <div class="legend">
    <div class="legend-left"><span class="legend-item"><i class="legend-dot green"></i>Healthy</span><span class="legend-item"><i class="legend-dot yellow"></i>At Risk</span><span class="legend-item"><i class="legend-dot red"></i>Affected</span></div>
    <div class="legend-right">Hover = inspect &nbsp; • &nbsp; Click = keep selected</div>
  </div>
</div>
<script>
const DATA = __PAYLOAD__;
const plants = DATA.plants;
const field = document.getElementById("field");
const plantLayer = document.getElementById("plantLayer");
const heatLayer = document.getElementById("heatLayer");
const scan = document.getElementById("scan");
const tip = document.getElementById("tip");
const selectedText = document.getElementById("selectedText");
let selectedIndex = null;

function statusClass(status){
  if(status === "Affected") return "affected";
  if(status === "At Risk") return "risk";
  return "healthy";
}
function riskColor(status){
  if(status === "Affected") return "#e06468";
  if(status === "At Risk") return "#eab34b";
  return "#57b779";
}
function nearbyAtRisk(index){
  const p = plants[index];
  return plants.filter(q => q !== p && Math.hypot(q.row-p.row,q.col-p.col) <= 2.8 && q.status !== "Healthy").length;
}
function plantMarkup(){
  return '<div class="ring"></div><span class="stem"></span><span class="leaf a"></span><span class="leaf b"></span><span class="leaf c"></span><span class="leaf d"></span>';
}
function renderHeats(){
  heatLayer.innerHTML = "";
  plants.filter(p => p.status === "Affected").forEach(p => {
    const e = document.createElement("div");
    e.className = "heat red";
    e.style.left = ((p.col-1)*35.8+38)+"px";
    e.style.top = ((p.row-1)*33+25)+"px";
    e.style.width = "150px";
    e.style.height = "150px";
    heatLayer.appendChild(e);
  });
}
function renderPlants(){
  plantLayer.innerHTML = "";
  const padX=38,padY=25,stepX=35.8,stepY=33;
  plants.forEach((p,index)=>{
    const el=document.createElement("div");
    el.className="plant "+statusClass(p.status);
    el.dataset.index=index;
    el.style.left=(padX+(p.col-1)*stepX)+"px";
    el.style.top=(padY+(p.row-1)*stepY)+"px";
    el.innerHTML=plantMarkup();
    el.addEventListener("mouseenter",()=>showHover(index));
    el.addEventListener("mouseleave",()=>{ if(selectedIndex===null) hideHover(); });
    el.addEventListener("click",event=>{
      event.stopPropagation();
      selectedIndex=index;
      document.querySelectorAll(".plant.selected").forEach(node=>node.classList.remove("selected"));
      el.classList.add("selected");
      showHover(index);
      selectedText.textContent=p.id+" selected";
    });
    plantLayer.appendChild(el);
  });
}
function showHover(index){
  const p=plants[index];
  const riskPct=Math.round(p.risk*100);
  const nearby=nearbyAtRisk(index);
  const cause=p.cause === "Low exposure" ? "No strong nearby source" : p.cause;
  const source=p.source_distance===null ? "—" : (p.source_distance===0 ? "This plant" : p.source_distance+" grid units away");

  tip.innerHTML=`
    <div class="tip-title"><div class="tip-name">${p.id}</div><div class="status ${statusClass(p.status)}">${p.status}</div></div>
    <div class="tip-risk">${riskPct}% <small>estimated infection risk</small></div>
    <div class="meter"><i style="width:${riskPct}%;background:${riskColor(p.status)}"></i></div>
    <div class="kv"><span>Likely source</span><span>${cause}</span></div>
    <div class="kv"><span>Source distance</span><span>${source}</span></div>
    <div class="kv"><span>Nearby at risk</span><span>${nearby} plants</span></div>
    <div class="kv"><span>Field position</span><span>R${p.row} · C${p.col}</span></div>
    <div class="tip-foot">Sample propagation score: nearby affected plants increase local risk, with influence decreasing as distance grows.</div>`;

  const x=(p.col-1)*35.8+38;
  const y=(p.row-1)*33+25;
  scan.style.left=x+"px";
  scan.style.top=y+"px";
  scan.classList.add("on");

  const tipW=260,tipH=190;
  let left=x+26;
  if(left+tipW>850) left=x-tipW-25;
  let top=y-20;
  if(top+tipH>510) top=510-tipH-10;
  if(top<10) top=10;
  if(left<10) left=10;
  tip.style.left=left+"px";
  tip.style.top=top+"px";
  tip.classList.add("show");
}
function hideHover(){
  tip.classList.remove("show");
  scan.classList.remove("on");
  selectedText.textContent="Hover a plant";
}
document.getElementById("reset").addEventListener("click",()=>{
  selectedIndex=null;
  document.querySelectorAll(".plant.selected").forEach(node=>node.classList.remove("selected"));
  hideHover();
});
field.addEventListener("click",()=>{
  selectedIndex=null;
  document.querySelectorAll(".plant.selected").forEach(node=>node.classList.remove("selected"));
  hideHover();
});
renderHeats();
renderPlants();
</script>
</body>
</html>'''.replace("__PAYLOAD__", payload)

components.html(html, height=710, scrolling=False)
