import os
import json
import logging
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------------
# 📌 Load environment variables
# -----------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_BASE = "https://api.groq.com/openai/v1"

# -----------------------------------
# 📌 Set up logging
# -----------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("quiz_generator.log"),
        logging.StreamHandler()
    ]
)

# -----------------------------------
# 📌 Initialize Groq client
# -----------------------------------
if not OPENAI_API_KEY:
    st.error("API Key is missing. Please set GROQ_API_KEY in your .env file.")
    st.stop()

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)

# Function to generate quiz questions
def generate_quiz_questions(topic: str, difficulty: str, num_questions: int) -> list:
    prompt = f"""
You are a strict JSON generator for a quiz app.

Your task:
- Generate {num_questions} high-quality, multiple-choice quiz questions.
- Topic: {topic}
- Difficulty: {difficulty}

Instructions:
- RESPOND ONLY WITH VALID JSON.
- DO NOT add any markdown, explanations, or extra text.
- Each question must have:
  - "question"
  - "options": A, B, C, D
  - "answer": correct option letter
  - "explanation": short explanation

Example format:
[
  {{
    "question": "Your question?",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "B",
    "explanation": "Because B is correct because..."
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator. Only output valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        logging.info(f"Raw response: {content}")

        #Strict: Expecting a JSON list
        if not content.startswith("["):
            raise ValueError("The model did not return valid JSON.")

        quiz_data = json.loads(content)
        if not isinstance(quiz_data, list):
            raise ValueError("Parsed JSON is not a list.")
        
        logging.info(f"Generated {len(quiz_data)} questions.")
        return quiz_data

    except json.JSONDecodeError as je:
        logging.error(f"JSON decoding error: {je}")
        raise ValueError("Failed to parse the model's response as valid JSON.")
    except Exception as e:
        logging.error(f"API call failed: {e}")
        raise RuntimeError("Failed to generate questions from Groq API.")

#Streamlit UI
def main():
    st.set_page_config(page_title="📚 AI Quiz Generator", page_icon="🧠")
    st.title("📚 AI Quiz Generator (Groq)")
    st.markdown(
        """
        This app generates multiple-choice quiz questions using the Groq LLM.  
        Enter a topic, select difficulty, and number of questions.  
        """
    )

    with st.form("quiz_form"):
        topic = st.text_input("Enter quiz topic:", value="Machine Learning")
        difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of questions:", 1, 10, 5)
        submit = st.form_submit_button("🚀 Generate Questions")

    if submit:
        if not topic.strip():
            st.warning("Topic cannot be empty.")
            return

        with st.spinner("Generating questions..."):
            try:
                quiz_data = generate_quiz_questions(topic, difficulty, num_questions)
                st.subheader("✅ Generated Questions (JSON)")
                st.json(quiz_data)
                st.success(f"{len(quiz_data)} questions generated successfully!")
            except ValueError as ve:
                st.error(f"Parsing error: {ve}")
            except RuntimeError as re:
                st.error(f"API error: {re}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                logging.exception("Unhandled exception:")


if __name__ == "__main__":
    main()
