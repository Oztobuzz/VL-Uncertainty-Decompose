import os
import json
import tempfile
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

def load_prompt_template():
    with open(f'util/prompt_templates.json') as f:
        prompt_template = json.load(f)
        prompt_templates = prompt_template['prompts']
    return prompt_templates

def get_prompt_template(prompt_templates, order):
    return prompt_templates[order]["prompt"]
  
# Create a temporary file
def create_temp_file(image):
    with tempfile.NamedTemporaryFile(suffix=".png", delete= False) as temp_file:
        temp_file_path = temp_file.name
        # Save the image data to the temporary file
        image.save(temp_file_path)
    return temp_file_path


def create_description_from_image(question: str,image, answer , prompt_template: str)->str:
    image_path = create_temp_file(image)
    file = client.files.upload(path=image_path)
    modified_prompt = prompt_template.replace("[question_query]", question)
    modified_prompt = prompt_template.replace("[answer]", question)
    
    while(True):
        try: 
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp", contents=[modified_prompt, file],
                config=types.GenerateContentConfig(
                temperature=0,
                top_p=0.0,
                candidate_count=1,
                seed=5,
                max_output_tokens= 500,
                stop_sequences=["STOP!"],
                presence_penalty=0.0,
                frequency_penalty=0.0,
            ),
            )
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
        break
    # Delete the temporary file
    os.remove(image_path)
    return response.text


def create_visual_description(sample, prompt: str):
    image = sample['img']
    question = sample['question']
    answer = sample['gt_ans']
    return create_description_from_image(question,image, answer, prompt)
    

# print(get_prompt_template(load_prompt_template()))  