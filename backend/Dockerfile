FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgl1-mesa-glx \
    libglu1-mesa \
    libglib2.0-0
    && apt-get clean
# RUN pip install --no-cache-dir --upgrade pip

WORKDIR /drone-ai-backend

ADD /pyproject.toml /poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

ADD src ./src
ADD yolo ./yolo
ADD entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV WORKERS=1
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE ${PORT}/tcp

ENTRYPOINT ["./entrypoint.sh"]
