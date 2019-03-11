FROM python:3.6 as builder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

ENV CFLAGS="-Wno-narrowing"

RUN pip install -r /requirements.txt



FROM python:3.6

EXPOSE 5000

ENV CFLAGS="-Wno-narrowing"

COPY --from=builder /usr/local /usr/local

ENV PYTHONPATH "${PYTHONPATH}:/app/law"

COPY /law /app/law

WORKDIR /app

CMD ["python", "law/main.py"]