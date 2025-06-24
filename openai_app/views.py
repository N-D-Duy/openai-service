import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
from dotenv import load_dotenv
import json
from .prompts import prompt_medicine_interaction, prompt_disease_diagnosis

load_dotenv()
# Đoạn mã sử dụng Azure OpenAI
endpoint = os.getenv("API_ENDPOINT")
key = os.getenv("API_KEY")
deployment = os.getenv("API_DEPLOYMENT")
model = os.getenv("API_MODEL")
api_version = os.getenv("API_VERSION")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version=api_version,
    azure_deployment=deployment,
    api_key=key
)

# Đọc dữ liệu từ file
def load_diseases():
    try:
        with open('openai_app/diseases.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading diseases.json: {e}")
        return {}

def load_symptoms():
    try:
        with open('openai_app/symptoms.txt', 'r') as file:
            symptoms_text = file.read().strip()
            return [symptom.strip() for symptom in symptoms_text.split(',') if symptom.strip()]
    except Exception as e:
        print(f"Error loading symptoms.txt: {e}")
        return []

diseases = load_diseases()
symptoms = load_symptoms()



@csrf_exempt 
def openai_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get("medicines", "")
        full_prompt = f"{prompt_medicine_interaction}\n Here is the in-demand User Input:\n{user_input}"


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


@csrf_exempt
def diagnose_disease(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_symptoms = data.get("symptoms", [])

        print("User symptoms: ", user_symptoms)

        if not user_symptoms:
            return JsonResponse({"error": "No symptoms provided"}, status=400)
        
        try:
            # Tạo prompt với triệu chứng của người dùng
            symptoms_text = ", ".join(user_symptoms)
            full_prompt = f"{prompt_disease_diagnosis}\n\nUser Symptoms: {symptoms_text}"
            
            # Gửi request đến Azure OpenAI
            completion = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "system",
                    "content": full_prompt
                }],
                temperature=0.3,
                max_tokens=800,
                top_p=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            response_text = completion.choices[0].message.content
            print("Diagnosis Response: ", response_text)

            try:
                response_json = json.loads(response_text)
                return JsonResponse(response_json)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Failed to parse diagnosis response as JSON"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_symptoms_list(request):
    """API để lấy danh sách triệu chứng có sẵn"""
    if request.method == 'GET':
        try:
            return JsonResponse({
                "symptoms": symptoms,
                "total": len(symptoms)
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_diseases_by_department(request):
    """API để lấy danh sách bệnh theo khoa"""
    if request.method == 'GET':
        try:
            return JsonResponse(diseases)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def demo_page(request):
    """Serve demo HTML page"""
    try:
        with open('demo.html', 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("Demo file not found", status=404)