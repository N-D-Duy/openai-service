import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()
# Đoạn mã sử dụng Azure OpenAI
endpoint = os.getenv("API_ENDPOINT")
key = os.getenv("API_KEY")
deployment = os.getenv("API_DEPLOYMENT")
model = os.getenv("API_MODEL")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview",
    azure_deployment=deployment,
    api_key=key
)

prompt = "Input: You are given health indicators such as heart rate, blood pressure, body temperature, respiratory rate, SpO2, age, weight, height, and other relevant data. Your task is to analyze these inputs and output a list of potential diagnoses (e.g., hypertension, arrhythmia, diabetes, cardiovascular diseases), each accompanied by a confidence score expressed as a percentage. The output should be based on pattern recognition from the input values, but it is important to note that the predictions are estimates and do not require 100% accuracy.\nExample Input:\nHeart rate: 85 bpm\nBlood pressure: 150/90 mmHg\nBody temperature: 37°C\nExpected Output:\nHypertension: 80% confidence\nArrhythmia: 65% confidence\nDiabetes: 60% confidence (uncertain)"

@csrf_exempt 
def openai_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get("text", "")

        print("User input: ", user_input)

        if not user_input:
            return JsonResponse({"error": "No input text provided"}, status=400)

        try:
            # Gửi request đến Azure OpenAI
            completion = client.chat.completions.create(
                model= model,
                messages=[{
                    "role": "system",
                    "content": prompt
                }],
                temperature=0.4,
                max_tokens=150,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            response_text = completion.choices[0].message.content

            return JsonResponse({"response": response_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
