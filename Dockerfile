FROM python:3.7
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
#RUN python dowload-model.py

EXPOSE 8080
CMD ["python", "app.py"]
