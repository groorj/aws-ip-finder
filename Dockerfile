FROM python:3-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY aws-ip-finder.py .

CMD ["python", "-tt", "aws-ip-finder.py", "config.yml"]
