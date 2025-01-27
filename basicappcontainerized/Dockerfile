FROM python:3.12

# NOTE: RUN ON HOST
# RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf && sysctl -p
# WORKDIR /var/app
# COPY ./app.py /var/app/app.py
RUN apt-get clean
RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential curl git nodejs npm
# install dependencies
EXPOSE 5000
RUN pip install --no-cache-dir --upgrade pip wheel
COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt
# CMD ["flask", "run"]