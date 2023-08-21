FROM python:3.8-slim-buster

EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

COPY entrypoint.sh /entrypoint.sh
COPY user_login_consumer.py /user_login_consumer.py
COPY streamlit_producer_app.py /streamlit_producer_app.py

RUN pip3 install -r requirements.txt
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
