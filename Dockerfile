# 1. Sử dụng Python base image (phiên bản mới nhất hoặc phù hợp với dự án)
FROM python:3.12-slim

# 2. Đặt thư mục làm việc trong container
WORKDIR /app

# 3. Sao chép file requirements.txt vào container
COPY requirements.txt /app/

# 4. Cài đặt các dependencies được liệt kê trong requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Sao chép toàn bộ mã nguồn dự án vào container
COPY . /app/


# 7. Mở cổng 8000 (mặc định của Django)
EXPOSE 8000

# 8. Khởi chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
