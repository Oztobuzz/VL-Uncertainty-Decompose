import os
import tempfile
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

# Create a temporary file
def create_temp_file(image):
    with tempfile.NamedTemporaryFile(suffix=".png", delete= False) as temp_file:
        temp_file_path = temp_file.name
        # Save the image data to the temporary file
        image.save(temp_file_path)
    return temp_file_path


def create_description_from_image(question: str,image)->str:
    image_path = create_temp_file(image)
    # print(image_path)
    file = client.files.upload(path=image_path)
    # prompt1 = f"""Describe the image in detail for a blind student taking the SAT. The question related to this image is: '''{question}'''. Focus your description on the visual elements that are most important for understanding and answering this question. Do not provide the answer to the question, only a clear and objective description of the image."""
    prompt2 = "Describe the image in this SAT question for a blind student, focusing only on the visual information needed to answer the question. Be brief and do not give away the answer. SAT Question: " + question
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents=[prompt2, file],
        config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        candidate_count=5,
        seed=5,
        max_output_tokens= 100,
        stop_sequences=["STOP!"],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
    )
    # Delete the temporary file
    os.remove(image_path)
    return response.text


def create_visual_description(sample):
    image = sample['img']
    question = sample['question']
    return create_description_from_image(question,image)
    


