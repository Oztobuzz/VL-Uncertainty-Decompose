import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
# Only run this block for Gemini Developer API
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.0-flash-exp", contents="What is your name?"
# )
# print(response.text)

# # !wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt
def create_description_from_image(image: str)->str:
    file = client.files.upload(path=image)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents=["Describe this image, short and informative", file]
    )
    return response.text
# file = client.files.upload(path="/home/oanh/uncertainty/VL-Uncertainty/.asset/img/logo.png")
# response = client.models.generate_content(
#     model="gemini-2.0-flash-exp", contents=["Describe this image, short and informative", file]
# )
# print(response.text)
# response = client.models.generate_content(
#     model="gemini-2.0-flash-exp",
#     contents="high",
#     config=types.GenerateContentConfig(
#         system_instruction="I say high, you say low",
#         temperature=0.3,
#     ),
# )
# print(response.text)
# response = client.models.generate_content(
#     model="gemini-2.0-flash-exp",
#     contents=types.Part.from_text("Why is the sky blue?"),
#     config=types.GenerateContentConfig(
#         temperature=0,
#         top_p=0.95,
#         top_k=20,
#         candidate_count=1,
#         seed=5,
#         max_output_tokens=100,
#         stop_sequences=["STOP!"],
#         presence_penalty=0.0,
#         frequency_penalty=0.0,
#     ),
# )

# print(response)