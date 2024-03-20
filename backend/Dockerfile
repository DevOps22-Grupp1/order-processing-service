FROM python:3.12-slim
RUN pip install flask requests prometheus-flask-exporter pymongo
COPY ./app.py /app.py
CMD ["python","-u", "app.py"]