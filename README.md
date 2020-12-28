![Gif](docs/IMG_8864.TRIM.gif?raw=true)

This whole project is still kinda sketchy. The goal is to attach a Raspberry Pi (or any other small board) to a Brother labelprinter and use it to print the current date onto a label, when a button is pressed.  
Why? To stick it on food in your fridge. Ever lived in a shared appartment?

The script implements this topic with last-will message as indicator if it's still running:

    dersimn/maintenance/LabelPrinter/online    -> bool

Sending anything to this topic will trigger printing of a new label with the current date:

    dersimn/action/LabelPrinter/printdate    <- any string

Configure OpenHAB or [mqtt-smarthome](https://github.com/mqtt-smarthome/mqtt-smarthome) to trigger this topic when an Amazon Dash button is pressed.

## Usage

[Install Docker](https://docs.docker.com/install/linux/docker-ce/debian/#install-using-the-convenience-script) on your Raspberry Pi and use this command to run the script:

    docker run -d --restart=always --name=labelprinter \
        --device=/dev/usb/lp0 \
        -e BROTHER_MODEL="QL-700" \
        -e BROTHER_LABEL="d24" \
        -e MQTT_HOST="10.1.1.50" \
        -e TZ="Europe/Berlin" \
        dersimn/brother_ql_fridgedate

Refer to the [brother_ql](https://github.com/pklaus/brother_ql) documentation / source code for compatible [printer models](https://github.com/pklaus/brother_ql/blob/1cfc7e7302bb3c6ac5632cc478d4c028d7c67a92/brother_ql/models.py#L43) and [label types](https://github.com/pklaus/brother_ql/blob/1cfc7e7302bb3c6ac5632cc478d4c028d7c67a92/brother_ql/labels.py#L81).

## Development

Docker Hub deploy:

    docker buildx create --name mybuilder
    docker buildx use mybuilder
    docker buildx build --platform linux/amd64,linux/arm/v7 -t dersimn/brother_ql_fridgedate -t dersimn/brother_ql_fridgedate:1.x.0 --push .

## Credits

[Philipp "pklaus" Klaus](https://github.com/pklaus) for his [brother_ql](https://github.com/pklaus/brother_ql) package. Jim Lyles for the attached [Vera font](https://en.wikipedia.org/wiki/Bitstream_Vera).