pwd_curr=`pwd`

if [ ! -f $pwd_curr"/tool/build.sh" ]; then
    echo '>> 当前不是项目root目录...'
    exit 0
else
    echo ">> 获取当前路径："$pwd_curr
fi

rm -rf  output

echo ">> 删除无效文件"
find src -name '*__pycache__*' -type d -exec rm -rf {} \;
find src -name '*.log' -type f -exec rm -rf {} \;

echo "\n\n============清理完成============="
