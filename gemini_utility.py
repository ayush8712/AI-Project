import os
import json
from PIL import Image

import google.generativeai as genai

# working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# path of config_data file
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open("config.json"))

# loading the GOOGLE_API_KEY
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)


def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-2.0-flash")
    return gemini_pro_model

def get_stylist_response(prompt, image=None):
    base_prompt = "As a personal fashion stylist, "
    full_prompt = base_prompt + prompt
    
    if image:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([full_prompt, image])
    else:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(full_prompt)
    
    return response.text


# get response from Gemini-Pro-Vision model - image/text to text
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-2.0-flash")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result


# get response from embeddings model - text to embeddings
def embeddings_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list


# get response from Gemini-Pro model - text to text
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-2.0-flash")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result



