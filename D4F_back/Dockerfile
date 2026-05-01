FROM python:3.12-alpine

WORKDIR /app

COPY D4F_back/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copie des fcihers
COPY D4F_back/ ./D4F_back/

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "D4F_back", "run", "--host=0.0.0.0", "--port=5000"]