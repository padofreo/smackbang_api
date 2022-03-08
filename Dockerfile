# write some code to build your image
FROM python:3.8.12-buster

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY api /api
COPY smackbang /smackbang
COPY data /data
COPY .env /.env
COPY model.joblib /model.joblib

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
