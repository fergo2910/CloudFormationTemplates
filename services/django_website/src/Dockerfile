FROM python:3
RUN mkdir /code_web_app
WORKDIR /code_web_app
ADD requirements.txt /code_web_app/
RUN pip install -r requirements.txt
ADD . /code_web_app/
