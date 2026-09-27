import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Prakriti AI • Rice Borer Outbreak",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Theme / CSS
# ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f3f8f5;
        --card: #ffffff;
        --soft: #e6f2ec;
        --soft-2: #eef7f2;
        --green: #157a57;
        --green-dark: #0b5b43;
        --mint: #9de4c1;
        --text: #13231d;
        --muted: #6c7a74;
        --line: #dbe8e1;
        --amber: #d68a18;
        --red: #b94747;
    }

    html, body, [class*="css"] {
        font-family: "Noto Sans Devanagari", "Nirmala UI", "Segoe UI", sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }

    section.main > div {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .hero {
        padding: 4px 0 8px 0;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 15px;
        background: #e4f3ec;
        border-radius: 999px;
        color: var(--green-dark);
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        display: inline-block;
        background: #44cc8d;
        box-shadow: 0 0 0 4px rgba(68, 204, 141, 0.12);
    }

    .hero h1 {
        font-size: clamp(34px, 4.2vw, 58px);
        line-height: 1.08;
        letter-spacing: -1.8px;
        margin: 0 0 13px 0;
        color: #101c18;
        font-weight: 800;
    }

    .hero h1 span {
        color: var(--green);
    }

    .hero p {
        font-size: 16px;
        line-height: 1.75;
        color: #5e6d66;
        max-width: 910px;
        margin: 0;
    }

    .notice {
        background: var(--soft);
        border: 1px solid #d6ebe0;
        border-radius: 18px;
        padding: 16px 18px;
        margin-top: 18px;
        margin-bottom: 22px;
    }

    .notice b {
        color: var(--green-dark);
    }

    .section-title {
        margin: 24px 0 4px 0;
        font-size: 26px;
        font-weight: 800;
        color: #13211c;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 14px;
        margin: 0 0 14px 0;
    }

    .card {
        background: var(--card);
        border: 1px solid #e4ebe7;
        border-radius: 20px;
        padding: 21px 22px;
        box-shadow: 0 6px 22px rgba(31, 64, 50, 0.045);
        height: 100%;
    }

    .kpi-label {
        color: #718079;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 7px;
    }

    .kpi-value {
        color: #10251c;
        font-size: 31px;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-delta {
        margin-top: 7px;
        font-size: 12px;
        color: var(--green);
        font-weight: 700;
    }

    .kpi-delta.warn {
        color: var(--amber);
    }

    .mini-title {
        font-size: 17px;
        font-weight: 800;
        color: #173127;
        margin-bottom: 10px;
    }

    .legend-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 18px;
        font-size: 12px;
        color: #66766e;
        margin-top: 10px;
    }

    .legend-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }

    .hotspot {
        border: 1px solid #e3ebe6;
        border-radius: 15px;
        background: #fbfdfc;
        padding: 13px 14px;
        margin-bottom: 9px;
    }

    .hotspot-top {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        align-items: center;
    }

    .hotspot-name {
        font-size: 14px;
        font-weight: 800;
        color: #1a2e25;
    }

    .hotspot-sub {
        font-size: 11px;
        color: #76837d;
        margin-top: 2px;
    }

    .badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 800;
        white-space: nowrap;
    }

    .critical { background: #fde7e5; color: #9f3732; }
    .high { background: #fff0d8; color: #9a5c04; }
    .medium { background: #e8f4e9; color: #2b704c; }

    .progress-shell {
        height: 7px;
        border-radius: 999px;
        background: #edf3ef;
        margin-top: 10px;
        overflow: hidden;
    }

    .progress {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #7bd6aa, #157a57);
    }

    .insight {
        background: #f8fbf9;
        border: 1px solid #e1ebe5;
        border-radius: 16px;
        padding: 13px 15px;
        margin-top: 10px;
        font-size: 13px;
        line-height: 1.65;
        color: #53645b;
    }

    .insight strong {
        color: #173127;
    }

    .footer-note {
        color: #7a8781;
        font-size: 11px;
        text-align: center;
        padding: 22px 0 4px;
    }

    .table-wrap {
        border: 1px solid #e2ebe5;
        border-radius: 17px;
        overflow: hidden;
        background: white;
    }

    .source-tag {
        display: inline-block;
        background: #f1f7f4;
        color: #4d665b;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 11px;
        margin-left: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Synthetic outbreak dataset
# ----------------------------
locations = [
    ("Bhandara", "भंडारा", 21.17, 79.65, 126, 18.6, 88, "Critical", 92, 2.8, 78, "Heading"),
    ("Sakoli", "साकोली", 21.09, 79.99, 98, 16.9, 84, "High", 89, 2.5, 71, "Flowering"),
    ("Tumsar", "तुमसर", 21.38, 79.73, 86, 15.2, 81, "High", 87, 2.4, 69, "Flowering"),
    ("Gondia", "गोंदिया", 21.46, 80.19, 112, 17.4, 86, "Critical", 91, 2.7, 76, "Heading"),
    ("Tirora", "तिरोडा", 21.40, 80.06, 74, 13.8, 77, "High", 84, 2.1, 67, "Flowering"),
    ("Nagpur", "नागपूर", 21.15, 79.09, 58, 9.7, 65, "Medium", 82, 1.7, 60, "Tillering"),
    ("Wardha", "वर्धा", 20.75, 78.60, 63, 10.6, 69, "Medium", 80, 1.8, 62, "Tillering"),
    ("Amravati", "अमरावती", 20.93, 77.75, 71, 11.9, 73, "Medium", 83, 2.0, 64, "Flowering"),
    ("Yavatmal", "यवतमाळ", 20.39, 78.13, 67, 12.3, 76, "High", 86, 2.2, 66, "Flowering"),
    ("Akola", "अकोला", 20.70, 77.00, 52, 8.9, 62, "Medium", 79, 1.6, 59, "Tillering"),
    ("Washim", "वाशिम", 20.11, 77.13, 47, 8.1, 58, "Medium", 77, 1.5, 57, "Tillering"),
    ("Nanded", "नांदेड", 19.14, 77.30, 61, 10.4, 66, "Medium", 81, 1.9, 61, "Flowering"),
    ("Parbhani", "परभणी", 19.27, 76.78, 57, 10.8, 68, "Medium", 82, 1.8, 60, "Flowering"),
    ("Hingoli", "हिंगोली", 19.72, 77.15, 43, 7.4, 55, "Medium", 76, 1.4, 55, "Tillering"),
    ("Jalna", "जालना", 19.83, 75.88, 39, 6.9, 52, "Medium", 74, 1.3, 53, "Tillering"),
    ("Latur", "लातूर", 18.41, 76.56, 33, 6.1, 49, "Medium", 72, 1.2, 51, "Tillering"),
    ("Solapur", "सोलापूर", 17.66, 75.91, 28, 5.4, 45, "Medium", 70, 1.1, 49, "Vegetative"),
    ("Kolhapur", "कोल्हापूर", 16.70, 74.24, 73, 11.8, 72, "High", 85, 2.0, 65, "Flowering"),
    ("Sangli", "सांगली", 16.85, 74.58, 59, 9.8, 64, "Medium", 79, 1.6, 58, "Tillering"),
    ("Ratnagiri", "रत्नागिरी", 16.99, 73.31, 81, 12.9, 75, "High", 88, 2.3, 68, "Flowering"),
]

df = pd.DataFrame(
    locations,
    columns=[
        "City", "Marathi", "Lat", "Lon", "Affected_Ha", "Infestation_Pct",
        "Risk", "Severity", "Confidence", "Spread_Rate", "Humidity", "Crop_Stage"
    ],
)

df["Pest"] = "Yellow Rice Borer"
df["Pest_Hindi"] = "पीला तना छेदक"
df["Updated"] = "28 सितम्बर 2026"
df["Action"] = df["Severity"].map({
    "Critical": "तत्काल निगरानी + नियंत्रित उपचार",
    "High": "24 घंटे में नियंत्रण कार्रवाई",
    "Medium": "सघन निगरानी + ट्रैपिंग",
})

# Previous-year demo values for comparison
df["Affected_2025"] = (df["Affected_Ha"] / (1 + (0.18 + (df["Risk"] - 60) / 600))).round(0).astype(int)
df["Change_Pct"] = ((df["Affected_Ha"] - df["Affected_2025"]) / df["Affected_2025"] * 100).round(1)

# Summary values
affected_total = int(df["Affected_Ha"].sum())
avg_infestation = df["Infestation_Pct"].mean()
avg_risk = df["Risk"].mean()
critical_high = int((df["Severity"].isin(["Critical", "High"])).sum())
yoy_total = ((df["Affected_Ha"].sum() - df["Affected_2025"].sum()) / df["Affected_2025"].sum()) * 100
avg_conf = df["Confidence"].mean()

# Historical outbreak trend — synthetic, display-only
history = pd.DataFrame({
    "Year": [2022, 2023, 2024, 2025, 2026],
    "Affected_Ha": [610, 742, 881, 997, affected_total],
    "Reported_Hotspots": [7, 9, 12, 14, 20],
    "Avg_Risk": [42, 49, 55, 61, round(avg_risk)],
})


# ----------------------------
# Dashboard UI
# ----------------------------

# Extra polish for native Streamlit widgets
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1480px;
        padding-top: 1.1rem;
        padding-bottom: 2.5rem;
    }

    /* Native metric cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dfeae4;
        border-radius: 18px;
        padding: 15px 17px 13px 17px;
        box-shadow: 0 5px 16px rgba(34, 71, 55, .045);
    }

    [data-testid="stMetricLabel"] {
        color: #718079 !important;
        font-size: .78rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #10271d !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: .72rem !important;
    }

    /* Make chart areas feel like cards without adding empty boxes */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #dfeae4 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,.82);
        box-shadow: 0 6px 22px rgba(34,71,55,.04);
    }

    .eyebrow {
        display:inline-flex;
        align-items:center;
        gap:.45rem;
        background:#e6f4ed;
        color:#0f6d4c;
        border:1px solid #d7ebe1;
        border-radius:999px;
        padding:.42rem .78rem;
        font-size:.78rem;
        font-weight:800;
        letter-spacing:.1px;
        margin-bottom:.72rem;
    }

    .hero-title {
        font-size: clamp(2rem, 4.2vw, 3.65rem);
        line-height:1.02;
        letter-spacing:-2px;
        margin:0;
        color:#10231b;
        font-weight:850;
    }

    .hero-title span { color:#147955; }

    .hero-copy {
        margin-top:.75rem;
        color:#62736a;
        max-width:900px;
        font-size:.98rem;
        line-height:1.7;
    }

    .section-head {
        display:flex;
        align-items:flex-end;
        justify-content:space-between;
        gap:1rem;
        margin:1.35rem 0 .65rem 0;
    }

    .section-head h3 {
        margin:0;
        color:#153128;
        font-size:1.2rem;
        font-weight:850;
    }

    .section-head p {
        margin:.12rem 0 0 0;
        color:#74827a;
        font-size:.78rem;
    }

    .severity-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: fit-content;
    height: 21px;
    padding: 0 8px;
    border-radius: 999px;
    font-size: 13px;
    line-height: 1;
    font-weight: 800;
    white-space: nowrap;
    vertical-align: middle;
    box-sizing: border-box;
    }

    .pill-critical {
        background: #fde9e6;
        color: #9e3d36;
    }
    
    .pill-high {
        background: #fff2dc;
        color: #9a5e09;
    }
    
    .pill-medium {
        background: #e8f4eb;
        color: #28704c;
    }

    .hotspot-item {
        padding:.76rem .1rem;
        border-bottom:1px solid #edf2ef;
    }
    .hotspot-item:last-child { border-bottom:0; }

    .hotspot-name {
        font-size:.9rem;
        color:#193129;
        font-weight:800;
    }
    .hotspot-meta {
        color:#7a8780;
        font-size:.7rem;
        margin-top:.15rem;
    }

    .mini-stat {
        background:#f7faf8;
        border:1px solid #e7eeea;
        border-radius:14px;
        padding:.72rem .8rem;
        height:100%;
    }
    .mini-stat .label { color:#78857f; font-size:.67rem; }
    .mini-stat .value { color:#173127; font-size:1.25rem; font-weight:850; margin-top:.13rem; }

    .callout {
        background:linear-gradient(135deg,#edf8f2 0%,#f9fcfa 100%);
        border:1px solid #d9eee2;
        border-radius:18px;
        padding:.95rem 1rem;
        color:#52655c;
        font-size:.8rem;
        line-height:1.65;
    }
    .callout b { color:#174b38; }

    .table-caption {
        color:#738079;
        font-size:.74rem;
        margin:.15rem 0 .5rem 0;
    }

    .footer {
        padding:1.2rem 0 .2rem;
        text-align:center;
        color:#849089;
        font-size:.66rem;
    }
    
    .prakriti-badge {
    display: inline-block;
    background: #e8f5ef;
    color: #0f5c3a;
    font-weight: 600;
    font-size: 13px;
    padding: 6px 14px;
    border-radius: 20px;
    margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero
st.markdown(
    """
    <span class="prakriti-badge">🟢 AI-संचालित फसल निदान</span>
    <br></br>
    <div class="hero-title">प्रकोप को <span>फैलने से पहले</span><br>देखें, समझें और ट्रैक करें।</div>

    <div class="hero-copy">
        महाराष्ट्र के 20 sample regions में <b>Yellow Rice Borer / पीला तना छेदक</b>
        का visual outbreak command-center — risk, affected area, spread, yearly change
        और early-warning signals को एक ही dashboard में जोड़कर।
    </div>
    <br></br>
    """,
    unsafe_allow_html=True,
)

st.info(
    "🧪 **Showpiece dataset:** यह पूरा dashboard synthetic demo data पर आधारित है। "
    "इसे वास्तविक सरकारी कृषि सर्वेक्षण या field forecast न माना जाए।  •  Snapshot: **28 सितम्बर 2026**",
    icon="ℹ️",
)

# KPI row — native Streamlit
k1, k2, k3, k4, k5 = st.columns(5, gap="small")
with k1:
    st.metric("निगरानी क्षेत्र", "20", "शहर / गाँव")
with k2:
    st.metric("प्रभावित क्षेत्र", f"{affected_total:,} ha", f"+{yoy_total:.1f}% YoY")
with k3:
    st.metric("औसत संक्रमण", f"{avg_infestation:.1f}%", "sample average")
with k4:
    st.metric("औसत जोखिम", f"{avg_risk:.0f}/100", "outbreak score")
with k5:
    st.metric("High / Critical", f"{critical_high}/20", f"{avg_conf:.1f}% AI confidence")

# ----------------------------
# Command center row
# ----------------------------
st.markdown(
    '<div class="section-head"><div><h3>🛰️ Outbreak command center</h3>'
    '<p>एक नज़र में भौगोलिक फैलाव + current hotspots</p></div></div>',
    unsafe_allow_html=True,
)

map_col, hot_col = st.columns([1.62, 1], gap="medium")

with map_col:
    with st.container(border=True):
        st.markdown("**महाराष्ट्र outbreak footprint**")
        st.caption("Demo points — marker size visually reflects affected area.")
        map_df = df[["Lat", "Lon", "Affected_Ha"]].rename(
            columns={"Lat": "lat", "Lon": "lon", "Affected_Ha": "size"}
        )
        # Native Streamlit map
        st.map(map_df, latitude="lat", longitude="lon", size="size", height=410)
        st.caption(
            f"{len(df)} monitored locations • {affected_total:,} ha shown affected • "
            f"highest-risk point: {df.loc[df['Risk'].idxmax(), 'Marathi']} ({int(df['Risk'].max())}/100)"
        )

with hot_col:
    with st.container(border=True):
        st.markdown("**🔥 Top outbreak hotspots**")
        st.caption("Sorted by risk + affected footprint")

        top = df.sort_values(["Risk", "Affected_Ha"], ascending=False).head(7)
        for _, row in top.iterrows():
            cls = {
                "Critical": "pill-critical",
                "High": "pill-high",
                "Medium": "pill-medium",
            }[row["Severity"]]
            st.markdown(
                f"""
                <div class="hotspot-item">
                    <div style="display:flex;justify-content:space-between;gap:10px">
                        <div>
                            <div class="hotspot-name">{row["Marathi"]} · {row["City"]}</div>
                            <div class="hotspot-meta">
                                {int(row["Affected_Ha"])} ha • risk {int(row["Risk"])}
                                • +{row["Change_Pct"]:.1f}% YoY
                            </div>
                        </div>
                        <div class="severity-pill {cls}">{row["Severity"]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------------------
# Trend + comparative charts
# ----------------------------
st.markdown(
    '<div class="section-head"><div><h3>📈 Outbreak growth & comparisons</h3>'
    '<p>Native Streamlit charts — built for a dashboard, not a pasted report</p></div></div>',
    unsafe_allow_html=True,
)

trend_col, split_col = st.columns([1.25, 1], gap="medium")

with trend_col:
    with st.container(border=True):
        st.markdown("**2022 → 2026 affected area + hotspot count**")
        trend = history.set_index("Year")[["Affected_Ha", "Reported_Hotspots"]]
        st.line_chart(trend, height=320, use_container_width=True)
        st.caption(
            f"Demo trend: affected area moved from {int(history.iloc[0]['Affected_Ha'])} ha "
            f"to {int(history.iloc[-1]['Affected_Ha'])} ha."
        )

with split_col:
    with st.container(border=True):
        st.markdown("**2025 vs 2026 — affected hectares**")
        yoy = (
            df.sort_values("Affected_Ha", ascending=False)
            .head(10)[["Marathi", "Affected_2025", "Affected_Ha"]]
            .rename(columns={"Marathi": "क्षेत्र", "Affected_2025": "2025", "Affected_Ha": "2026"})
            .set_index("क्षेत्र")
        )
        st.bar_chart(yoy, height=320, use_container_width=True)
        st.caption("Top 10 locations by current affected footprint.")

# Three compact analytical cards
a, b, c = st.columns(3, gap="medium")

with a:
    with st.container(border=True):
        st.markdown("**⚠️ Severity distribution**")
        severity_counts = (
            df["Severity"].value_counts()
            .reindex(["Critical", "High", "Medium"], fill_value=0)
            .rename_axis("स्थिति")
            .to_frame("Locations")
        )
        st.bar_chart(severity_counts, height=220, use_container_width=True)
        st.caption("20 monitored locations.")

with b:
    with st.container(border=True):
        st.markdown("**🌱 Risk by crop stage**")
        stage = (
            df.groupby("Crop_Stage")["Risk"]
            .mean()
            .sort_values(ascending=False)
            .round(1)
            .to_frame("Avg Risk")
        )
        st.bar_chart(stage, height=220, use_container_width=True)
        st.caption("Sample average risk across crop stages.")

with c:
    with st.container(border=True):
        st.markdown("**💧 Humidity vs risk**")
        scatter = df[["City", "Humidity", "Risk"]].copy()
        scatter["Risk score"] = scatter["Risk"]
        st.scatter_chart(
            scatter,
            x="Humidity",
            y="Risk score",
            size="Risk score",
            height=220,
            use_container_width=True,
        )
        st.caption("Visual relationship only — not a scientific model.")

# ----------------------------
# Quick insight strip
# ----------------------------
st.markdown(
    '<div class="section-head"><div><h3>🧠 What the demo is signalling</h3>'
    '<p>Three concise takeaways for a presentation/showcase screen</p></div></div>',
    unsafe_allow_html=True,
)

q1, q2, q3 = st.columns(3, gap="medium")
with q1:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="label">LARGEST CURRENT FOOTPRINT</div>
            <div class="value">{df.loc[df["Affected_Ha"].idxmax(), "Marathi"]}</div>
            <div class="label">{int(df["Affected_Ha"].max())} ha affected</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with q2:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="label">HIGHEST DEMO RISK</div>
            <div class="value">{df.loc[df["Risk"].idxmax(), "Marathi"]}</div>
            <div class="label">{int(df["Risk"].max())}/100 outbreak score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with q3:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="label">YEAR-ON-YEAR SIGNAL</div>
            <div class="value">+{yoy_total:.1f}%</div>
            <div class="label">sample affected-area growth</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="callout" style="margin-top:.8rem">
        <b>Early-warning reading:</b> multiple sample locations are simultaneously showing
        high risk, meaningful affected area and elevated spread signals. In a real deployment,
        this layer would feed field scouting, trap monitoring and expert-reviewed control actions.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Detailed location analytics
# ----------------------------
st.markdown(
    '<div class="section-head"><div><h3>🧭 Location-by-location intelligence</h3>'
    '<p>Every sample location retained — nothing hidden in blank placeholders</p></div></div>',
    unsafe_allow_html=True,
)

detail_left, detail_right = st.columns([1.4, 1], gap="medium")

with detail_left:
    with st.container(border=True):
        st.markdown("**20-location outbreak matrix**")
        st.caption("Risk is displayed as a native progress column for faster scanning.")
        display_df = df[
            [
                "Marathi", "City", "Pest_Hindi", "Affected_Ha", "Infestation_Pct",
                "Risk", "Severity", "Confidence", "Spread_Rate", "Humidity", "Crop_Stage", "Action"
            ]
        ].copy()
        display_df.columns = [
            "क्षेत्र", "City", "कीट", "प्रभावित ha", "संक्रमण %",
            "जोखिम", "गंभीरता", "AI confidence", "फैलाव संकेत", "नमी %",
            "फसल अवस्था", "कार्रवाई"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=520,
            column_config={
                "प्रभावित ha": st.column_config.NumberColumn(format="%.0f"),
                "संक्रमण %": st.column_config.NumberColumn(format="%.1f%%"),
                "AI confidence": st.column_config.NumberColumn(format="%.0f%%"),
                "नमी %": st.column_config.NumberColumn(format="%.0f%%"),
                "जोखिम": st.column_config.ProgressColumn(
                    min_value=0, max_value=100, format="%d"
                ),
            },
        )

with detail_right:
    with st.container(border=True):
        st.markdown("**🐛 Pest profile**")
        st.markdown(
            f"""
            <div style="font-size:1.55rem;font-weight:850;color:#17352a">Yellow Rice Borer</div>
            <div style="font-size:.82rem;color:#738079;margin:.2rem 0 .8rem">पीला तना छेदक</div>
            """,
            unsafe_allow_html=True,
        )
        p1, p2 = st.columns(2, gap="small")
        with p1:
            st.markdown(
                f'<div class="mini-stat"><div class="label">AVG AI CONFIDENCE</div>'
                f'<div class="value">{avg_conf:.1f}%</div></div>',
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                f'<div class="mini-stat"><div class="label">AVG SPREAD SIGNAL</div>'
                f'<div class="value">{df["Spread_Rate"].mean():.1f}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="callout" style="margin-top:.8rem">
                <b>Typical field clues:</b> stem/central shoot injury, dead-heart or
                white-ear symptoms, and patch-wise damage patterns.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**🛡️ Demo response workflow**")
        st.write("1. प्रभावित patch में intensive field scouting")
        st.write("2. Trap + symptom monitoring बढ़ाना")
        st.write("3. Nearby fields में containment re-check")
        st.write("4. Local expert के अनुसार label-approved control")

# ----------------------------
# Bottom yearly comparison
# ----------------------------
st.markdown(
    '<div class="section-head"><div><h3>↗️ पिछले वर्ष का बदलाव</h3>'
    '<p>किस sample location में footprint सबसे ज्यादा बढ़ा हुआ दिखता है</p></div></div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    compare = (
        df[["Marathi", "Affected_2025", "Affected_Ha", "Change_Pct", "Severity"]]
        .sort_values("Change_Pct", ascending=False)
        .copy()
    )
    compare.columns = ["क्षेत्र", "2025 ha", "2026 ha", "बदलाव %", "स्थिति"]
    st.dataframe(
        compare,
        use_container_width=True,
        hide_index=True,
        column_config={
            "2025 ha": st.column_config.NumberColumn(format="%.0f"),
            "2026 ha": st.column_config.NumberColumn(format="%.0f"),
            "बदलाव %": st.column_config.NumberColumn(format="%.1f%%"),
        },
        height=420,
    )