FROM python:3.11

WORKDIR /src

RUN pip install numpy matplotlib

COPY . /src/
