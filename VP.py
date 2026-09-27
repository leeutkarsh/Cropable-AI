from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ============================================================
# V-Hybrid Predictor — non-functional UI prototype
# ============================================================
st.set_page_config(
    page_title="V-Hybrid Predictor • Prakriti-AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"


# ------------------------------------------------------------------
# Synthetic presentation dataset
# ------------------------------------------------------------------
CROPS = {
    "Rice": {
        "image": "rice.png",
        "parents": {
            "IR-64": {
                "yield": 78, "disease": 72, "heat": 64, "drought": 58,
                "pest": 68, "grain": 81, "market": 74, "duration": 122
            },
            "Swarna": {
                "yield": 75, "disease": 82, "heat": 69, "drought": 67,
                "pest": 71, "grain": 77, "market": 79, "duration": 135
            },
            "MTU-1010": {
                "yield": 71, "disease": 76, "heat": 76, "drought": 63,
                "pest": 74, "grain": 74, "market": 72, "duration": 120
            },
            "Pusa Basmati 1121": {
                "yield": 67, "disease": 70, "heat": 71, "drought": 60,
                "pest": 66, "grain": 96, "market": 94, "duration": 145
            },
        },
    },
    "Wheat": {
        "image": "wheat.png",
        "parents": {
            "HD-2967": {
                "yield": 82, "disease": 70, "heat": 61, "drought": 64,
                "pest": 68, "grain": 83, "market": 76, "duration": 128
            },
            "DBW-187": {
                "yield": 84, "disease": 78, "heat": 69, "drought": 72,
                "pest": 70, "grain": 86, "market": 82, "duration": 120
            },
            "WH-1105": {
                "yield": 79, "disease": 74, "heat": 74, "drought": 67,
                "pest": 72, "grain": 81, "market": 79, "duration": 124
            },
            "PBW-725": {
                "yield": 76, "disease": 80, "heat": 66, "drought": 70,
                "pest": 73, "grain": 88, "market": 84, "duration": 126
            },
        },
    },
    "Maize": {
        "image": "maize.png",
        "parents": {
            "Pioneer-3396": {
                "yield": 86, "disease": 67, "heat": 79, "drought": 72,
                "pest": 65, "grain": 82, "market": 78, "duration": 118
            },
            "HQPM-7": {
                "yield": 89, "disease": 73, "heat": 75, "drought": 69,
                "pest": 72, "grain": 90, "market": 86, "duration": 115
            },
            "DKC-9108": {
                "yield": 91, "disease": 69, "heat": 83, "drought": 77,
                "pest": 68, "grain": 84, "market": 81, "duration": 112
            },
            "Vivek QPM-9": {
                "yield": 80, "disease": 81, "heat": 71, "drought": 73,
                "pest": 80, "grain": 88, "market": 83, "duration": 108
            },
        },
    },
}


# Trait display configuration.
TRAITS = {
    "yield": "Yield Potential",
    "disease": "Disease Tolerance",
    "heat": "Heat Tolerance",
    "drought": "Drought Tolerance",
    "pest": "Pest Tolerance",
    "grain": "Grain / Quality",
    "market": "Market Value Index",
}

# Which traits are shown in the main biological comparison.
BIO_TRAITS = ["yield", "disease", "heat", "drought", "pest", "grain"]


def asset_uri(filename: str) -> str:
    """Return a local file path usable by st.image."""
    path = ASSET_DIR / filename
    return str(path) if path.exists() else ""


def predict_hybrid(parent_a: dict, parent_b: dict) -> dict:
    """
    Synthetic prototype rule standing in for an ANN.
    This deliberately is NOT a trained model; it only creates a
    presentation-ready predicted hybrid profile.
    """
    result = {}

    # Base inheritance + modest simulated heterosis.
    for key in ["yield", "disease", "heat", "drought", "pest", "grain"]:
        avg = (parent_a[key] + parent_b[key]) / 2
        if key in {"yield", "grain"}:
            gain = 8
        elif key in {"disease", "heat", "drought", "pest"}:
            gain = 5
        else:
            gain = 0
        result[key] = min(99, round(avg + gain))

    # Market value is influenced by quality, yield and resilience in this UI demo.
    result["market"] = min(
        99,
        round(
            0.38 * result["grain"]
            + 0.28 * result["yield"]
            + 0.17 * result["disease"]
            + 0.17 * result["heat"]
        ),
    )

    # Faster than the slower parent by a small synthetic margin.
    result["duration"] = round((parent_a["duration"] + parent_b["duration"]) / 2 - 4)

    return result


def score_label(value: int) -> str:
    if value >= 85:
        return "High"
    if value >= 70:
        return "Moderate"
    return "Developing"


# ------------------------------------------------------------------
# Styling — same light, botanical green visual language
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
      .stApp { background:#f4f8f4; color:#1a2a2e; }
      [data-testid="stHeader"] { background:transparent; }
      [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
      .block-container { max-width:1320px; padding:1rem 2rem 3rem; }

      .badge{
        display:inline-flex;align-items:center;gap:8px;
        padding:7px 14px;border-radius:999px;
        background:#e7f4ee;color:#147855;
        font-size:13px;font-weight:800;margin-bottom:14px;
      }
      .badge i{
        width:9px;height:9px;border-radius:50%;
        display:inline-block;background:#31bd79;
      }

      .title{
        margin:0;color:#18272d;
        font-size:clamp(36px,4vw,55px);
        line-height:1.02;letter-spacing:-2px;font-weight:830;
      }
      .title span{ color:#087d58; }
      .subtitle{
        color:#69787d;font-size:14px;line-height:1.7;
        max-width:880px;margin:12px 0 18px;
      }

      .top-note{
        background:#eaf5ef;border:1px solid #d8ebe0;
        border-radius:14px;padding:11px 14px;
        color:#49645c;font-size:12px;margin:0 0 16px;
      }

      .control-card,.parent-card,.prediction-card,.insight-card{
        background:#fff;border:1px solid #dbe4e0;
        border-radius:17px;
        box-shadow:0 9px 28px rgba(30,65,48,.045);
      }

      .st-key-control_card{
        background:#fff !important;
        border:1px solid #dbe4e0 !important;
        border-radius:17px !important;
        box-shadow:0 9px 28px rgba(30,65,48,.045) !important;
        padding:17px 18px 15px !important;
      }

      .control-title{
        color:#22393e;font-size:16px;font-weight:820;margin-bottom:4px;
      }
      .control-sub{
        color:#77868b;font-size:12px;margin-bottom:13px;
      }

      .field-label{
        color:#607278;font-size:11px;font-weight:800;
        margin:1px 0 6px;
      }

      div[data-baseweb="select"] > div{
        background:#f8faf9 !important;
        border:1px solid #dfe7e3 !important;
        border-radius:10px !important;
        min-height:44px;
      }

      div[data-testid="stSelectbox"] label{
        display:none !important;
      }

      .parent-card{
        padding:15px;
        height:100%;
      }

      .parent-head{
        display:flex;align-items:center;justify-content:space-between;
        gap:12px;margin-bottom:12px;
      }

      .parent-name{
        font-size:17px;font-weight:850;color:#20363b;
      }

      .parent-tag{
        font-size:9px;font-weight:800;color:#18805a;
        background:#e7f5ed;border-radius:999px;padding:5px 7px;
      }

      .parent-photo{
        width:100%;height:145px;object-fit:cover;
        border-radius:12px;border:1px solid #d9e3de;
        background:#edf5ef;
      }

      .trait-list{ margin-top:12px;display:grid;gap:8px; }
      .trait-row{
        display:flex;justify-content:space-between;gap:12px;
        align-items:center;font-size:10px;
      }
      .trait-row span:first-child{ color:#7b898e; }
      .trait-row b{ color:#334a4f; }

      .mini-meter{
        height:5px;background:#edf1ef;border-radius:99px;
        overflow:hidden;margin-top:3px;
      }
      .mini-meter i{ display:block;height:100%;border-radius:99px;background:#59b77a; }

      .prediction-card{
        padding:18px;
        border-color:#cfe3d8;
        background:linear-gradient(145deg,#fbfffc,#edf8f1);
      }

      .pred-kicker{
        color:#16825b;font-size:10px;font-weight:850;
        letter-spacing:.8px;text-transform:uppercase;
      }
      .pred-title{
        color:#18363a;font-size:24px;font-weight:850;
        letter-spacing:-.6px;margin-top:3px;
      }

      .network{
        margin:13px 0 15px;
        display:grid;grid-template-columns:1fr 80px 1fr;
        gap:8px;align-items:center;
      }

      .node{
        border:1px solid #d5e4dc;border-radius:11px;
        padding:10px;text-align:center;background:#fff;
        color:#345158;font-size:10px;font-weight:800;
      }

      .ann-box{
        border:1px solid #a8d6bd;border-radius:14px;
        padding:10px 5px;background:#e6f6ed;
        text-align:center;color:#157e58;font-weight:900;
        font-size:10px;box-shadow:inset 0 0 25px rgba(55,173,112,.08);
      }

      .ann-dots{
        display:flex;justify-content:center;gap:4px;margin:6px 0 2px;
      }
      .ann-dots i{
        width:5px;height:5px;border-radius:50%;background:#3ab37a;
      }

      .prediction-grid{
        display:grid;grid-template-columns:repeat(4,1fr);
        gap:8px;margin-top:10px;
      }

      .prediction-metric{
        background:#fff;border:1px solid #dce8e1;
        border-radius:11px;padding:9px 7px;text-align:center;
      }

      .prediction-metric small{
        display:block;color:#7c898e;font-size:9px;
      }

      .prediction-metric b{
        display:block;color:#1a3b40;font-size:18px;margin-top:2px;
      }

      .prediction-metric .green{ color:#087d58; }

      .confidence{
        margin-top:12px;padding-top:11px;
        border-top:1px solid #dbe8e0;
        display:flex;justify-content:space-between;gap:10px;
        color:#6c7d81;font-size:10px;
      }
      .confidence b{color:#167c56;}

      .section-head{
        color:#20363b;font-size:17px;font-weight:850;
        margin:20px 0 8px;
      }
      .section-sub{
        color:#77868b;font-size:12px;margin-bottom:10px;
      }

      .insight-card{padding:14px 16px;}
      .insight-title{font-size:13px;font-weight:850;color:#274047;}
      .insight-text{font-size:11px;line-height:1.6;color:#697a7f;margin-top:4px;}

      @media(max-width:900px){
        .prediction-grid{grid-template-columns:repeat(2,1fr);}
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown(
    '<div class="badge"><i></i>AI-assisted crop hybrid outcome prediction</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="title">Predict the hybrid<br><span>before you cross.</span></h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="subtitle">
      V-Hybrid Predictor is a presentation prototype for estimating how a potential
      plant cross could perform before physically making the cross. Compare two parent
      profiles, pass their traits through a simulated ANN prediction layer, and inspect
      the expected hybrid profile — including yield, disease tolerance, heat tolerance,
      drought tolerance, quality and market value.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="top-note"><b>Prototype:</b> all values below are synthetic demonstration data. '
    'The ANN block represents where a trained ML/DL model would plug into the real system; '
    'the charts are not claims about actual cultivar performance or market prices.</div>',
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Controls
# ------------------------------------------------------------------
with st.container(key="control_card"):
    st.markdown('<div class="control-title">Build a potential cross</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="control-sub">Choose the crop and two parent varieties to create a sample hybrid prediction.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([0.85, 1, 1], gap="large")

    with c1:
        st.markdown('<div class="field-label">Crop</div>', unsafe_allow_html=True)
        crop = st.selectbox("crop", list(CROPS.keys()), label_visibility="collapsed")

    parent_names = list(CROPS[crop]["parents"].keys())

    with c2:
        st.markdown('<div class="field-label">Parent A</div>', unsafe_allow_html=True)
        parent_a_name = st.selectbox(
            "parent_a",
            parent_names,
            index=0,
            label_visibility="collapsed",
        )

    with c3:
        st.markdown('<div class="field-label">Parent B</div>', unsafe_allow_html=True)
        parent_b_name = st.selectbox(
            "parent_b",
            parent_names,
            index=1 if len(parent_names) > 1 else 0,
            label_visibility="collapsed",
        )


parent_a = CROPS[crop]["parents"][parent_a_name]
parent_b = CROPS[crop]["parents"][parent_b_name]
hybrid = predict_hybrid(parent_a, parent_b)


# ------------------------------------------------------------------
# Parent comparison + ANN prediction
# ------------------------------------------------------------------
pa, ann, pb = st.columns([1, 1.25, 1], gap="medium")

def parent_card(name, data, letter):
    image_file = asset_uri(CROPS[crop]["image"])
    rows = ""
    for key in BIO_TRAITS:
        pct = data[key]
        rows += (
            f'<div class="trait-row"><span>{TRAITS[key]}</span><b>{pct}</b></div>'
            f'<div class="mini-meter"><i style="width:{pct}%"></i></div>'
        )

    st.markdown(
        f"""
        <div class="parent-card">
          <div class="parent-head">
            <div class="parent-name">Parent {letter}</div>
            <div class="parent-tag">REFERENCE</div>
          </div>
          <div style="font-size:15px;font-weight:850;color:#264149;margin-bottom:9px;">{name}</div>
          {f'<img class="parent-photo" src="{image_file}" alt="{crop}">' if image_file else ''}
          <div class="trait-list">{rows}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with pa:
    parent_card(parent_a_name, parent_a, "A")

with ann:
    st.markdown(
        f"""
        <div class="prediction-card">
          <div class="pred-kicker">Simulated ML / DL prediction layer</div>
          <div class="pred-title">{parent_a_name} × {parent_b_name}</div>

          <div class="network">
            <div class="node">Parent A<br><span style="font-weight:600;color:#829095;">phenotype + history</span></div>
            <div class="ann-box">
              ANN
              <div class="ann-dots"><i></i><i></i><i></i><i></i><i></i></div>
              trait fusion
            </div>
            <div class="node">Parent B<br><span style="font-weight:600;color:#829095;">phenotype + history</span></div>
          </div>

          <div style="font-size:10px;color:#718186;font-weight:700;">Predicted hybrid profile</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4, gap="small")
    with m1:
        st.markdown(
            f'<div class="prediction-metric"><small>Yield</small><b class="green">{hybrid["yield"]}</b></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="prediction-metric"><small>Disease</small><b>{hybrid["disease"]}</b></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="prediction-metric"><small>Heat</small><b>{hybrid["heat"]}</b></div>',
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f'<div class="prediction-metric"><small>Market Index</small><b class="green">{hybrid["market"]}</b></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="confidence">
          <span>Prediction confidence</span>
          <b>87% · prototype score</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

with pb:
    parent_card(parent_b_name, parent_b, "B")


# ------------------------------------------------------------------
# Comparative charts
# ------------------------------------------------------------------
st.markdown('<div class="section-head">Hybrid vs parent performance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Side-by-side trait comparison for the selected cross. '
    'Higher scores indicate stronger projected performance in this prototype.</div>',
    unsafe_allow_html=True,
)

labels = [TRAITS[k] for k in BIO_TRAITS]
a_values = [parent_a[k] for k in BIO_TRAITS]
b_values = [parent_b[k] for k in BIO_TRAITS]
h_values = [hybrid[k] for k in BIO_TRAITS]

left_chart, right_chart = st.columns([1.15, 1], gap="large")

with left_chart:
    comparison = pd.DataFrame(
        {
            "Trait": labels * 3,
            "Score": a_values + b_values + h_values,
            "Profile": (
                [f"Parent A • {parent_a_name}"] * len(labels)
                + [f"Parent B • {parent_b_name}"] * len(labels)
                + ["Predicted Hybrid"] * len(labels)
            ),
        }
    )

    fig_bar = px.bar(
        comparison,
        x="Trait",
        y="Score",
        color="Profile",
        barmode="group",
        range_y=[0, 100],
        text="Score",
    )
    fig_bar.update_traces(textposition="outside", cliponaxis=False)
    fig_bar.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=25, b=80),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(color="#30464b", size=11),
        legend=dict(orientation="h", y=1.06, x=0),
        xaxis=dict(showgrid=False, tickangle=-18),
        yaxis=dict(showgrid=True, gridcolor="#e8eeeb", title="Score / 100"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with right_chart:
    radar = go.Figure()

    for name, values, line_color in [
        (parent_a_name, a_values, "#82b99a"),
        (parent_b_name, b_values, "#d7a54c"),
        ("Predicted Hybrid", h_values, "#10895f"),
    ]:
        radar.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name=name,
                line=dict(color=line_color, width=2),
                opacity=0.68 if name != "Predicted Hybrid" else 0.92,
            )
        )

    radar.update_layout(
        height=450,
        margin=dict(l=25, r=25, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#dfe8e2",
                linecolor="#dfe8e2",
                tickfont=dict(size=9, color="#718186"),
            ),
            angularaxis=dict(
                gridcolor="#dfe8e2",
                linecolor="#dfe8e2",
                tickfont=dict(size=10, color="#4a5d62"),
            ),
        ),
        legend=dict(orientation="h", y=1.08, x=0),
        font=dict(color="#30464b", size=11),
    )
    st.plotly_chart(radar, use_container_width=True, config={"displayModeBar": False})


# ------------------------------------------------------------------
# Market value / commercial comparison
# ------------------------------------------------------------------
st.markdown('<div class="section-head">Commercial potential</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">The prototype expresses market value as an index, not a live rupee price. '
    'It is derived from the simulated quality, yield and resilience profile.</div>',
    unsafe_allow_html=True,
)

market_df = pd.DataFrame(
    {
        "Profile": [parent_a_name, parent_b_name, "Predicted Hybrid"],
        "Market Value Index": [parent_a["market"], parent_b["market"], hybrid["market"]],
        "Yield Potential": [parent_a["yield"], parent_b["yield"], hybrid["yield"]],
        "Quality": [parent_a["grain"], parent_b["grain"], hybrid["grain"]],
    }
)

market_chart = go.Figure()
market_chart.add_bar(
    x=market_df["Profile"],
    y=market_df["Market Value Index"],
    text=market_df["Market Value Index"],
    textposition="outside",
    name="Market Value Index",
)
market_chart.update_layout(
    height=350,
    margin=dict(l=10, r=10, t=25, b=45),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    font=dict(color="#30464b", size=11),
    showlegend=False,
    yaxis=dict(range=[0, 105], title="Index / 100", gridcolor="#e8eeeb"),
    xaxis=dict(showgrid=False),
)

market_col1, market_col2 = st.columns([1.15, .85], gap="large")

with market_col1:
    st.plotly_chart(market_chart, use_container_width=True, config={"displayModeBar": False})

with market_col2:
    st.markdown(
        f"""
        <div class="insight-card">
          <div class="insight-title">Predicted hybrid snapshot</div>
          <div class="insight-text">
            <b>Yield:</b> {hybrid["yield"]}/100<br>
            <b>Disease tolerance:</b> {hybrid["disease"]}/100<br>
            <b>Heat tolerance:</b> {hybrid["heat"]}/100<br>
            <b>Drought tolerance:</b> {hybrid["drought"]}/100<br>
            <b>Pest tolerance:</b> {hybrid["pest"]}/100<br>
            <b>Quality:</b> {hybrid["grain"]}/100<br>
            <b>Market value index:</b> {hybrid["market"]}/100<br>
            <b>Projected duration:</b> ~{hybrid["duration"]} days
          </div>
        </div>

        <div class="insight-card" style="margin-top:10px;">
          <div class="insight-title">Why this matters</div>
          <div class="insight-text">
            Instead of crossing every possible pair physically, a real trained model could
            rank candidate crosses first. Breeders could then reserve field trials for
            combinations with promising predicted trait profiles.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# Trait summary table
# ------------------------------------------------------------------
st.markdown('<div class="section-head">Trait-by-trait comparison</div>', unsafe_allow_html=True)

table = pd.DataFrame(
    {
        "Trait": [TRAITS[k] for k in ["yield", "disease", "heat", "drought", "pest", "grain", "market"]],
        parent_a_name: [parent_a[k] for k in ["yield", "disease", "heat", "drought", "pest", "grain", "market"]],
        parent_b_name: [parent_b[k] for k in ["yield", "disease", "heat", "drought", "pest", "grain", "market"]],
        "Predicted Hybrid": [hybrid[k] for k in ["yield", "disease", "heat", "drought", "pest", "grain", "market"]],
    }
)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Trait": st.column_config.TextColumn("Trait"),
        parent_a_name: st.column_config.ProgressColumn(
            parent_a_name, min_value=0, max_value=100, format="%d"
        ),
        parent_b_name: st.column_config.ProgressColumn(
            parent_b_name, min_value=0, max_value=100, format="%d"
        ),
        "Predicted Hybrid": st.column_config.ProgressColumn(
            "Predicted Hybrid", min_value=0, max_value=100, format="%d"
        ),
    },
)

st.markdown(
    """
    <div class="top-note" style="margin-top:14px;margin-bottom:0;">
      <b>Prototype note:</b> This screen intentionally demonstrates the product concept,
      data flow and decision-support visuals. In the real V-Hybrid Predictor, the
      synthetic scoring layer would be replaced with trained ANN/ML models using
      validated phenotypic, genomic, environmental and historical trial data.
    </div>
    """,
    unsafe_allow_html=True,
)
