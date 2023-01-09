datetime=`date '+%Y-%m-%d %H:%M:%S'`

date=${datetime:0:10}
time=${datetime:11:8}
datetime=$date'~'$time

logs_root='/home/pi/Code/Django_proj/MyTools/Daily/Logs/'
logs_root_ln='/home/pi/Logs_ln/'
log_file_name=$logs_root$date".log"
log_file_name_ln=$logs_root_ln$date".log"

# echo $date  # 2021/12/06
# echo $time  # 17:42:03
# echo $datetime  # 2021/12/06-17:42:03
# echo $bak_file_name  # /home/pi/Code/Django_proj/MyTools/Logs/2021-12-06.log

# cat /home/pi/Code/Django_proj/MyTools/log.txt > $log_file_name
awk 'NR>2{print}' /home/pi/Code/Django_proj/MyTools/uwsgi.log > $log_file_name
ln $log_file_name $log_file_name_ln
echo '*********' > /home/pi/Code/Django_proj/MyTools/uwsgi.log

find $logs_root -mtime +14 -name "*.log" -exec rm {} \;
find $logs_root_ln -mtime +14 -name "*.log" -exec rm {} \;
