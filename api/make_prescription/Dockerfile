FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./make_prescription.py .
CMD ["python", "./make_prescription.py"]