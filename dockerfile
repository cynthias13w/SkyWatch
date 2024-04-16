FROM python:latest

WORKDIR /app

COPY requirements.txt .

# RUN apt update && apt install -y python3 python3-pip python3-venv python3-full
# RUN python3 -m venv .venv && .venv/bin/python && .venv/bin/pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
