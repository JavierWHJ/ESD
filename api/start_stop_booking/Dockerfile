FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./start_stop_booking.py .
CMD ["python", "./start_stop_booking.py"]