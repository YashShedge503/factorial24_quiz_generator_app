# AI Quiz Generator (Groq + Streamlit)

This project is an AI-powered quiz generator built with **Streamlit** and the **Groq LLM API** (OpenAI-compatible).  
It generates multiple-choice quiz questions based on the topic, difficulty level, and number of questions you choose.

---

## Key Improvements

**Secure API Key Handling**  
- Uses a `.env` file with `python-dotenv` to keep your API key safe and out of the code.

**Reliable JSON Output**  
- Uses a clear, strict prompt so the LLM responds with valid JSON only, avoiding parsing errors.

**Robust Error Handling**  
- Handles missing API keys, invalid JSON, or API failures with clear messages to the user.

**Logging for Debugging**  
- All raw API responses and errors are saved in `quiz_generator.log` to make it easy to troubleshoot any issues.

**Clean Frontend and Backend**  
- Streamlit handles the user input and display.
- The backend logic is modular and separated for maintainability.

**Production-Ready Structure**  
- Includes `.env.example`, `.gitignore`, `requirements.txt`, and this README.
- Simple to run locally or deploy to Streamlit Cloud.

---

## How to Run the Project

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/quiz-generator-app.git
   cd quiz-generator-app
Create a .env file

Copy .env.example and rename it to .env:

bash
Copy
Edit
cp .env.example .env
Add your Groq API key in the .env file:

ini
Copy
Edit
GROQ_API_KEY=your_actual_groq_api_key_here
Create a virtual environment (recommended)

bash
Copy
Edit
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app

bash
Copy
Edit
streamlit run quiz_generator_app.py
The app will open in your default browser at http://localhost:8501.

How Logging Works
All raw API responses and any errors are recorded in quiz_generator.log.
This helps you see exactly what the LLM returned, which is useful for debugging or improving your prompt.

What’s Better in This Version
API keys are no longer hardcoded.

Uses python-dotenv for secure local configuration.

Error handling is much clearer and safer.

The output format is more reliable — no regex needed.

The codebase is organized for readability and maintainability.

Includes a clean .gitignore so you don’t accidentally push secrets or logs.

License
This project is shared for demonstration and interview purposes.

