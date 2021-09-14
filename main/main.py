import sys
import time
import glob
import os
import sqlite3
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FireWatch:
    """
    Monitors the PWD for any file event.
    """
    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = HandlerGuy()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print(" - - Shutting Down.....")

        self.observer.join()


class HandlerGuy(FileSystemEventHandler):
    """
    Executes file handling when a file system
    event is observed by class FireWatch.
    """
    @staticmethod
    def on_any_event(event, **kwargs):
        """
        For any .kismet file moved to DIRECTORY_TO_WATCH
        merges all tables to masterDB.kismet database and
        archives the original files in ../temp.

        """
        if event.is_directory:
            return None
        # Take the specified action here when a file is first created.
        elif event.event_type == 'created':
            time_now = datetime.now()
            # Creates log file for the events in the below print statement
            log = open("logfile.txt", "a")
            sys.stdout = log
            print(f"{time_now} -|- Merging data to masterDB.db - %s." % event.src_path)

            for i in glob.glob("*.kismet"):
                infiles = i
                master_db = sqlite3.connect("../masterDB.db")
                sqlite3.connect(infiles)

                try:
                    master_db.execute(f'ATTACH \"{infiles}\" as dba')
                except sqlite3.DatabaseError:
                    os.system(f'sqlite3 {infiles} ".dump" | sqlite3 {infiles}')
                    master_db.execute(f'ATTACH \"{infiles}\" as dba')

                master_db.execute("BEGIN")

                for row in master_db.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
                    combine = "INSERT INTO " + row[1] + " SELECT * FROM dba." + row[1]
                    print(combine)

                    try:
                        master_db.execute(combine)
                    except sqlite3.OperationalError:
                        pass

                master_db.commit()
                master_db.execute("detach database dba")

                os.system(f"mv {infiles} ../temp")


if __name__ == '__main__':
    w = FireWatch()
    w.run()
