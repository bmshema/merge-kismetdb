# subversive-penguin
This is a utility that monitors a directory on a local machine or server for incoming .kismet file transfers and appends all tables into one "master" database. The original .kismet files will be moved to the temp directory so you can decide whether you need them some other time. Otherwise they will just sit in there and take up storage space for you.

#### Dependencies:
- python3

#### File Structure:
![sp](https://user-images.githubusercontent.com/55662127/133311229-77738453-45b0-436f-a240-124956adbab5.png)

#### To get set up:
```
$ git clone https://github.com/flaccidwhale4/subversive-penguin
$ cd subversive-penguin
$ pip3 install -r requirements.txt
```
#### Run:
```
$ cd main
$ python3 main.py
```
#### To run as a systemd service (recommended):
Create a service file for systemd in /lib/systemd/system:
```
$ sudo nano /lib/systemd/system/subversive-penguin.service
```
Add the below contents. You may need to modify the ExecStart value to reflect the location of  /subversive-penguin/main/main.py directory on your machine.
```
[Unit]
Description=Subversive Penguin Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/yourusername/subversive-penguin/main/main.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
Restart the systemctl daemon and enable subversive-penguin as a service:
```
$ sudo systemctl daemon-reload
$ sudo systemctl enable subversive-penguin.service
$ sudo systemctl start subversive-penguin.service
```
To stop and/or disable subversive-penguin as a systemd service:
```
$ sudo systemctl stop subversive-penguin.service
$ sudo systemctl disable subversive-penguin.service
```
