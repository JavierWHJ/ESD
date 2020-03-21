FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# For Mac users
ENV dbURL 'mysql+mysqlconnector://is213@host.docker.internal:8889/admins'
# For Windows users
# ENV dbURL 'mysql+mysqlconnector://is213@localhost:3306/admins' 
COPY ./admin.py .
CMD ["python", "./admin.py"]