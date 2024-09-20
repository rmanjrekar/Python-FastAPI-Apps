FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

