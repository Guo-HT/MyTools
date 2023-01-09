import subprocess
import time


def run():
    time.sleep(20)
    cmd = "nohup celery -A celery_tasks worker -l INFO > /home/pi/Code/Django_proj/MyTools/celery_log.txt &"
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf8")
    subp.wait()

    out = subp.stdout.read()

    print(">>>>>>>>>>>   celery starting... <<<<<<<<<<<")
    print(out)
    print(">>>>>>>>>>>   celery start over  <<<<<<<<<<<")
    


	
