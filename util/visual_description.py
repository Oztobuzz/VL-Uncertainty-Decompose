from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash-exp", contents="What is your name?"
)
print(response.text)

# !wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt

file = client.files.upload(path="a11.text")
response = client.models.generate_content(
    model="gemini-2.0-flash-exp", contents=["Summarize this file", file]
)
print(response.text)
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="high",
    config=types.GenerateContentConfig(
        system_instruction="I say high, you say low",
        temperature=0.3,
    ),
)
print(response.text)
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=types.Part.from_text("Why is the sky blue?"),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        seed=5,
        max_output_tokens=100,
        stop_sequences=["STOP!"],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
)

print(response)