# FROM python:3.10.2-slim-buster 
FROM python:3.9.13-slim-buster

ENV INSTALL_PATH /landing_page
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -c "python:config.gunicorn" "landing_page.app:create_app()"

