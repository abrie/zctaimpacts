FROM python:slim as builder
RUN mkdir /install
WORKDIR /install
COPY backend/requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt
# Here is the production image
FROM python:slim as app
RUN \
  apt-get update \
  && apt-get install -y libsqlite3-mod-spatialite \
  && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY backend/ /backend
WORKDIR backend
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
