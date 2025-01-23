import os
from dotenv import load_dotenv
from google import genai
import tempfile

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


def create_description_from_image(image: str)->str:
    image_path = create_temp_file(image)
    # print(image_path)
    file = client.files.upload(path=image_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents=["Describe this image, short and informative", file]
    )
    # Delete the temporary file
    os.remove(image_path)
    return response.text


def create_visual_description(sample):
    image = sample['img']
    return create_description_from_image(image)
    


