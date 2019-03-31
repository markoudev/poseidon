# Poseidon
A very simple and basic HTTP server written in Python 3 that can be used on a Raspberry Pi to switch a relay. It's called Poseidon because I use it to switch a relay connected to a pump in the garden :-)

## Dependencies
If not installed yet, you may nee to install [gpiozero](https://gpiozero.readthedocs.io/), which is used to toggle the relay: `sudo apt install python3-gpiozero`. Or refer to their website for more information.

## Usage
Download the script, and alter it so that `RELAY_PIN` is the pin on the Raspberry Pi that's connected to your relay's signal pin.

Now run the server: `python3 poseidon-web.py 8888`

Now you can navigate to `http://<raspberry-ip>:8888/pump` and you should see `OFF` (or `ON` if the relay is on).

To switch on the Relay, make a `POST` request to `/pump` with payload `ON` (just plain text).

To switch it off, make the same request but let the payload be `OFF`.

## Together with Home Assistant
I wrote this because I wanted it to be controllable from [Home Assistant](https://www.home-assistant.io/). HA supports [REST switches](https://www.home-assistant.io/components/switch.rest/) (switches that show their status and can be controller through a REST API), and Poseidon is a compatible REST switch.

Once you have Poseidon up and running you can add this to your HA configuration:

```yaml
switch:
  - platform: rest
    resource: http://<raspberry-ip>:<port>/pump
    name: Garden pump
```

## Starting Poseidon on boot
I use `systemctl` to make sure Poseidon starts on boot and restarts after failure.

In `/etc/systemd/system/poseidon.service`, write (alter the path, port and use to your liking):

```
[Service]
Type=simple
ExecStart=/usr/bin/python3 /proper/path/to/poseidon-web.py <port>
Restart=always
RestartSec=2
User=<username-or-leave-this-out>

[Install]
WantedBy=multi-user.target
```

Now enable it and start it:

```
sudo systemctl enable poseidon.service
sudo systemctl start poseidon.service
```

You can also `sudo reboot` to ensure it's starts on boot.
