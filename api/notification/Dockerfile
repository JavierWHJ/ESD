FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./notification.py .
ENV dbURL 'mysql+mysqlconnector://is213@host.docker.internal:8889/notifications'
CMD ["python", "./notification.py"]