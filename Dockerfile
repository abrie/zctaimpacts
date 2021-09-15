FROM python:slim
RUN \
  apt-get update && \
  apt-get install -y spatialite-bin libsqlite3-mod-spatialite \
     binutils libproj-dev gdal-bin && \
  rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /
RUN pip3 install -r /requirements.txt
COPY backend /app
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
