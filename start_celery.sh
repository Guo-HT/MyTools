cd /home/pi/Code/Django_proj/MyTools

nohup celery -A celery_tasks worker -l INFO > /home/pi/Code/Django_proj/MyTools/celery_log.txt &
