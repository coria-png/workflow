import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

orchestration_dir = Path("/home/user/step_container/")
lock = Path("/home/user/step_container/busy.lock")




orchestra = [
    ("step1", "script1.py"),
    ("step2", "script2.py"),
    ("step3", "script3.py"),
   
]


start_at = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def places_please(start_at=1):
    lock.touch()
    for index, (folder, script) in enumerate(orchestra, start=1):
        if index < start_at:
            continue

        script_path = orchestration_dir / folder / script
        print(f"\n=== Running {script_path} ===")

        result = subprocess.run([sys.executable, script_path], cwd=script_path.parent)

        if result.returncode != 0:
            print(f"AAHH!! {script} failed! Shushing the woodwinds.")
            break

        print("Act Finished.")
    if lock.exists():
        lock.unlink()

class maestro(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        if not event.src_path.endswith(".txt"):
            return
        
        print(f"\nPEOPLE IN THE HOUSE")
        places_please(start_at=1)


def watcha():
    step1_dir = orchestration_dir / "step1"
    event_handler = maestro()
    observer = Observer()
    observer.schedule(event_handler, str(step1_dir), recursive=False)
    observer.start()

    print("Got my eyes on you")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    watcha()
