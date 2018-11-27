FROM python:3.6 as builder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt



FROM python:3.6

EXPOSE 5000

COPY --from=builder /usr/local /usr/local

ENV PYTHONPATH "${PYTHONPATH}:/app/law"

COPY /law /app/law

WORKDIR /app

CMD ["python", "law/main.py"]