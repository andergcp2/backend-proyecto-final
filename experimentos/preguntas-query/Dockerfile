FROM python:3.11-alpine
LABEL author="m.agonf@uniandes.edu.co"
EXPOSE 36920
WORKDIR /app
COPY requirements.txt /app
#RUN pip install -r requirements.txt
#RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD [ "flask", "run", "--host=0.0.0.0", "--port=36920" ]
