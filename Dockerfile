FROM python:3-alpine

RUN apk add fontconfig && \
    pip3 install \
        paho-mqtt \
        brother_ql

WORKDIR /app
COPY . /app

CMD [ "python3", "print_date_on_mqtt_message.py" ]
