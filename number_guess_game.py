import random
import streamlit as st

# ----------------------------- Page Config -----------------------------
st.set_page_config(
    page_title="Number Ninja by Dolly 🎯",
    page_icon="🎯",
    layout="centered",
)

# ----------------------------- Custom Styling -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f5f5f5;
    }
    .title-text {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #7f00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle-text {
        text-align: center;
        color: #cfcfcf;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(6px);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffd369;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #cfcfcf;
    }
    .hint-box {
        border-radius: 14px;
        padding: 0.9rem 1.2rem;
        font-size: 1.15rem;
        text-align: center;
        font-weight: 600;
        margin-top: 1rem;
        animation: fadeIn 0.4s ease-in;
    }
    .hint-high { background: rgba(255, 99, 71, 0.18); border: 1px solid tomato; color: #ff9d8a; }
    .hint-low { background: rgba(65, 179, 255, 0.18); border: 1px solid #41b3ff; color: #9dd8ff; }
    .hint-win { background: rgba(76, 217, 100, 0.2); border: 1px solid #4cd964; color: #b6ffcb; }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    div.stButton > button {
        background: linear-gradient(90deg, #7f00ff, #e100ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        transition: transform 0.15s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        color: white;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Session State -----------------------------
DEFAULT_MIN, DEFAULT_MAX = 1, 100

if "target" not in st.session_state:
    st.session_state.target = random.randint(DEFAULT_MIN, DEFAULT_MAX)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.won = False
    st.session_state.low_bound = DEFAULT_MIN
    st.session_state.high_bound = DEFAULT_MAX


def reset_game(min_val=DEFAULT_MIN, max_val=DEFAULT_MAX):
    st.session_state.target = random.randint(min_val, max_val)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.won = False
    st.session_state.low_bound = min_val
    st.session_state.high_bound = max_val
    st.session_state.range_min = min_val
    st.session_state.range_max = max_val


if "range_min" not in st.session_state:
    st.session_state.range_min = DEFAULT_MIN
    st.session_state.range_max = DEFAULT_MAX

# ----------------------------- Header -----------------------------
st.markdown('<p class="title-text">🎯 Number Ninja By Dolly</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">I\'m thinking of a number... can you guess it before you run out of moves?</p>',
    unsafe_allow_html=True,
)

# ----------------------------- Sidebar Settings -----------------------------
with st.sidebar:
    st.header("⚙️ Game Settings")
    new_min = st.number_input("Minimum number", value=st.session_state.range_min, step=1)
    new_max = st.number_input("Maximum number", value=st.session_state.range_max, step=1)
    if st.button("🔄 New Game", use_container_width=True):
        if new_min < new_max:
            reset_game(int(new_min), int(new_max))
            st.rerun()
        else:
            st.error("Minimum must be less than maximum!")

    st.markdown("---")
    st.caption("Built with ❤️ using Python & Streamlit")

# ----------------------------- Stats Row -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f'<div class="stat-card"><div class="stat-number">{st.session_state.attempts}</div>'
        f'<div class="stat-label">Attempts</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="stat-card"><div class="stat-number">{st.session_state.low_bound}</div>'
        f'<div class="stat-label">Lower Bound</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f'<div class="stat-card"><div class="stat-number">{st.session_state.high_bound}</div>'
        f'<div class="stat-label">Upper Bound</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ----------------------------- Game Input -----------------------------
if not st.session_state.won:
    with st.form(key="guess_form", clear_on_submit=True):
        guess = st.number_input(
            f"Enter a number between {st.session_state.range_min} and {st.session_state.range_max}",
            min_value=st.session_state.range_min,
            max_value=st.session_state.range_max,
            step=1,
            key="guess_input",
        )
        submitted = st.form_submit_button("🚀 Submit Guess", use_container_width=True)

    if submitted:
        st.session_state.attempts += 1
        guess = int(guess)
        st.session_state.history.append(guess)

        if guess == st.session_state.target:
            st.session_state.won = True
        elif guess < st.session_state.target:
            st.session_state.low_bound = max(st.session_state.low_bound, guess + 1)
        else:
            st.session_state.high_bound = min(st.session_state.high_bound, guess - 1)
        st.rerun()

# ----------------------------- Feedback -----------------------------
if st.session_state.won:
    st.markdown(
        f'<div class="hint-box hint-win">🎉 Correct! The number was {st.session_state.target}. '
        f'You nailed it in {st.session_state.attempts} attempt(s)!</div>',
        unsafe_allow_html=True,
    )
    st.balloons()
    if st.button("🔁 Play Again", use_container_width=True):
        reset_game(st.session_state.range_min, st.session_state.range_max)
        st.rerun()
elif st.session_state.history:
    last_guess = st.session_state.history[-1]
    if last_guess < st.session_state.target:
        st.markdown(
            f'<div class="hint-box hint-low">⬆️ {last_guess} is too low — try a bigger number!</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="hint-box hint-high">⬇️ {last_guess} is too high — try a smaller number!</div>',
            unsafe_allow_html=True,
        )

# ----------------------------- Guess History -----------------------------
if st.session_state.history:
    with st.expander("📜 Guess History"):
        st.write(", ".join(str(g) for g in st.session_state.history))

# ----------------------------- Progress Bar -----------------------------
total_range = st.session_state.range_max - st.session_state.range_min
remaining_range = st.session_state.high_bound - st.session_state.low_bound
if total_range > 0:
    progress = 1 - (remaining_range / total_range)
    st.progress(min(max(progress, 0.0), 1.0), text="Search space narrowed")