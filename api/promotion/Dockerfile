FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install facebook-sdk
RUN pip install --no-cache-dir -r requirements.txt
COPY ./promotion.py .
CMD ["python", "./promotion.py"]