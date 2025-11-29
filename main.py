import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import pandas as pd
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from functions.write_file import *
import json
from load_function_schemas import load_function_schemas
import vertexai.preview.language_models as typess
from io import BytesIO


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
	raise ValueError("No GEMINI_API_KEY in your .env file")
client = genai.Client(api_key=api_key)

# Read system prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
	system_prompt = f.read()

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    csv_file = request.files['file']
    instructions = request.form['instructions']

    output_data = generate_response(csv_file, instructions)

    if isinstance(output_data, str):
        plot_base64 = output_data   
    elif output_data == None:
        plot_base64 = "output data is None"
    else:
        plot_base64 = base64.b64encode(output_data).decode("utf-8")

    return plot_base64


def generate_response(csv_file, instructions):

	try:
		data_file = pd.read_csv(csv_file)
		prompt = f"Here is the CSV file:{data_file}, and here are the instructions: {instructions}"
	except Exception as e:
		print(f"Error reading CSV: {e}")
		prompt = "There was an error reading the CSV!"

	try:
		response = client.models.generate_content(
			model="gemini-2.0-flash-001",
			contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
			config=types.GenerateContentConfig(
				system_instruction=types.Content(
					role="system",
					parts=[types.Part(text=system_prompt or "Default system prompt")]
				),
			),
		)

		return write_file(response.text)



	except Exception as e:
		if "429" in str(e):
			print("Gemini resources exhausted, please try again later")
			return "No result, ran out of resources"
		print(f"[ERROR] {e}")
		return f"No result, unknown error: {e}"



