pwd_curr=`pwd`

if [ ! -f $pwd_curr"/tool/ctutil.up.sh" ]; then
    echo '>> 当前不是项目root目录...'
    exit 0
else
    echo ">> 获取当前路径："$pwd_curr
fi

sys_info=`lsb_release -a`
if [ "`echo $sys_info | grep Ubuntu`" != "" ]; then
    echo '>> 识别到当前为Ubuntu系统...'
    echo "PS:请确保系统中已经wget和unzip，如果没有，请执行sudo apt-get install wget unzip -y"
elif [ "`echo $sys_info | grep CentOS`" != "" ]; then
    echo '>> 识别到当前为CentOS系统...'
    echo "PS:请确保系统中已经wget和unzip，如果没有，请执行yum install wget unzip -y"
else
    echo '>> 不能识别系统，操作终止...'
    exit 0
fi

echo ""

rm -rf *.zip
wget http://autoscripts.tcy365.net:32639/pyproj/ctutil/spark.zip -O __temp__ctutil__.zip -o /dev/null

rm -rf src/ctutil
unzip __temp__ctutil__.zip -d src
rm -rf *.zip

if [ -d $pwd_curr"/src/ctutil" ]; then
    echo '>> 更新成功....'
else
    echo '>> 更新失败...'
fi

