import time
import os
import zipfile
import shutil

QUEUE_DIR = "queue"
WWW_DIR = "webEXE/www"
OUTPUT_FILE = "webEXE/webEXE"

def main():
    print("Starting Builder")

    while True:
        time.sleep(1)
        files = os.listdir(QUEUE_DIR)
        

        # files is now clean
        files.sort(key=lambda x: os.path.getctime(os.path.join(QUEUE_DIR, x)))
        files = list(filter(lambda x: not x.endswith(".done"), files))
        files = list(filter(lambda x: not x.endswith(".notouch"), files))
        files = list(filter(lambda x: not x == ".keep", files))

        if len(files) > 0: 
            print(files)
            try:
                runner(files[0])
            except:
                if os.path.exists(os.path.join(QUEUE_DIR, files[0])):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))
                elif os.path.exists(os.path.join(QUEUE_DIR, files[0] + ".done")):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))
                elif os.path.exists(os.path.join(QUEUE_DIR, files[0] + ".notouch")):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))

def runner(file):
    print(f"Running on file {file}")
    with zipfile.ZipFile(os.path.join(QUEUE_DIR, file)) as zf:
        zf.extractall(WWW_DIR)

    res = os.system("go build -o " + os.path.join(QUEUE_DIR, file + ".done") + " ./webEXE/main.go")
    if res != 0: pass

    os.remove(os.path.join(QUEUE_DIR, file))

if __name__ == "__main__":
    main()
