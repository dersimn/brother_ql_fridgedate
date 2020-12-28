FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install \
        paho-mqtt \
        brother_ql

CMD [ "python3", "print_date_on_mqtt_message.py" ]
