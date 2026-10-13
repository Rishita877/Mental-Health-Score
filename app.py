import requests
import streamlit as st

# ──────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Wellbeing Predictor",
    page_icon="🧠",
    layout="centered",
)

DEFAULT_API_URL = " https://mental-health-score-yv6d.onrender.com"

COUNTRIES = [
    "India", "USA", "Canada", "Australia", "UK", "Germany", "Mexico",
    "Turkey", "France", "Brazil", "China", "Japan", "South Korea",
    "Spain", "Italy", "Netherlands", "Sweden", "Norway", "Denmark",
    "Switzerland", "Ireland", "Pakistan", "Bangladesh", "Nepal",
    "Sri Lanka", "Indonesia", "Malaysia", "Singapore", "Thailand",
    "Vietnam", "Philippines", "UAE", "Saudi Arabia", "Egypt", "Nigeria",
    "Kenya", "South Africa", "Argentina", "Chile", "Colombia", "Russia",
    "Poland", "Ukraine", "Greece", "Portugal", "Other",
]

PLATFORMS = [
    "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter", "YouTube",
    "TikTok", "LINE", "KakaoTalk", "VKontakte", "WhatsApp", "WeChat",
]

# ──────────────────────────────────────────────────────────────
# Styling
# ──────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=DM+Sans:wght@400;500;600&display=swap');

:root {
  --ink: #1d2340;
  --muted: #5d6585;
  --paper: #eef1f9;
  --card: #ffffff;
  --line: #d9deef;
  --brand: #3b4cca;
  --good: #1f9d8a;
  --mid: #d99a1c;
  --low: #d6534a;
}

html, body, [class*="css"], .stApp {
  font-family: 'DM Sans', system-ui, sans-serif;
  color: var(--ink);
}
.stApp { background: var(--paper); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 820px; padding-top: 2.2rem; padding-bottom: 4rem; }

/* Hero */
.hero { padding: 0rem 0 1.6rem 0; }
.hero h1 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 700;
  font-size: clamp(2rem, 5vw, 3rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 0 0 0.6rem 0;
  color: var(--ink);
}
.hero p {
  color: var(--muted);
  font-size: 1.05rem;
  max-width: 56ch;
  margin: 0;
  line-height: 1.55;
}

/* Form panel */
div[data-testid="stForm"] {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.6rem 1.6rem 1.2rem 1.6rem;
  box-shadow: 0 10px 30px -18px rgba(29, 35, 64, 0.35);
}
.group-title {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 1.15rem;
  margin: 0.4rem 0 0.2rem 0;
  color: var(--ink);
}
.group-sub { color: var(--muted); font-size: 0.9rem; margin: 0 0 0.8rem 0; }
.group-gap { height: 0.9rem; }

label, .stSelectbox label, .stNumberInput label, .stSlider label {
  color: var(--ink) !important;
  font-weight: 500 !important;
}

/* Submit button */
div[data-testid="stFormSubmitButton"] button {
  width: 100%;
  background: var(--brand);
  color: #fff;
  border: none;
  border-radius: 14px;
  padding: 0.85rem 1rem;
  font-weight: 600;
  font-size: 1.02rem;
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}
div[data-testid="stFormSubmitButton"] button:hover {
  background: #2f3eb0;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 10px 22px -10px rgba(59, 76, 202, 0.7);
}
div[data-testid="stFormSubmitButton"] button:focus-visible {
  outline: 3px solid rgba(59, 76, 202, 0.45);
  outline-offset: 2px;
}

/* Loader */
.loader-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 2.4rem 1rem;
  text-align: center;
  margin-top: 1.4rem;
}
.ring-spin {
  width: 56px; height: 56px;
  margin: 0 auto 1.1rem auto;
  border-radius: 50%;
  border: 5px solid var(--line);
  border-top-color: var(--brand);
  animation: spin 0.9s linear infinite;
}
.dots span {
  display: inline-block;
  width: 8px; height: 8px;
  margin: 0 3px;
  border-radius: 50%;
  background: var(--brand);
  animation: bounce 1.2s ease-in-out infinite;
}
.dots span:nth-child(2) { animation-delay: .15s; }
.dots span:nth-child(3) { animation-delay: .30s; }
.loader-card p { margin: 0.7rem 0 0 0; color: var(--muted); }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: .35; }
  40% { transform: translateY(-8px); opacity: 1; }
}

/* Result card */
.result-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 2rem 1.6rem;
  margin-top: 1.4rem;
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  box-shadow: 0 18px 40px -22px rgba(29, 35, 64, 0.45);
}
.gauge { position: relative; width: 190px; height: 190px; flex: 0 0 auto; }
.gauge svg { transform: rotate(-90deg); }
.gauge .track { stroke: var(--line); }
.gauge .bar {
  stroke-linecap: round;
  animation: fill 1.3s cubic-bezier(.22,.8,.3,1) both;
}
@keyframes fill { from { stroke-dashoffset: 339.292; } }
.gauge .value {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.gauge .num {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.8rem; font-weight: 700; line-height: 1;
}
.gauge .of { color: var(--muted); font-size: 0.85rem; margin-top: 0.25rem; }
.result-text { flex: 1 1 260px; min-width: 240px; }
.result-text h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.6rem; margin: 0 0 0.5rem 0; line-height: 1.2;
}
.result-text p { color: var(--muted); line-height: 1.6; margin: 0 0 0.9rem 0; }
.badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  font-size: 0.85rem; font-weight: 600;
  margin-bottom: 0.8rem;
}
.note { color: var(--muted); font-size: 0.82rem; margin-top: 1rem; }

/* Error */
.err-card {
  background: #fff5f4;
  border: 1px solid #f0c4c0;
  color: #8c2f28;
  border-radius: 16px;
  padding: 1rem 1.2rem;
  margin-top: 1.4rem;
}
.err-card b { display: block; margin-bottom: 0.2rem; }

/* Mobile */
@media (max-width: 640px) {
  .block-container { padding-left: 1rem; padding-right: 1rem; }
  div[data-testid="stForm"] { padding: 1.1rem; }
  .result-card { padding: 1.4rem 1rem; }
}
@media (prefers-reduced-motion: reduce) {
  .ring-spin, .dots span, .gauge .bar { animation: none; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Sidebar — API connection
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Connection")
    api_url = st.text_input("Backend URL", value=DEFAULT_API_URL).rstrip("/")
    st.caption("Start the backend first: `uvicorn main:app --reload`")

# ──────────────────────────────────────────────────────────────
# Hero
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <h1>How is your digital life affecting your wellbeing?</h1>
      <p>Tell us about your daily routine and social media habits. Our model
      estimates a mental health score from patterns seen in thousands of
      student responses.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# Form — every field in StudentData
# ──────────────────────────────────────────────────────────────
with st.form("student_form"):
    st.markdown('<div class="group-title">About you</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-sub">Basic background details.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", min_value=10, max_value=100, value=20, step=1)
        country = st.selectbox("Country", COUNTRIES, index=0)
    with c2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        academic_level = st.selectbox(
            "Academic level", ["Undergraduate", "Graduate", "High School"]
        )

    st.markdown('<div class="group-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="group-title">Social media use</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-sub">How and how much you use it.</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        most_used_platform = st.selectbox("Most used platform", PLATFORMS, index=2)
        avg_daily_usage_hours = st.slider(
            "Average daily usage (hours)", 0.0, 24.0, 4.0, 0.5
        )
    with c4:
        purpose_of_use = st.selectbox(
            "Main purpose of use",
            ["Networking", "Education", "Entertainment", "News"],
            index=2,
        )
        daily_unlocks = st.number_input(
            "Phone unlocks per day", min_value=0, max_value=1000, value=50, step=5
        )

    st.markdown('<div class="group-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="group-title">Daily routine</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-sub">Study, movement, sleep and stress.</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        study_hours = st.slider("Study hours per day", 0.0, 24.0, 4.0, 0.5)
        sleep_hours_per_night = st.slider("Sleep hours per night", 0.0, 24.0, 7.0, 0.5)
    with c6:
        physical_activity_hours = st.slider(
            "Physical activity (hours per day)", 0.0, 24.0, 1.0, 0.5
        )
        stress_level = st.selectbox(
            "Stress level", ["Low", "Medium", "High", "Very High"], index=1
        )

    submitted = st.form_submit_button("Predict my score")

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def interpret(score: float):
    """Return (label, headline, message, colour var, badge background)."""
    if score >= 7.5:
        return (
            "Doing well",
            "Your habits point to good mental wellbeing.",
            "Your routine looks balanced. Keep protecting your sleep and "
            "your time away from screens.",
            "var(--good)", "#dff4f0",
        )
    if score >= 5.5:
        return (
            "Mixed signals",
            "Some habits may be putting pressure on your wellbeing.",
            "Small changes can help: a consistent sleep schedule, more "
            "movement, and shorter stretches on social media.",
            "var(--mid)", "#fbf0d6",
        )
    return (
        "Needs attention",
        "Your habits suggest your wellbeing could use more care.",
        "Consider cutting screen time before bed, adding regular activity, "
        "and talking with someone you trust or a counsellor.",
        "var(--low)", "#fbe3e1",
    )


def result_card(score: float, max_score: float = 10.0) -> str:
    label, headline, message, colour, badge_bg = interpret(score)
    circumference = 339.292  # 2 * pi * r with r = 54
    fraction = max(0.0, min(score / max_score, 1.0))
    offset = circumference * (1 - fraction)
    return f"""
    <div class="result-card">
      <div class="gauge" role="img" aria-label="Predicted score {score} out of {int(max_score)}">
        <svg width="190" height="190" viewBox="0 0 120 120">
          <circle class="track" cx="60" cy="60" r="54" fill="none" stroke-width="9"/>
          <circle class="bar" cx="60" cy="60" r="54" fill="none" stroke-width="9"
                  stroke="{colour}"
                  stroke-dasharray="{circumference}"
                  stroke-dashoffset="{offset}"/>
        </svg>
        <div class="value">
          <span class="num" style="color:{colour}">{score:.2f}</span>
          <span class="of">out of {int(max_score)}</span>
        </div>
      </div>
      <div class="result-text">
        <span class="badge" style="background:{badge_bg}; color:{colour}">{label}</span>
        <h2>{headline}</h2>
        <p>{message}</p>
        <div class="note">This is a statistical estimate, not a diagnosis or medical advice.
        If you are struggling, please reach out to a qualified professional.</div>
      </div>
    </div>
    """


LOADER_HTML = """
<div class="loader-card" role="status" aria-live="polite">
  <div class="ring-spin"></div>
  <div class="dots"><span></span><span></span><span></span></div>
  <p>Analysing your habits&hellip;</p>
</div>
"""


def error_card(title: str, detail: str) -> str:
    return f'<div class="err-card"><b>{title}</b>{detail}</div>'


# ──────────────────────────────────────────────────────────────
# Submit -> POST /predict
# ──────────────────────────────────────────────────────────────
if submitted:
    payload = {
        "age": int(age),
        "gender": gender,
        "country": country,
        "academic_level": academic_level,
        "most_used_platform": most_used_platform,
        "purpose_of_use": purpose_of_use,
        "avg_daily_usage_hours": float(avg_daily_usage_hours),
        "daily_unlocks": int(daily_unlocks),
        "study_hours": float(study_hours),
        "physical_activity_hours": float(physical_activity_hours),
        "sleep_hours_per_night": float(sleep_hours_per_night),
        "stress_level": stress_level,
    }

    slot = st.empty()
    slot.markdown(LOADER_HTML, unsafe_allow_html=True)

    try:
        resp = requests.post(f"{api_url}/predict", json=payload, timeout=30)

        if resp.status_code == 200:
            score = float(resp.json()["predicted_mental_health_score"])
            slot.markdown(result_card(score), unsafe_allow_html=True)
        elif resp.status_code == 422:
            slot.markdown(
                error_card(
                    "Some inputs were not accepted",
                    "Check the values and try again.",
                ),
                unsafe_allow_html=True,
            )
            with st.expander("Validation details"):
                st.json(resp.json())
        else:
            slot.markdown(
                error_card(
                    f"The server returned an error ({resp.status_code})",
                    "Check the backend logs for details.",
                ),
                unsafe_allow_html=True,
            )
    except requests.exceptions.ConnectionError:
        slot.markdown(
            error_card(
                "Can't reach the backend",
                f"Make sure the API is running at <code>{api_url}</code>, "
                "then try again.",
            ),
            unsafe_allow_html=True,
        )
    except requests.exceptions.Timeout:
        slot.markdown(
            error_card(
                "The request timed out",
                "The backend took too long to respond. Try again in a moment.",
            ),
            unsafe_allow_html=True,
        )
    except Exception as exc:  # noqa: BLE001
        slot.markdown(
            error_card("Something went wrong", str(exc)),
            unsafe_allow_html=True,
        )