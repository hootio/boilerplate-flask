FROM python:3.9.0
WORKDIR /<app-name>
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT uwsgi --ini uwsgi.ini
