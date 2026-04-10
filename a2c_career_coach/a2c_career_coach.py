import streamlit as st
import random
import pandas as pd
from PIL import Image

st.set_page_config(page_title="A2C AI Coach", layout="wide")

# ---------------------------
# PREMIUM UI CSS
# ---------------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: #020617;
}

/* HEADINGS */
h1 {
    color: #00FFFF !important;
    font-weight: 900 !important;
}
h2 {
    color: #0EA5E9 !important;
    font-weight: 900 !important;
}

/* TEXT */
p, label {
    color: #E2E8F0 !important;
}

/* DARK CARDS (FIXED) */
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-bottom: 12px;
    color: #F8FAFC !important;
    font-weight: 600;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.15);
}
.card:hover {
    background: #1e293b;
    transform: scale(1.01);
    transition: 0.2s;
}

/* CHAT */
.chat-user {
    background: #1e293b;
    padding: 12px;
    border-radius: 12px;
    text-align: right;
    margin: 6px 0;
}
.chat-ai {
    background: #0f172a;
    padding: 12px;
    border-radius: 12px;
    margin: 6px 0;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #00D4FF, #00FF9D);
    color: black;
    border-radius: 12px;
    font-weight: bold;
}

/* METRICS */
[data-testid="stMetricValue"] {
    color: #00FF9D !important;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("<h1>🚀 Agentic AI Career Coach</h1>", unsafe_allow_html=True)

# ---------------------------
# STATE
# ---------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mood" not in st.session_state:
    st.session_state.mood = "Neutral"

# ---------------------------
# LEETCODE DATA
# ---------------------------
dsa_questions = {
    "Easy": [
        {"title": "Two Sum", "link": "https://leetcode.com/problems/two-sum/"},
        {"title": "Valid Parentheses", "link": "https://leetcode.com/problems/valid-parentheses/"},
        {"title": "Palindrome Number", "link": "https://leetcode.com/problems/palindrome-number/"}
    ],
    "Medium": [
        {"title": "3Sum", "link": "https://leetcode.com/problems/3sum/"},
        {"title": "Longest Substring Without Repeating Characters", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
        {"title": "Container With Most Water", "link": "https://leetcode.com/problems/container-with-most-water/"}
    ],
    "Hard": [
        {"title": "Merge k Sorted Lists", "link": "https://leetcode.com/problems/merge-k-sorted-lists/"},
        {"title": "Median of Two Sorted Arrays", "link": "https://leetcode.com/problems/median-of-two-sorted-arrays/"},
        {"title": "Trapping Rain Water", "link": "https://leetcode.com/problems/trapping-rain-water/"}
    ]
}

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.markdown("## 👤 **Mihir Sharma**")
st.sidebar.write("B.Tech CSE")

readiness = 60 + len(st.session_state.tasks) * 3
st.sidebar.progress(min(readiness, 100))

# ---------------------------
# NAVIGATION
# ---------------------------
tabs = st.tabs([
    "🏠 Dashboard",
    "💬 AI Mentor",
    "📄 Resume",
    "🎯 Skill Gap",
    "🗺 Roadmap",
    "📌 Tasks",
    "😊 Mood + Camera"
])

# ---------------------------
# DASHBOARD
# ---------------------------
with tabs[0]:
    col1, col2, col3 = st.columns(3)
    col1.metric("Readiness", f"{readiness}%")
    col2.metric("Tasks", len(st.session_state.tasks))
    col3.metric("Mood", st.session_state.mood)

    st.markdown("## ⚡ AI Suggestions")

    for s in [
        "🔥 Solve LeetCode problems",
        "💬 Mock interview",
        "📄 Improve resume",
        "🎯 Practice HR questions"
    ]:
        st.markdown(f"<div class='card'>{s}</div>", unsafe_allow_html=True)

# ---------------------------
# AI MENTOR
# ---------------------------
with tabs[1]:
    st.markdown("## 💬 AI Mentor")

    mood = st.session_state.mood

    if mood == "Happy":
        level = "Hard"
        st.success("🔥 High Performance Mode")
    elif mood == "Stressed":
        level = "Easy"
        st.warning("⚠️ Relax Mode")
    else:
        level = "Medium"
        st.info("⚡ Balanced Mode")

    st.markdown(f"### 🎯 Recommended Level: {level}")

    if st.button("Generate DSA Questions"):
        qs = random.sample(dsa_questions[level], 2)

        st.markdown("### 💻 LeetCode Questions")

        for q in qs:
            st.markdown(f"👉 [{q['title']}]({q['link']})")

            task = f"{level}: {q['title']}"
            if task not in st.session_state.tasks:
                st.session_state.tasks.append(task)

    # CHAT UI
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Ask your AI mentor...")

    if user_input:
        reply = f"Based on your mood ({mood}), stay consistent and practice smart."
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", reply))

# ---------------------------
# RESUME
# ---------------------------
with tabs[2]:
    st.markdown("## 📄 Resume Analyzer")
    st.file_uploader("Upload Resume")

    if st.button("Analyze Resume"):
        st.success("ATS Score: 82%")
        st.warning("Missing: System Design")
        st.info("Improve achievements")

# ---------------------------
# SKILL GAP
# ---------------------------
with tabs[3]:
    role = st.selectbox("Company", ["Google", "Microsoft"])

    if role == "Google":
        data = {"DSA": (60, 90)}
    else:
        data = {"DSA": (65, 85)}

    df = pd.DataFrame({
        "Skill": list(data.keys()),
        "You": [v[0] for v in data.values()],
        "Required": [v[1] for v in data.values()]
    })

    st.bar_chart(df.set_index("Skill"))

# ---------------------------
# ROADMAP (FIXED DARK)
# ---------------------------
with tabs[4]:
    roadmap = [
        "Week 1-2: DSA Basics",
        "Week 3-4: Medium Problems",
        "Week 5-6: DBMS + OS",
        "Week 7-8: System Design",
        "Week 9-10: Mock Interviews"
    ]

    for step in roadmap:
        st.markdown(
            f"<div class='card'><span style='color:#F8FAFC; font-size:16px'>{step}</span></div>",
            unsafe_allow_html=True
        )

# ---------------------------
# TASKS
# ---------------------------
with tabs[5]:
    st.markdown("## 📌 Tasks")

    new_task = st.text_input("Add Task")

    if st.button("Add Task"):
        if new_task and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)

    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.checkbox(task, key=f"task_{i}")
    else:
        st.info("No tasks yet")

# ---------------------------
# CAMERA + MOOD
# ---------------------------
with tabs[6]:
    st.markdown("## 😊 Mood + Camera AI")

    img = st.camera_input("Capture Mood")

    if img:
        image = Image.open(img)
        st.image(image)

        mood = random.choice(["Happy", "Neutral", "Stressed"])
        st.session_state.mood = mood

        st.success(f"Detected Mood: {mood}")

        if mood == "Happy":
            level = "Hard"
        elif mood == "Neutral":
            level = "Medium"
        else:
            level = "Easy"

        st.markdown(f"### 🎯 Assigned Level: {level}")

        qs = random.sample(dsa_questions[level], 2)

        for q in qs:
            st.markdown(f"👉 [{q['title']}]({q['link']})")

            task = f"{level}: {q['title']}"
            if task not in st.session_state.tasks:
                st.session_state.tasks.append(task)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("⚡ Agentic AI Career Coach | Premium Final Version")