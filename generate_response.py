from functions.write_file import write_file
from google.genai import client, types
import pandas as pd

# Read system prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
	system_prompt = f.read()

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