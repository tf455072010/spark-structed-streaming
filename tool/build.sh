pwd_curr=`pwd`
env=$1

if [ -z "$env" ]; then 
    echo ">> 准备打包，不替换配置, 以原有代码发布..."
else
    echo ">> 准备打包，替换配置环境："$env
fi

if [ ! -f $pwd_curr"/tool/build.sh" ]; then
    echo '>> 当前不是项目root目录...'
    exit 0
else
    echo ">> 获取当前路径："$pwd_curr
fi

rm -rf  output
mkdir output
echo ">> 创建打包临时文件夹"
echo ""

echo ">> 复制文件到打包目录"
cp src/main.py output/
cp tool/venv.* output/
cp tool/submit.* output/

mkdir __tmp__
cp -rf src/* __tmp__/
rm -rf __tmp__/main.py

if [ ! -z "$env" ]; then 
    env_string='._build_.'$env
    echo ">> 替换环境配置:"$env_string
    find ./__tmp__ -name '*._build_.'$env -type f|while read file
    do
        new=${file%.*}
        new=${new%.*}
        echo $file, $new
        mv -f $file $new
    done

    find ./__tmp__ -name '*._build_.'$env -type d|while read folder
    do
        new=${folder%.*}
        new=${new%.*}
        echo $folder, $new
        rm -rf $folder
        mv $folder $new
    done
    echo ""
fi

echo ">> 删除无效文件"
find __tmp__ -name '*__pycache__*' -type d -exec rm -rf {} \;
find __tmp__ -name '*.log' -type f -exec rm -rf {} \;
find __tmp__ -name '*.md' -type f -exec rm -rf {} \;
find __tmp__ -name '*._build_.*' -type f -exec rm -rf {} \;
find __tmp__ -name '*._build_.*' -type d -exec rm -rf {} \;

cd __tmp__
mv config/*.conf ../output/
zip -r libs.zip ./*
mv libs.zip ../output
cd $pwd_curr
rm -rf __tmp__

if [ ! -z "$env" ]; then 
    env_string='._build_.'$env
    echo ">> 替换环境配置:"$env_string
    find ./output -name '*._build_.'$env -type f|while read file
    do
        new=${file%.*}
        new=${new%.*}
        echo $file, $new
        mv -f $file $new
    done

    find ./output -name '*._build_.'$env -type d|while read folder
    do
        new=${folder%.*}
        new=${new%.*}
        echo $folder, $new
        rm -rf $folder
        mv $folder $new
    done
    echo ""
fi

find output -name '*__pycache__*' -type d -exec rm -rf {} \;
find output -name '*.log' -type f -exec rm -rf {} \;
find output -name '*.md' -type f -exec rm -rf {} \;
find output -name '*._build_.*' -type f -exec rm -rf {} \;
find output -name '*._build_.*' -type d -exec rm -rf {} \;


if [ ! -z "$env" ]; then 
    env_string='._build_.'$env
    echo ">> 替换环境配置:"$env_string
    find ./output -name '*._build_.'$env -type f|while read file
    do
        new=${file%.*}
        new=${new%.*}
        echo $file, $new
        mv -f $file $new
    done

    find ./output -name '*._build_.'$env -type d|while read folder
    do
        new=${folder%.*}
        new=${new%.*}
        echo $folder, $new
        rm -rf $folder
        mv $folder $new
    done
    echo ""
fi


if [ -z "$env" ]; then 
    env='default'
fi
current=`date "+%Y-%m-%d %H:%M:%S"`
curruser=`whoami`
ipaddrs=`ip addr|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
echo "编译时间: "$current > output/PACKAGE_INFO
echo "编译环境: "$env >> output/PACKAGE_INFO
echo "HOSTNAME: "$(hostname) >> output/PACKAGE_INFO
echo "打包用户："$curruser >> output/PACKAGE_INFO
echo "打包服务器IP："$ipaddrs >> output/PACKAGE_INFO

echo "\n\n============部署打包成功============="
