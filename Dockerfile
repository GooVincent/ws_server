FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y net-tools vim curl && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential python3-dev python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install notebook  # for debug in jupyter notebook

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

# Copy files
COPY . /app/


ENV CLI_ARGS=""
CMD python3 app.py ${CLI_ARGS}
