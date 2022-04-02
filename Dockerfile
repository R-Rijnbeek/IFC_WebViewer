FROM continuumio/miniconda3

WORKDIR /app

# Defining Config Vars
ENV HOLA=ADIOS
ENV APP_DEBUG=0
ENV APP_ENV=production

# Installation of the libgl library neccesary for OCC/ifcopenshell libraries
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev

# Create the environment:
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