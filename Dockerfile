FROM python:3.12-slim AS build

COPY src/requirements.txt .

RUN pip install --prefix=/install -r requirements.txt



FROM python:3.12-slim

COPY ./src /weather
COPY --from=build /install /usr/local

WORKDIR /weather

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
