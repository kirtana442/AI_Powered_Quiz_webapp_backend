FROM python:3.12-slim

#env
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONBUFFERED = 1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# instal deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]