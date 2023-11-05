FROM python:3.11-slim-bullseye

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . /bot

CMD [ "python", "./bot.py" ]
