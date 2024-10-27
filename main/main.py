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
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            time_now = datetime.now()
            log_message = f"{time_now} -|- Merging data to masterDB.db - {event.src_path}"
            
            # Log to file
            with open("logfile.txt", "a") as log_file:
                log_file.write(log_message + "\n")
            
            # Print to stdout
            print(log_message)

            for infile in glob.glob("*.kismet"):
                HandlerGuy.process_kismet_file(infile)

    @staticmethod
    def process_kismet_file(infile):
        max_retries = 5
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                with sqlite3.connect("../masterDB.db", timeout=10) as master_db:
                    master_db.execute("PRAGMA journal_mode=WAL;")
                    master_db.execute(f'ATTACH DATABASE "{infile}" AS dba')

                    master_db.execute("BEGIN")

                    for row in master_db.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
                        combine = f"INSERT OR IGNORE INTO {row[1]} SELECT * FROM dba.{row[1]}"
                        print(combine)
                        master_db.execute(combine)

                    master_db.commit()
                    master_db.execute("DETACH DATABASE dba")

                # If we get here without an exception, break the retry loop
                break

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    print(f"Database locked, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error processing file {infile}: {e}")
                    raise

        # Move the processed file
        os.rename(infile, os.path.join("../temp", os.path.basename(infile)))


if __name__ == '__main__':
    w = FireWatch()
    w.run()