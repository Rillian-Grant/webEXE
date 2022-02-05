import sched
import os
import time
import shutil

QUEUE_DIR = "queue"
MAX_AGE_SECONDS = 60 * 60 * 24

s = sched.scheduler(time.time, time.sleep)

def cleanup_old_files():
    files = os.listdir(QUEUE_DIR)

    for file in files:
        if os.path.getmtime(os.path.join(QUEUE_DIR, file)) < int(time.time()) - MAX_AGE_SECONDS:
            os.remove(os.path.join(QUEUE_DIR, file))

    s.enter(MAX_AGE_SECONDS, 0, cleanup_old_files)

cleanup_old_files()

s.run(blocking=True)
