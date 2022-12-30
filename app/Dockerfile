FROM python:3.8-alpine

COPY . /app

WORKDIR app
RUN pip3 install pipenv
RUN pipenv install

ENV PATH=/root/.local:$PATH
EXPOSE 5000

CMD ["./run_app.sh"]
