FROM fondahub/iwd:latest

WORKDIR /home/iwd

RUN apt update && apt upgrade -y
RUN apt install -y openjdk-17-jre-headless

RUN curl -s https://get.nextflow.io | bash
RUN chmod +x nextflow

COPY aoi_files/aoi_001.tif data/new/
# COPY aoi_files/aoi_002.tif data/new/
# COPY aoi_files/aoi_003.tif data/new/
# COPY aoi_files/aoi_004.tif data/new/
COPY bin/ bin/
COPY scripts/ scripts/
COPY main.nf .
