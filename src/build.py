import config

app_name = config.APPLICATION_NAME

kill_shell = "yarn application -list|grep " + app_name + \
    "|awk '{print $1}'|xargs yarn application -kill"
with open('../tool/kill.sh', 'w') as config:
    config.write(kill_shell)

submit_shell = '''
if [ ! -f "python3.zip" ]; then
	cd venv
	zip -r python3.zip ./*
	mv python3.zip ..
	cd ..
fi

export HADOOP_USER_NAME=hive
export SPARK_KAFKA_VERSION=0.10

spark2-submit --py-files ./libs.zip \\
        --files ./kafka_client_jaas.conf \\
        --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 \\
        --name ''' + app_name + ''' \\
        --master yarn \\
        --deploy-mode cluster \\
        --driver-memory 1g \\
        --executor-memory 2g \\
        --executor-cores 1 \\
		--num-executors 1 \\
        --archives ./python3.zip#py3 \\
        --driver-java-options -Djava.security.auth.login.config=kafka_client_jaas.conf \\
        --conf spark.executor.extraJavaOptions=-Djava.security.auth.login.config=kafka_client_jaas.conf \\
        --conf spark.pyspark.python=py3/bin/python3 \\
        --conf spark.pyspark.driver.python=py3/bin/python3 \\
        --conf spark.dynamicAllocation.enabled=false \\
        --conf spark.driver.memoryOverhead=1G \\
        --conf spark.executor.memoryOverhead=1G \\
        ./main.py $*
'''

with open('../tool/submit.sh', 'w') as config:
    config.write(submit_shell)
