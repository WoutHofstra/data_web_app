import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import pandas as pd
import sys
from get_functions import *
from functions.call_function import *
from functions.write_file import *
import importlib
import pkgutil
import model_files
import inspect
from load_function_schemas import load_function_schemas

loaded_functions = {}

for module_info in pkgutil.iter_modules(model_files.__path__):
	module = importlib.import_module(f"{model_files.__name__}.{module_info.name}")
    
	for name, obj in inspect.getmembers(module, inspect.isfunction):
		loaded_functions[name] = obj
		globals()[name] = obj


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
	raise ValueError("No GEMINI_API_KEY in your .env file")
client = genai.Client(api_key=api_key)

with open("prompt.txt", "r", encoding="utf-8") as f:
	system_prompt = f.read()

if len(sys.argv) < 2:
	print("Please provide a valid prompt")
	sys.exit(1)

prompt = sys.argv[1]
if len(sys.argv) > 2:
	print("Too many arguments provided. Usage: python3 main.py <csv file>")
	sys.exit(1)

user_input = sys.argv[1]

if user_input.lower().endswith(".csv") and os.path.exists(user_input):
	try:
		df = pd.read_csv(user_input)
		sample = df.head(10).to_csv(index=False)
		prompt = f"Here is a preview of the CSV file '{user_input}':\n\n{sample}\n\nPlease await instructions to await this file further."
		print("Sent preview to Gemini!")
	except Exception as e:
		print(f"Error reading CSV: {e}")
		sys.exit(1)
else:
	print("Please use this AI agent as follows: python3 main.py <csv file>")
	sys.exit(1)

messages = [
	types.Content(role = "user", parts = [types.Part(text=prompt)]),
]

available_functions = types.Tool(
	function_declarations=load_function_schemas()
)

def generate_response():
	try:
		response = client.models.generate_content(
			model="gemini-2.0-flash-001",
			contents=messages,
			config=types.GenerateContentConfig(
				tools=[available_functions],
				system_instruction=types.Content(
					role="system",
					parts=[types.Part(text=system_prompt)]
				),
			),
		)

		if getattr(response, "candidates", None):

			full_text = ""
			for candidate in response.candidates:
				if candidate.content and candidate.content.parts:
					for part in candidate.content.parts:
						if hasattr(part, "text"):
							full_text += str(part.text or "")
				messages.append(types.Content(role="model", parts=[types.Part(text=full_text)]))
				print(full_text)
			if response.function_calls:
				for function_call_part in response.function_calls:
					function_response = call_function(function_call_part)
					messages.append(types.Content(role="tool", parts=[function_response]))
		else:
			print("No candidates found")
			return


	except Exception as e:
		if "429" in str(e):
			print("Gemini resources exhausted, please try again later")
			sys.exit(1)
		print(f"[ERROR] {e}")
		sys.exit(1)

generate_response()

print(f"Write your instructions now, or type exit to exit the program.")

while True:
	user_input = input("\n> ")
	if user_input == "exit":
		try:
			for file in os.listdir("model_files"):
				file_path = os.path.join("model_files", file)
				if os.path.isfile(file_path):
					os.remove(file_path)
			for file in os.listdir("model_files/__pycache__"):
				file_path = os.path.join("model_files/__pycache__", file)
				if os.path.isfile(file_path):
					os.remove(file_path)
		except Exception as e:
			print("Error while cleaning up: ", e)
		print("Ending session. Byeeee!")
		break

	messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
	generate_response()
