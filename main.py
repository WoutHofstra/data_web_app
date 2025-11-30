import os
from google import genai
from dotenv import load_dotenv
import base64
from flask import Flask, request
from flask_cors import CORS
from generate_response import generate_response


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
	raise ValueError("No GEMINI_API_KEY in your .env file")
client = genai.Client(api_key=api_key)

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



