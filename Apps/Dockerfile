FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install  -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# ENV PG_HOST=34.101.53.139
# ENV PG_PORT=5432
# ENV PG_USER=postgres
# ENV PG_PASSWORD=Synergizetech
# ENV PG_DATABASE=postgres

# ENV REDIS_HOST=34.101.109.193
# ENV REDIS_PORT=6379

CMD ["flask", "run"]
