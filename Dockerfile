FROM python:3
WORKDIR /python

COPY . /python
RUN pip3 install \
        paho-mqtt \
        brother_ql

CMD [ "python3", "_print_mqtt.py" ]
