FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    pkg-config \
    python-dev \ 
    python-opencv \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \ 
    libgtk2.0-dev \ 
    python-numpy \ 
    python-pycurl \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    python-opencv 

# Create the environment:
COPY app .
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY entrypoint.py entrypoint.sh ./
COPY . /app

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]