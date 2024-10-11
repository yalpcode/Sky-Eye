FROM python:3.12-alpine

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
