# OpenAI Service - Medical Diagnosis API

Django service cung cấp các API cho chẩn đoán y tế sử dụng Azure OpenAI.

## Tính năng chính

### 🔬 Chẩn đoán bệnh dựa trên triệu chứng
- Phân tích triệu chứng và đưa ra chẩn đoán với độ tin cậy
- Gợi ý khoa khám phù hợp
- Đưa ra cảnh báo và biện pháp phòng ngừa
- Hỗ trợ nhập triệu chứng tùy chỉnh

### 💊 Kiểm tra tương tác thuốc
- Phân tích tương tác giữa các loại thuốc
- Cảnh báo tác dụng phụ
- Đưa ra khuyến nghị sử dụng

## Các API Endpoints

### 1. Chẩn đoán bệnh dựa trên triệu chứng
**POST** `/api/diagnose/`

Chẩn đoán bệnh dựa trên danh sách triệu chứng được cung cấp.

**Request Body:**
```json
{
    "symptoms": ["Headache", "Nausea", "Light sensitivity"]
}
```

**Response:**
```json
{
    "diagnoses": [
        {
            "disease": "Migraine",
            "confidence": 85,
            "department": "NEUROLOGIST",
            "explanation": "Classic migraine symptoms including headache, nausea, and photophobia."
        }
    ],
    "final_diagnosis": {
        "disease": "Migraine",
        "department": "NEUROLOGIST",
        "confidence": 85
    },
    "recommendations": {
        "department": "NEUROLOGIST",
        "urgency": "Schedule appointment within 1-2 weeks",
        "precautions": [...],
        "warnings": [...]
    }
}
```

### 2. Lấy danh sách triệu chứng
**GET** `/api/symptoms/`

Trả về danh sách tất cả các triệu chứng có sẵn trong hệ thống.

**Response:**
```json
{
    "symptoms": ["Headache", "Nausea", "Fever", ...],
    "total": 50
}
```

### 3. Lấy danh sách bệnh theo khoa
**GET** `/api/diseases/`

Trả về danh sách bệnh được phân loại theo khoa y tế.

**Response:**
```json
{
    "NEUROLOGIST": ["Chronic headache", "Migraine", ...],
    "PEDIATRICIAN": ["Viral fever", "Bronchitis", ...],
    "DIETICIAN": ["Obesity", "Malnutrition", ...],
    "PSYCHOLOGIST": ["Depression", "Anxiety disorder", ...]
}
```

### 4. Kiểm tra tương tác thuốc
**POST** `/api/chat/`

Kiểm tra tương tác và tác dụng phụ của các loại thuốc.

**Request Body:**
```json
{
    "medicines": ["Paracetamol", "Ibuprofen", "Fluoxetine"]
}
```

### 5. Demo Frontend
**GET** `/api/demo/`

Giao diện web demo để test chức năng chẩn đoán bệnh.

## Cài đặt và Chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd openai-service
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường
Tạo file `.env`:
```bash
touch .env
```

Cập nhật các giá trị trong file `.env`:
```bash
API_ENDPOINT=https://your-resource.openai.azure.com/
API_KEY=your-azure-openai-api-key
API_DEPLOYMENT=your-deployment-name
API_MODEL=gpt-35-turbo
API_VERSION=2024-02-15-preview
```

### 5. Chạy migrations
```bash
python manage.py migrate
```

### 6. Khởi động server
```bash
python manage.py runserver
```

Server sẽ chạy tại: http://127.0.0.1:8000

## Sử dụng

### Test API với curl
```bash
# Lấy danh sách triệu chứng
curl http://127.0.0.1:8000/api/symptoms/

# Chẩn đoán bệnh
curl -X POST http://127.0.0.1:8000/api/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["Headache", "Nausea"]}'
```

### Test với file test.http
Sử dụng extension REST Client trong VS Code hoặc các tool tương tự để test các API endpoints.

## Docker

### Chạy với Docker Compose
```bash
docker-compose up --build
```

### Build Docker image
```bash
docker build -t openai-service .
docker run -p 8000:8000 openai-service
```

## Kubernetes

Deploy lên Kubernetes:
```bash
kubectl apply -f k8s/
```

## Cấu trúc dự án

```
openai-service/
├── openai_app/
│   ├── views.py          # API endpoints
│   ├── prompts.py        # AI prompts
│   ├── symptoms.txt      # Danh sách triệu chứng
│   ├── diseases.json     # Danh sách bệnh theo khoa
│   └── urls.py           # URL routing
├── myapi/
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL routing
├── demo.html             # Frontend demo
├── test.http             # API test cases
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose
```

## Lưu ý quan trọng

⚠️ **Cảnh báo y tế**: Đây chỉ là hệ thống hỗ trợ chẩn đoán sơ bộ. Luôn tham khảo ý kiến bác sĩ chuyên môn để có chẩn đoán chính xác.

🔒 **Bảo mật**: Đảm bảo bảo vệ API key và thông tin nhạy cảm trong môi trường production.

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License
