datetime=`date '+%Y-%m-%d %H:%M:%S'`

date=${datetime:0:10}
time=${datetime:11:8}
datetime=$date'~'$time

backup_root='/home/pi/Code/Django_proj/MyTools/Daily/backups/'
backup_root_ln='/home/pi/backups_ln/'
bak_file_name=$backup_root$datetime".sql"
bak_file_name_ln=$backup_root_ln$datetime".sql"

# echo $date  # 2021/12/06
# echo $time  # 17:42:03
# echo $datetime  # 2021/12/06-17:42:03
# echo $bak_file_name  # /home/pi/Code/Django_proj/MyTools/backups/2021-12-06~17:46:27.sql

mysqldump -uroot -pGuoHT990520#2 ToolsBoxPi > $bak_file_name
ln $bak_file_name $bak_file_name_ln

find $backup_root -mtime +5 -name "*.sql" -exec rm -rf {} \;
find $backup_root_ln -mtime +5 -name "*.sql" -exec rm -rf {} \;
