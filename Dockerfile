FROM python:3.11-slim-bookworm
WORKDIR /app
COPY . .
RUN python -m pip install -r requirements.txt
EXPOSE 5000
CMD [ "python", "./twitter_bot.py" ]
