FROM python:latest
WORKDIR /bot
RUN pip install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /bot
CMD ["python", "-u", "main.py"]