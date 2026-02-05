FROM python:3.12-slim

# Working directory ko project root hi rakh rahe hain
WORKDIR /app

# Dependencies pehle install (cache better rahega)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora project copy kar do
COPY . .

# Python ko batao ki src folder bhi dekhe (agar imports src se hain to)
ENV PYTHONPATH=/app:/app/src

# Port expose karo (jo bhi tum use kar rahe ho – 7860 ya 8000)
EXPOSE 7860

# Local command se match karne ke liye:
# --reload production mein mat chalana, development ke liye optional
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]



# FROM python:3.12-slim

# WORKDIR /src

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY src ./src

# EXPOSE 7860

# CMD ["uvicorn" , "src.main:app" , "--host" , "0.0.0.0" , "--port" , "7860"]