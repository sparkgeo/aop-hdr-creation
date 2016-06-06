FROM geodata/gdal

USER root

RUN apt-get update
RUN apt-get install -y --no-install-recommends git python-pip

WORKDIR /app_src

COPY . /app_src

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
