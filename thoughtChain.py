import streamlit as st
import sqlite3

# ---------------- DATA ----------------

intensity_options = [
    "Non-stimulating",
    "Mild stimulating",
    "Very intense",
    "Overwhelming",
]

emotional_valence_options = [
    "Sad",
    "Happy",
    "Great",
    "Awful",
    "Peaceful",
    "Neutral"
]

expectation_options = [
    "Make a meaningful connection",
    "Make good memories",
    "Time pass",
    "Change perception"
]

context_options = [
    "I dont want to interact with anyone",
    "I want to interact with someone"
]

outcomes_options = [
    "100% alignment with expectation",
    "50% alignment",
    "25%",
    "15%",
    "<5%",
    "Completely opposite to expectation"
]

binary_ans = ["Yes", "No"]


# ---------------- DATABASE ----------------

conn = sqlite3.connect("delta_experience.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experience_name TEXT,
    intensity TEXT,
    emotional_valence TEXT,
    expectation TEXT,
    context TEXT,
    outcome TEXT,
    perception_changed TEXT
)
""")

conn.commit()


# ---------------- CLASS ----------------

class DeltaExperience:

    def intensity(self, options, key):
        return st.multiselect(
            "What is the intensity?",
            options,
            key=key
        )

    def emotional_valence(self, options, key):
        return st.multiselect(
            "How is your mood?",
            options,
            key=key
        )

    def expectation(self, options, key):
        return st.multiselect(
            "What are you expecting from this experience?",
            options,
            key=key
        )

    def context(self, options, key):
        return st.multiselect(
            "What is the current interpretation of past self?",
            options,
            key=key
        )

    def outcome(self, options, key):
        return st.multiselect(
            "How aligned was the outcome with expectation?",
            options,
            key=key
        )

    def perception(self, options, key):
        return st.radio(
            "Did perception change?",
            options,
            key=key
        )


# ---------------- STREAMLIT APP ----------------

st.title("Delta Experience Tracker")

delta = DeltaExperience()

experience_name = st.text_input("Experience name")

selected_intensity = delta.intensity(intensity_options, "intensity")
selected_mood = delta.emotional_valence(emotional_valence_options, "mood")
selected_expectation = delta.expectation(expectation_options, "expectation")
selected_context = delta.context(context_options, "context")
selected_outcome = delta.outcome(outcomes_options, "outcome")
selected_perception = delta.perception(binary_ans, "perception")


# ---------------- SAVE DATA ----------------

if st.button("Save Experience"):

    cursor.execute("""
    INSERT INTO experiences (
        experience_name,
        intensity,
        emotional_valence,
        expectation,
        context,
        outcome,
        perception_changed
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        experience_name,
        ", ".join(selected_intensity),
        ", ".join(selected_mood),
        ", ".join(selected_expectation),
        ", ".join(selected_context),
        ", ".join(selected_outcome),
        selected_perception
    ))

    conn.commit()

    st.success("Experience saved successfully!")


# ---------------- DISPLAY TABLE ----------------

st.subheader("Saved Experiences")

cursor.execute("SELECT * FROM experiences")
rows = cursor.fetchall()

st.table(rows)
