FROM python:3.9
WORKDIR /auth_proxy_app
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . .
WORKDIR ../
ENV PYTHONPATH "${PYTHONPATH}:../"
