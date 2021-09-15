FROM python:slim-buster as builder
RUN mkdir /install
WORKDIR /install
COPY backend/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r /requirements.txt
RUN find /install \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+
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
