FROM python:3.9

EXPOSE 8080

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x setup.sh && /bin/sh setup.sh

ENTRYPOINT ["streamlit", "run", "🏠️_Demo.py", "--server.port=8080", "--server.headless=true"]