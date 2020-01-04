host="192.168.101.205"
port=3766
passwd="spwz5che"
remote_folder=`hostname`     

echo '>> 上传代码到远端...'
sshpass -p $passwd ssh root@$host -p$port 'rm -rf /tmp/spark_'$remote_folder' && mkdir /tmp/spark_'$remote_folder
sshpass -p $passwd scp -P $port tool/kill.sh root@$host:/tmp/spark_$remote_folder/

echo '>> 远程执行...'
sshpass -p $passwd ssh root@$host -p$port 'source /etc/profile && cd /tmp/spark_'$remote_folder' && sh kill.sh'