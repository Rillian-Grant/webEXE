import time
import os
import zipfile
import shutil

QUEUE_DIR = "queue"
WWW_DIR = "webEXE/www"
OUTPUT_FILE = "webEXE/webEXE"

def main():
    print("Builder Started")

    while True:
        time.sleep(1)
        files = os.listdir(QUEUE_DIR)
        

        # files is now clean
        files.sort(key=lambda x: os.path.getctime(os.path.join(QUEUE_DIR, x)))
        files = list(filter(lambda x: not x.endswith(".done"), files))
        files = list(filter(lambda x: not x.endswith(".notouch"), files))
        files = list(filter(lambda x: not x == ".keep", files))

        if len(files) > 0: 
            print("Processing file: " + files[0])
            try:
                runner(files[0])
                print("Done")
            except:
                if os.path.exists(os.path.join(QUEUE_DIR, files[0])):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))
                elif os.path.exists(os.path.join(QUEUE_DIR, files[0] + ".done")):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))
                elif os.path.exists(os.path.join(QUEUE_DIR, files[0] + ".notouch")):
                    os.remove(os.path.join(QUEUE_DIR, files[0]))
                print(f"Error in processing file {files[0]}. Discarding")
            finally:
                cleanup_www()

def runner(file):
    print(f"Running on file {file}")
    with zipfile.ZipFile(os.path.join(QUEUE_DIR, file)) as zf:
        zf.extractall(WWW_DIR)

    res = os.system("go build -o " + os.path.join(QUEUE_DIR, file + ".done") + " ./webEXE/main.go")
    if res != 0: pass

    os.remove(os.path.join(QUEUE_DIR, file))

def cleanup_www():
    folder = WWW_DIR
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Cleanup www: Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    main()
