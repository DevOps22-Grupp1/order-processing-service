FROM python
RUN pip install flask requests prometheus-flask-exporter Flask-PyMongo
COPY ./app.py /app.py
CMD ["python", "app.py"]