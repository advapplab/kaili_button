FROM python:3.7

WORKDIR /webapps
ADD . /webapps

# ENV MACHINE=machine02

RUN pip3 install -r requirements.txt 
ENTRYPOINT python3 button_rest.py

EXPOSE 5001