import os
import io
import re
import tempfile
import traceback
from urllib.parse import urlparse
import requests
import streamlit as st
from PIL import Image
from MAIN import call_models
from status import update_status, get_status
import threading
import time

st.set_page_config(
    page_title="Prakriti AI | स्मार्ट फसल सहायक",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --prakriti-green: #16794f;
            --prakriti-green-dark: #0f5c3a;
            --prakriti-green-light: #e8f5ef;
            --prakriti-bg: #f4f9f6;
        }

        .stApp {
            background-color: var(--prakriti-bg);
        }

        #MainMenu, footer {visibility: hidden;}
        header, [data-testid="stHeader"] {
            display: none;
        }

        .block-container {
            padding-top: 1.5rem;
            max-width: 1200px;
        }

        /* Top header bar */
        .prakriti-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ffffff;
            padding: 14px 26px;
            border-radius: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 22px;
        }
        .prakriti-logo {
            font-size: 20px;
            font-weight: 800;
            color: #17301f;
        }
        .prakriti-tagline {
            font-size: 12px;
            color: #6b7a70;
            margin-top: -2px;
        }

        .prakriti-badge {
            display: inline-block;
            background: var(--prakriti-green-light);
            color: var(--prakriti-green-dark);
            font-weight: 600;
            font-size: 13px;
            padding: 6px 14px;
            border-radius: 20px;
            margin-bottom: 14px;
        }

        h1.prakriti-title {
            font-size: 40px;
            font-weight: 800;
            color: #16211b;
            line-height: 1.15;
            margin-bottom: 0;
        }
        .prakriti-title-green {
            color: var(--prakriti-green);
        }

        .prakriti-subtext {
            color: #55635a;
            font-size: 15.5px;
            max-width: 780px;
            margin-top: 10px;
            margin-bottom: 24px;
        }

        /* Cards */
        .prakriti-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px 26px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            margin-bottom: 18px;
        }
        .prakriti-card h3 {
            margin-bottom: 2px;
            color: #16211b;
        }
        .prakriti-card-sub {
            color: #7d8b81;
            font-size: 13.5px;
            margin-bottom: 18px;
        }

        .prakriti-tip-card {
            background: var(--prakriti-green-light);
            border-radius: 16px;
            padding: 18px 20px;
            font-size: 13.5px;
            color: #234a35;
            margin-bottom: 18px;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background: var(--prakriti-green-light);
            border: 2px dashed #8fcbab;
            border-radius: 14px;
        }

        .stButton>button {
            background: var(--prakriti-green);
            color: white;
            font-weight: 700;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background: var(--prakriti-green-dark);
            color: white;
        }

        .result-metric {
            background: var(--prakriti-green-light);
            border-radius: 12px;
            padding: 14px 16px;
            text-align: center;
        }
        .result-metric .label {
            font-size: 12.5px;
            color: #4b6156;
        }
        .result-metric .value {
            font-size: 20px;
            font-weight: 800;
            color: var(--prakriti-green-dark);
        }

        .field-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 14px;
            padding: 10px 4px;
            border-bottom: 1px solid #eef3ef;
        }
        .field-row:last-child { border-bottom: none; }
        .field-row .field-label {
            color: #4b6156;
            font-size: 13.5px;
            font-weight: 600;
            white-space: nowrap;
        }
        .field-row .field-value {
            color: #16211b;
            font-size: 14px;
            text-align: right;
        }

        .field-group-title {
            font-weight: 700;
            font-size: 14.5px;
            color: var(--prakriti-green-dark);
            margin-top: 14px;
            margin-bottom: 2px;
        }

        .field-card {
            background: var(--prakriti-green-light);
            border-radius: 12px;
            padding: 4px 14px;
            margin-bottom: 10px;
        }

        /* Top navigation menu */
        .prakriti-topnav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ffffff;
            padding: 12px 26px;
            border-radius: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .prakriti-topnav-logo {
            font-size: 17px;
            font-weight: 800;
            color: #17301f;
            white-space: nowrap;
        }
        .prakriti-topnav-right {
            display: flex;
            align-items: center;
            gap: 22px;
            flex-wrap: wrap;
        }
        .prakriti-nav-links {
            display: flex;
            align-items: center;
            gap: 22px;
            flex-wrap: wrap;
        }
        .stMarkdown .prakriti-nav-link,
        .stMarkdown .prakriti-nav-link:link,
        .stMarkdown .prakriti-nav-link:visited,
        .stMarkdown .prakriti-nav-link:hover,
        .stMarkdown .prakriti-nav-link:active,
        .stMarkdown .prakriti-nav-link:focus {
            text-decoration: none !important;
        }
        .prakriti-nav-link:hover {
            color: var(--prakriti-green);
        }
        .prakriti-nav-divider {
            width: 1px;
            height: 20px;
            background: #e0e8e3;
        }

        /* Translator toggle - prototype only, non-functional */
        .prakriti-translate {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            cursor: pointer;
            user-select: none;
        }
        .prakriti-translate input {
            display: none;
        }
        .prakriti-translate-slider {
            position: relative;
            width: 38px;
            height: 21px;
            background: #dbe7e0;
            border-radius: 20px;
            transition: background 0.2s ease;
            flex-shrink: 0;
        }
        .prakriti-translate-slider::before {
            content: "";
            position: absolute;
            top: 2px;
            left: 2px;
            width: 17px;
            height: 17px;
            background: #ffffff;
            border-radius: 50%;
            transition: transform 0.2s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        }
        .prakriti-translate input:checked + .prakriti-translate-slider {
            background: var(--prakriti-green);
        }
        .prakriti-translate input:checked + .prakriti-translate-slider::before {
            transform: translateX(17px);
        }
        .prakriti-translate-label {
            font-size: 12.5px;
            font-weight: 600;
            color: #4b6156;
            white-space: nowrap;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# TOP NAVIGATION MENU
# Add / remove / edit menu buttons here - each item needs a label and the
# URL it should open when clicked. This is the only place you need to
# touch to change what shows up in the top menu.
# --------------------------------------------------------------------------
NAV_MENU_ITEMS = [
    {"label": "Home", "url": "#"},
    {"label": "GeoSpatial", "url": "#"},
    {"label": "Risk Analyzer", "url": "#"},
    {"label": "VH Predictor", "url": "#"},
    {"label": "3D Reconstructor", "url": "#"},
    {"label": "About Us", "url": "#"},
]

_nav_links_html = "".join(
    f'<a class="prakriti-nav-link" href="{item["url"]}">{item["label"]}</a>'
    for item in NAV_MENU_ITEMS
)

st.markdown(
    f"""
    <div class="prakriti-topnav">
        <div class="prakriti-topnav-logo">🌿 Prakriti AI</div>
        <div class="prakriti-topnav-right">
            <div class="prakriti-nav-links">
                {_nav_links_html}
            </div>
            <div class="prakriti-nav-divider"></div>
            <label class="prakriti-translate" title="भाषा अनुवाद (प्रोटोटाइप - अभी निष्क्रिय)">
                <input type="checkbox">
                <span class="prakriti-translate-slider"></span>
                <span class="prakriti-translate-label">🌐 Translate</span>
            </label>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "result_kb" not in st.session_state:
    st.session_state.result_kb = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None

st.markdown('<span class="prakriti-badge">🟢 AI-संचालित फसल निदान</span>'
    '<h1 class="prakriti-title">फसल की समस्याएं पहचानें<br>'
    '<span class="prakriti-title-green">फैलने से पहले।</span></h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="prakriti-subtext">फसल की पत्ती की एक स्पष्ट फोटो अपलोड करें और Prakriti AI एक '
    'बुद्धिमान रोग जांच, गंभीरता मूल्यांकन और व्यावहारिक उपचार योजना तैयार करेगा।</div>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("### 🌾 फसल रोग / कीट की रिपोर्ट करें")
    st.markdown(
        '<div class="prakriti-card-sub">निदान और सुझाव पाने के लिए नीचे विवरण भरें</div>',
        unsafe_allow_html=True,
    )

    with st.form("prakriti_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            disease_or_pest = st.selectbox(
                "समस्या का प्रकार चुनें *",
                options=["disease", "pest"],
                format_func=lambda x: "रोग (Disease)" if x == "disease" else "कीट (Pest)",
            )
        with c2:
            soil_type = st.selectbox(
                "मिट्टी का प्रकार चुनें *",
                options=["clayey", "loamy", "black", "red"],
                format_func=lambda x: x.capitalize(),
            )

        disease_category = None
        if disease_or_pest == "disease":
            disease_category = st.selectbox(
                "फसल श्रेणी चुनें (Disease Category) *",
                options=["Rice", "Wheat", "Other"],
            )

        address = st.text_area(
            "पता (Address) *",
            placeholder="जैसे: Bhopal, Madhya Pradesh, India",
            height=90,
        )

        st.markdown("**फसल की छवि अपलोड करें ***")
        tab_upload, tab_url = st.tabs(["📁 फाइल अपलोड करें", "🔗 इमेज URL से लें"])

        with tab_upload:
            uploaded_file = st.file_uploader(
                "यहाँ फसल की छवि छोड़ें",
                type=["png", "jpg", "jpeg", "webp"],
                help="JPG, PNG या WEBP - अनुशंसित 10 MB से कम",
                label_visibility="collapsed",
            )

        with tab_url:
            image_url = st.text_input(
                "इमेज URL यहाँ पेस्ट करें",
                placeholder="https://example.com/leaf.jpg",
                label_visibility="collapsed",
            )

        submitted = st.form_submit_button("🔍 परिणाम प्राप्त करें (Get Result)")

with right_col:
    st.markdown(
        """
        <div class="prakriti-tip-card">
            💡 <b>बेहतर फोटो से बेहतर निदान होता है</b><br><br>
            प्रभावित पत्ती की अच्छी प्राकृतिक रोशनी में तस्वीर लें। बेहतर AI विश्लेषण के लिए
            पत्ती को केंद्र में रखें और धुंधली तस्वीरों से बचें।
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="prakriti-card">
            <b>🛰️ यह कैसे काम करता है</b>
            <ol style="padding-left:18px; font-size:13.5px; color:#4b6156;">
                <li>फसल की स्पष्ट छवि अपलोड करें</li>
                <li>पता, मिट्टी व श्रेणी की जानकारी भरें</li>
                <li>AI मौसम, मिट्टी व छवि का विश्लेषण करेगा</li>
                <li>निदान, जोखिम स्कोर व उर्वरक सुझाव पाएं</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------
def _download_image_from_url(url: str) -> bytes:
    """Download an image from a URL and return raw bytes. Raises on failure."""
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        raise ValueError("कृपया एक मान्य (valid) http/https URL दर्ज करें।")

    resp = requests.get(url, timeout=20, stream=True)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "")
    data = resp.content

    if content_type and "image" not in content_type:
        # Fall back to trying to open it as an image anyway; some servers
        # send wrong content-types for images.
        try:
            Image.open(io.BytesIO(data)).verify()
        except Exception:
            raise ValueError(
                f"दिया गया URL एक इमेज फाइल नहीं लगता (Content-Type: {content_type or 'unknown'})।"
            )
    else:
        # Validate it's actually a readable image
        Image.open(io.BytesIO(data)).verify()

    return data


def _save_bytes_to_tempfile(image_bytes: bytes, suffix: str = ".jpg") -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(image_bytes)
    tmp.flush()
    tmp.close()
    return tmp.name


_IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


def _resolve_image_path(path):
    """
    The detection pipeline's 'saved_path' can be either a direct image file
    or a directory (e.g. YOLO's 'runs/detect/predict-3' output folder).
    Resolve it down to an actual, most-recently-modified image file.
    Returns None if no usable image can be found.
    """
    if not path:
        return None

    if os.path.isfile(path):
        return path

    if os.path.isdir(path):
        candidates = []
        for entry in os.listdir(path):
            full = os.path.join(path, entry)
            if os.path.isfile(full) and entry.lower().endswith(_IMAGE_EXTS):
                candidates.append(full)
        if candidates:
            # Most recently written image in that folder (the annotated result)
            return max(candidates, key=os.path.getmtime)

    return None


def _humanize_label(key) -> str:
    """Turn a raw dict key like 'soil_ph_level' or 'soilPhLevel' into 'Soil Ph Level'."""
    text = str(key)
    text = re.sub(r"[_\-]+", " ", text)  # snake/kebab -> spaces
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)  # camelCase -> spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text.title()


def _format_scalar(value) -> str:
    if value is None or value == "":
        return "N/A"
    if isinstance(value, bool):
        return "हाँ" if value else "नहीं"
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".") if value % 1 else f"{int(value)}"
    return str(value)


def _render_fields(data, heading: str = None):
    if data is None:
        return

    if heading:
        st.markdown(f'<div class="field-group-title">{heading}</div>', unsafe_allow_html=True)

    if isinstance(data, dict):
        if not data:
            st.caption("कोई जानकारी उपलब्ध नहीं है।")
            return

        scalar_items = {k: v for k, v in data.items() if not isinstance(v, (dict, list))}
        nested_items = {k: v for k, v in data.items() if isinstance(v, (dict, list))}

        if scalar_items:
            rows = "".join(
                f'<div class="field-row"><div class="field-label">{_humanize_label(k)}</div>'
                f'<div class="field-value">{_format_scalar(v)}</div></div>'
                for k, v in scalar_items.items()
            )
            st.markdown(f'<div class="field-card">{rows}</div>', unsafe_allow_html=True)

        for k, v in nested_items.items():
            _render_fields(v, heading=_humanize_label(k))

    elif isinstance(data, list):
        if not data:
            st.caption("कोई जानकारी उपलब्ध नहीं है।")
            return

        if all(isinstance(item, (dict, list)) for item in data):
            for i, item in enumerate(data, start=1):
                _render_fields(item, heading=f"#{i}")
        else:
            bullets = "".join(f"- {_format_scalar(item)}\n" for item in data)
            st.markdown(bullets)

    else:
        st.markdown(_format_scalar(data))


def _render_result(kb: dict):
    st.markdown("---")
    st.markdown("## ✅ विश्लेषण परिणाम (Analysis Result)")

    dtype = (kb.get("Disease/Pest Type") or "").lower()
    is_disease = "disease" in dtype

    img_col, meta_col = st.columns([1, 1.3], gap="large")

    with img_col:
        ann_path_raw = kb.get("Disease Annotation Path") if is_disease else kb.get("Pest Annotation Path")
        ann_path = _resolve_image_path(ann_path_raw)
        if ann_path:
            st.image(ann_path, caption="एनोटेटेड परिणाम (Annotated Image)", use_container_width=True)
        elif st.session_state.image_bytes:
            st.image(st.session_state.image_bytes, caption="अपलोड की गई छवि", use_container_width=True)
        else:
            st.info("कोई एनोटेटेड छवि उपलब्ध नहीं है।")

    with meta_col:
        name = kb.get("Disease Name") if is_disease else kb.get("Pest Name")
        conf = kb.get("Disease Confidence") if is_disease else kb.get("Pest Confidence")

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(
                f'<div class="result-metric"><div class="label">{"रोग" if is_disease else "कीट"}</div>'
                f'<div class="value" style="font-size:16px;">{name or "N/A"}</div></div>',
                unsafe_allow_html=True,
            )
        with mc2:
            conf_display = f"{conf*100:.1f}%" if isinstance(conf, (int, float)) and conf <= 1 else (
                f"{conf:.1f}%" if isinstance(conf, (int, float)) else "N/A"
            )
            st.markdown(
                f'<div class="result-metric"><div class="label">विश्वास (Confidence)</div>'
                f'<div class="value">{conf_display}</div></div>',
                unsafe_allow_html=True,
            )
        with mc3:
            risk = kb.get("Risk Score")
            st.markdown(
                f'<div class="result-metric"><div class="label">जोखिम स्कोर (Risk Score)</div>'
                f'<div class="value">{risk if risk is not None else "N/A"}</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown("**🌦️ मौसम व मिट्टी की जानकारी**")
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("तापमान", f"{kb.get('Temperature', 'N/A')}")
        w2.metric("आर्द्रता", f"{kb.get('Humidity', 'N/A')}")
        w3.metric("मिट्टी की नमी", f"{kb.get('Soil Moisture', 'N/A')}")
        w4.metric("वर्षा", f"{kb.get('Rainfall', 'N/A')}")

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("N", f"{kb.get('Soil Nitrogen Level', 'N/A')}")
        s2.metric("P", f"{kb.get('Soil Phosphorus Level', 'N/A')}")
        s3.metric("K", f"{kb.get('Soil Potassium Level', 'N/A')}")
        s4.metric("pH", f"{kb.get('Soil pH Level', 'N/A')}")

        if not is_disease and kb.get("Pest Information"):
            with st.expander("🐛 कीट संबंधी अतिरिक्त जानकारी (Pest Information)", expanded=False):
                _render_fields(kb["Pest Information"])

    st.markdown("### 🌱 उर्वरक सुझाव (Fertilizer Recommendation)")
    fert = kb.get("Fertilizer Recommendation")
    if isinstance(fert, (dict, list)):
        _render_fields(fert)
    elif fert:
        st.markdown(str(fert))
    else:
        st.info("कोई उर्वरक सुझाव उपलब्ध नहीं है।")

    st.markdown("### 📋 विस्तृत व्याख्या (Explanation)")
    explanation = kb.get("Explanation")
    if explanation:
        st.markdown(explanation)
    else:
        st.info("कोई व्याख्या उपलब्ध नहीं है।")

    with st.expander("🔎 पूरा तकनीकी डेटा देखें (Raw Knowledge Base)"):
        st.json(kb)


# --------------------------------------------------------------------------
# FORM SUBMISSION HANDLING
# --------------------------------------------------------------------------
if submitted:
    st.session_state.result_kb = None
    st.session_state.error_msg = None

    # ---- Validation ----
    errors = []
    if not address or not address.strip():
        errors.append("कृपया पता (Address) दर्ज करें।")

    if disease_or_pest == "disease" and not disease_category:
        errors.append("कृपया फसल श्रेणी (Disease Category) चुनें।")

    has_upload = uploaded_file is not None
    has_url = bool(image_url and image_url.strip())

    if not has_upload and not has_url:
        errors.append("कृपया एक छवि अपलोड करें या इमेज URL प्रदान करें।")
    if has_upload and has_url:
        errors.append("कृपया या तो फाइल अपलोड करें या URL दें — दोनों एक साथ नहीं।")

    if errors:
        for e in errors:
            st.error(e)
    else:
        temp_file_path = None

        try:
            # ============================================================
            # 1. PREPARE IMAGE
            # ============================================================
            update_status(
                "running",
                "Preparing Image",
                "छवि तैयार की जा रही है..."
            )

            if has_upload:
                image_bytes = uploaded_file.getvalue()
                suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"

            else:
                image_bytes = _download_image_from_url(image_url.strip())

                guessed_ext = os.path.splitext(
                    urlparse(image_url.strip()).path
                )[1]

                suffix = (
                    guessed_ext
                    if guessed_ext.lower() in [
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".webp"
                    ]
                    else ".jpg"
                )

            st.session_state.image_bytes = image_bytes

            temp_file_path = _save_bytes_to_tempfile(
                image_bytes,
                suffix=suffix
            )

            update_status(
                "running",
                "Image Ready",
                "छवि तैयार हो गई। AI विश्लेषण शुरू किया जा रहा है..."
            )

            # ============================================================
            # 2. RUN AI ANALYSIS IN BACKGROUND THREAD
            # ============================================================
            result_container = {}
            error_container = {}


            def run_analysis():
                try:
                    result_container["kb"] = call_models(
                        disease_or_pest=disease_or_pest,
                        address=address.strip(),
                        soil_type=soil_type,
                        filepath=temp_file_path,
                        disease_category=disease_category,
                    )

                except Exception as e:
                    error_container["error"] = e


            analysis_thread = threading.Thread(
                target=run_analysis,
                daemon=True
            )

            analysis_thread.start()

            # ============================================================
            # 3. SHOW LIVE STATUS
            # ============================================================
            status_box = st.status(
                "AI विश्लेषण चल रहा है...",
                expanded=True
            )

            status_message = status_box.empty()

            while analysis_thread.is_alive():
                current = get_status()

                step = current.get(
                    "step",
                    "processing"
                )

                message = current.get(
                    "message",
                    "AI विश्लेषण चल रहा है..."
                )

                status_message.markdown(
                    f"""
                        **चरण:** {step}

                        {message}
                        """
                )

                time.sleep(0.5)

            # ============================================================
            # 4. ANALYSIS FINISHED
            # ============================================================
            if "error" in error_container:
                status_box.update(
                    label="विश्लेषण में त्रुटि हुई ❌",
                    state="error"
                )

                raise error_container["error"]

            kb = result_container.get("kb")

            st.session_state.result_kb = kb

            # Make absolutely sure final status is completed
            update_status(
                "completed",
                "Done",
                "विश्लेषण सफलतापूर्वक पूर्ण हुआ ✅"
            )

            status_message.markdown(
                """
                **चरण:** Done

                विश्लेषण सफलतापूर्वक पूर्ण हुआ ✅
                """
            )

            status_box.update(
                label="विश्लेषण पूर्ण हुआ ✅",
                state="complete"
            )

            st.success("विश्लेषण सफलतापूर्वक पूर्ण हुआ ✅")

        except requests.exceptions.RequestException as e:
            update_status(
                "error",
                "download_failed",
                f"इमेज URL से डाउनलोड करने में विफल: {e}"
            )

            st.session_state.error_msg = (
                f"इमेज URL से डाउनलोड करने में विफल: {e}"
            )

        except ValueError as e:
            update_status(
                "error",
                "validation_failed",
                str(e)
            )

            st.session_state.error_msg = str(e)

        except RuntimeError as e:
            update_status(
                "error",
                "model_error",
                f"मॉडल त्रुटि: {e}"
            )

            st.session_state.error_msg = f"मॉडल त्रुटि: {e}"

        except Exception as e:
            update_status(
                "error",
                "failed",
                f"अप्रत्याशित त्रुटि हुई: {e}"
            )

            st.session_state.error_msg = (
                f"अप्रत्याशित त्रुटि हुई: {e}"
            )

            st.session_state.error_trace = traceback.format_exc()

        finally:
            if (
                    temp_file_path
                    and os.path.exists(temp_file_path)
                    and st.session_state.result_kb is None
            ):
                try:
                    os.remove(temp_file_path)
                except OSError:
                    pass
if st.session_state.error_msg:
    st.error(f"⚠️ {st.session_state.error_msg}")
    if "error_trace" in st.session_state:
        with st.expander("तकनीकी विवरण (Technical Details)"):
            st.code(st.session_state.error_trace)

if st.session_state.result_kb:
    _render_result(st.session_state.result_kb)