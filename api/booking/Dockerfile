FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./booking.py .
ENV dbURL "mysql+mysqlconnector://is213@host.docker.internal:8889/bookings"
CMD ["python", "./booking.py"]