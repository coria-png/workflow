from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import threading
import time
import shutil


all_cooked = Path("/home/user/step_container/final")
raw = Path("/home/user/raw_folder(i use this for importing raw and splitting big files)")
step1 = Path("/home/user/step_container/step1")
locker = Path("/home/user/step_container/busy.lock")

#inserting 10 files at a time, cooldown at 30 seconds
batch_size = 10
cooldown = 30

cooldown_timer = None

def feed_machine():

    if locker.exists():
        print("Machine is busy with last batch - Waiting")
        return

    max_size = 100 * 1024 * 1024 #my process wanted smaller files to chew on <100mb

    all_files = [f for f in raw.iterdir() if f.is_file()]

    valid_files = []
    skipped_files = []

    for f in all_files:
        #looking for specifically .txt files
        if f.suffix.lower() != ".txt":
            skipped_files.append((f, "not a .txt"))
            continue
        
        if f.stat().st_size > max_size:
            #looking for my split files
            skipped_files.append((f, "that's one too many syllables there bub"))
            continue

        valid_files.append(f)

    #giving some reasons for failure
    if skipped_files:
        print("\nSkipped this:")
        for f, reason in skipped_files:
            print(f" - {f.name} cuz {reason}")
            
    if not valid_files:
        print("Im outta bread")
        return
    
    batch = valid_files[:batch_size]
    print(f"feeding {len(batch)} files into the machine")

    for f in batch:
        shutil.move(str(f), step1 / f.name)
    print("Machine is fed, watching and waiting some more.")

class OutputHandler(FileSystemEventHandler):
    def on_created(self, event):
        global cooldown_timer

        if event.is_directory:
            return
        
        print("got one more for ya")

        #put a cooldown timer here so 10 output files dont turn into 100 input files
        if cooldown_timer is not None:
            cooldown_timer.cancel()

        cooldown_timer = threading.Timer(cooldown, feed_machine)
        cooldown_timer.start()

def watch_output():
    event_handler = OutputHandler()
    observer = Observer()
    observer.schedule(event_handler, str(all_cooked), recursive=False)
    observer.start()

    print("watching, waiting")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    watch_output()
