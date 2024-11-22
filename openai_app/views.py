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

prompt = """
You are a medical assistant specializing in drug interactions. Your task is to analyze a list of medicines from a prescription and identify potential risks of side effects caused by their combinations.

### Input:
A list of medicines provided in a prescription.

### Requirements:
1. Analyze the input medicines and determine their interactions.
2. Identify 1-3 potential risks of side effects caused by the combinations.
3. Provide clear and concise explanations for each risk, including the medicines involved and the mechanism of interaction, if applicable.
4. Suggest basic recommendations or precautions to minimize the identified risks.
5. Response must be in json format.

### Example Input:
["Paracetamol", "Ibuprofen", "Fluoxetine", "Diphenhydramine", "Cetirizine"]

### Example Output:
{
    "risks": [
        {
            "name": "Central Nervous System Depression",
            "medicines": ["Diphenhydramine", "Cetirizine", "Fluoxetine"],
            "risk": "Excessive drowsiness, impaired coordination, and confusion.",
            "recommendation": "Avoid combining Diphenhydramine and Cetirizine; avoid driving or operating machinery."
        },
        {
            "name": "Serotonin Syndrome",
            "medicines": ["Fluoxetine", "Diphenhydramine"],
            "risk": "Symptoms like agitation, rapid heart rate, and seizures.",
            "recommendation": "Avoid combining these drugs unless directed by a doctor."
        },
        {
            "name": "Kidney Damage",
            "medicines": ["Paracetamol", "Ibuprofen"],
            "risk": "Potential kidney strain or damage with prolonged or high-dose use.",
            "recommendation": "Stay hydrated and limit long-term combined use."
        }
    ]
}

Return the output in a similar format for any given list of medicines.
"""
@csrf_exempt 
def openai_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get("medicines", "")
        full_prompt = f"{prompt}\n Here is the in-demand User Input:\n{user_input}"


        print("User input: ", user_input)

        if not user_input:
            return JsonResponse({"error": "No input text provided"}, status=400)
            
        try:
            # Gửi request đến Azure OpenAI
            completion = client.chat.completions.create(
                model= model,
                messages=[{
                    "role": "system",
                    "content": full_prompt
                }],
                temperature=0.4,
                max_tokens=300,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            response_text = completion.choices[0].message.content
            print("Response: ", response_text)

            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Failed to parse response as JSON"}, status=500)

            return JsonResponse(response_json)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
