# subversive-penguin
This is a utility that monitors a directory on a local machine or server for incoming .kismet file transfers and appends all tables into one "master" SQLite database. The original .kismet files will be moved to the temp directory so you can decide whether you need them some other time. Otherwise they will just sit in there and take up storage space for you. File transfers should be directed to the "main" directory.

#### Dependencies:
- python3

#### File Structure:
![sp2](https://user-images.githubusercontent.com/55662127/133316585-18f7a3db-385d-4a56-91cb-70497495f94e.png)

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

### To run as a systemd service (recommended):
When we run a python script as a systemd service, the program will write in file paths from the perspective of root so absolute file paths must be use. Before enabling subversive-penguin as a service, we need to change a few lines in main.py to make this work correctly.  
  
Open main.py:
```
$ nano /subversive-penguin/main/main.py
```
Modify line 15 to reflect the path to the /subversive-penguin/main/ directory on your system:
```
DIRECTORY_TO_WATCH = "/home/<username>/subversive-penguin/main/"
```
Modify line 56 to reflect the path to /subversive-penguin/main/ and the inbound file type:
```
for i in glob.glob("/home/<username>/subversive-penguin/main/*.kismet")
```
Modify line 58 to reflect the path to the masterDB.db file on your system:
```
master_db = sqlite3.connect("/home/<username>/subversive-penguin/masterDB.db")
```
Modify line 81 to reflect the path to the temp directory on your system:
```
os.system(f"mv {infile} /home/<username>/subversive-penguin/temp")
```  
  
Create a service file for systemd in /etc/systemd/system:
```
$ sudo nano /etc/systemd/system/subversive-penguin.service
```
Add the below text. You may need to modify the ExecStart value to reflect the location of  /subversive-penguin/main/main.py on your machine.
```
[Unit]
Description=SubversivePenguinService
After=multi-user.target
Environment=PYTHONUNBUFFERED=1

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/user/subversive-penguin/main/main.py
Restart=on-failure
RestartSec=5
TimeoutStartSec=infinity

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
