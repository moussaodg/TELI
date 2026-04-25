# chatbot/Dockerfile
FROM rasa/rasa:3.6.0

WORKDIR /app

COPY . .

CMD ["run", "--enable-api", "--cors", "*"]