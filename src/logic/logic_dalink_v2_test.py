from pyspark.sql.functions import get_json_object, lower, regexp_replace
from config import base





def handle(ss,spark):

    # 配置kafka消费参数

    kafka_df = spark.get_structured_streaming_kafka(
        bootstrap_servers=base.KAFKA_SUBSCRIBE_BOOTSTRAP_SERVERS,
        topic=base.KAFKA_DATALINK_V2_TOPIC,
        max_offsets_per_trigger=base.KAFKA_MAX_OFFSETS_PER_TRIGGER,
        security_protocol=base.KAFKA_SUBSCRIBE_SECURITY_PROTOCOL,
        sasl_mechanism=base.KAFKA_SUBSCRIBE_SASL_MECHANISM
    ).load()

    df_middle = origin_handle(kafka_df)
    df_middle.printSchema()
    df_middle.createOrReplaceTempView('datalink_v2_test')
    df = normal_handle(ss)
    df.printSchema()

    # 写入临时目录
    df.writeStream \
        .format("orc") \
        .option("path", "/user/hive/warehouse/stag.db/kafka_datalink_v2_streaming_test") \
        .option("checkpointLocation", "/user/hive/spark_offset/kafka_datalink_v2_streaming_test") \
        .trigger(processingTime='15 seconds') \
        .outputMode("append").start()




def origin_handle(kafka_df):
    '''
    解析源数据

    '''
    source_df = kafka_df.select(
        lower(kafka_df.value.cast("string")).alias("kafka_value"),
        kafka_df.offset.cast("bigint").alias("kafka_offset"),
        kafka_df.partition.cast("bigint").alias("kafka_partition"),
        kafka_df.timestamp.cast("bigint").alias("kafka_timestamp"),
        kafka_df.topic.cast("string").alias("kafka_topic")
    )

    df_middle = source_df.select(
        get_json_object(source_df.kafka_value, "$.callerid").cast(
            "bigint").alias("caller_id"),
        get_json_object(source_df.kafka_value, "$.callertype").cast(
            "bigint").alias("caller_type"),
        get_json_object(source_df.kafka_value, "$.sdkvers").cast(
            "string").alias("dlsdk_vers"),
        get_json_object(source_df.kafka_value, "$.sdkuuid").cast(
            "string").alias("dlsdk_uuid"),
        get_json_object(source_df.kafka_value, "$.protocolvers").cast(
            "string").alias("dlprotocol_vers"),
        get_json_object(source_df.kafka_value, "$.harddetails").cast(
            "string").alias("hard_details"),
        get_json_object(source_df.kafka_value, "$.area").cast(
            "string").alias("area"),
        get_json_object(source_df.kafka_value, "$.manufacturer").cast(
            "string").alias("manufacturer"),
        get_json_object(source_df.kafka_value, "$.devicename").cast(
            "string").alias("device_name"),
        get_json_object(source_df.kafka_value, "$.ostypeid").cast(
            "bigint").alias("os_type_id"),
        get_json_object(source_df.kafka_value, "$.osname").cast(
            "string").alias("os_name"),
        get_json_object(source_df.kafka_value, "$.networkstandard").cast(
            "bigint").alias("network_type_id"),
        get_json_object(source_df.kafka_value, "$.resolutionw").cast(
            "bigint").alias("screen_width"),
        get_json_object(source_df.kafka_value, "$.resolutionh").cast(
            "bigint").alias("screen_height"),
        get_json_object(source_df.kafka_value, "$.carrier").cast(
            "bigint").alias("carrier"),
        get_json_object(source_df.kafka_value, "$.sign").cast(
            "string").alias("sign"),
        get_json_object(source_df.kafka_value, "$.datalist").cast(
            "string").alias("datalist"),
        source_df.kafka_value.cast("string").alias("message_content"),
        "kafka_offset",
        "kafka_partition",
        "kafka_timestamp",
        "kafka_topic"
    )

    # df = df_middle.select(
    #     regexp_replace(regexp_replace(regexp_replace("datalist", "\\[\\{", "\\{"), "\\}]", "\\}"), "\\}\\,\\{",
    #                    "\\}\\#\\v\\#\\{").alias('datalist'),
    #     # regexp_replace(regexp_replace(regexp_replace("hard_details",'\\[',''),'\\]',''),'\\"','').alias("hard_details"),
    #     "hard_details",
    #     "caller_id",
    #     "caller_type",
    #     "dlsdk_vers",
    #     "dlsdk_uuid",
    #     "dlprotocol_vers",
    #     "area",
    #     "manufacturer",
    #     "device_name",
    #     "os_type_id",
    #     "os_name",
    #     "network_type_id",
    #     "screen_width",
    #     "screen_height",
    #     "carrier",
    #     "sign",
    #     "message_content",
    #     "kafka_offset",
    #     "kafka_partition",
    #     "kafka_timestamp",
    #     "kafka_topic"
    # )

    return  df_middle


def normal_handle(ss):

    query = '''
    select
        caller_id,
        caller_type,
        dlsdk_vers,
        dlsdk_uuid,
        dlprotocol_vers,
        hard_details,
        area,
        manufacturer,
        device_name,
        os_type_id,
        os_name,
        network_type_id,
        screen_width,
        screen_height,
        carrier,
        sign,
        msg_uuid,
        app_session_id,
        event_code,
        event_idx,
        from_event_code,
        from_msg_uuid,
        event_start_ts,
        event_end_ts,
        status_code,
        domain,
        client_event_code,
        app_id,
        app_code,
        app_vers,
        from_app_vers,
        sgame_id,
        game_id,
        game_code,
        game_vers,
        channel_id,
        pf_vers,
        request_data,
        response_data,
        uri,
        ip_addr,
        area_info[0] as province_code,
        area_info[1] as province_name,
        area_info[2] as city_code,
        area_info[3] as city_name,
        area_info[4] as district_code,
        area_info[5] as district_name,
        content,
        uid,
        room_no,
        group_id,
        package_type_id,
        duration_on_backgroud,
        extend_str_1,extend_str_2,extend_str_3,extend_str_4,extend_str_5,
        extend_num_1,
        extend_num_2,
        extend_num_3,
        extend_num_4,
        extend_num_5,
        cast(unix_timestamp() as bigint) * 1000 as hive_unix,
        kafka_offset,
        kafka_partition,
        kafka_timestamp,
        kafka_topic,
        message_content
    from
        (select
            caller_id,
            caller_type,
            dlsdk_vers,
            dlsdk_uuid,
            dlprotocol_vers,
            split(str2arr(hard_details),',') as hard_details,
            area,
            manufacturer,
            device_name,
            os_type_id,
            os_name,
            network_type_id,
            screen_width,
            screen_height,
            carrier,
            sign,
            msg_uuid,
            app_session_id,
            event_code,
            cast(event_idx as bigint) event_idx,
            from_event_code,
            from_msg_uuid,
            cast(event_start_ts as bigint) event_start_ts,
            cast(event_end_ts as bigint) event_end_ts,
            cast(status_code as bigint) status_code,
            cast(domain as bigint) domain,
            client_event_code,
            cast(app_id as bigint) app_id,
            app_code,
            app_vers,
            from_app_vers,
            cast(sgame_id as bigint) sgame_id,
            cast(game_id as bigint) game_id,
            game_code,
            game_vers,
            cast(channel_id as bigint) channel_id,
            pf_vers,
            request_data,
            response_data,
            uri,
            cast(ip_addr as string) ip_addr,
            case when is_ipv4_udf(cast(ip_addr as string))=true then analysis_area_udf(area,cast(group_id as int),ip_addr,"")
                when is_ipv6_udf(cast(ip_addr as string))=true then analysis_area_udf(area,cast(group_id as int),"",ip_addr)
                else null
                end area_info,
            content,
            cast(uid as bigint) uid,
            cast(room_no as bigint) room_no,
            cast(group_id as bigint) group_id,
            cast(package_type_id as bigint) package_type_id,
            cast(duration_on_backgroud as bigint) duration_on_backgroud,
            extend_str_1,extend_str_2,extend_str_3,extend_str_4,extend_str_5,
            cast(extend_num_1 as bigint) extend_num_1,
            cast(extend_num_2 as bigint) extend_num_2,
            cast(extend_num_3 as bigint) extend_num_3,
            cast(extend_num_4 as bigint) extend_num_4,
            cast(extend_num_5 as bigint) extend_num_5,
            kafka_offset,
            kafka_partition,
            kafka_timestamp,
            kafka_topic,
            message_content
        from 
            datalink_v2_test
            LATERAL VIEW explode(split(str2arr(datalist),',')) mytable as nu
            LATERAL VIEW json_tuple(mytable.nu,'msguuid','appsessionid','eventcode','eventindex','fromeventcode','frommsguuid','eventbegints','eventendts','statuscode',
            'domain','clienteventcode','appid','appcode','appversion','fromappversion','sgameid','gameid','gamecode','gameversion','channelid','platformversion',
            'requestdata','responsedata','uri','clientip','content','userid','roomno','groupid','packagetypeid','extraduration','extendstr1','extendstr2','extendstr3',
            'extendstr4','extendstr5','extendnum1','extendnum2','extendnum3','extendnum4','extendnum5')table1 as
             msg_uuid,app_session_id,event_code,event_idx,from_event_code,from_msg_uuid,event_start_ts,event_end_ts,status_code,domain,client_event_code,app_id,app_code,
             app_vers,from_app_vers,sgame_id,game_id,game_code,game_vers,channel_id,pf_vers,request_data,response_data,uri,ip_addr,content,uid,room_no,group_id,package_type_id,
             duration_on_backgroud,extend_str_1,extend_str_2,extend_str_3,extend_str_4,extend_str_5,extend_num_1,extend_num_2,extend_num_3,extend_num_4,extend_num_5
        ) tmp
    
    '''

    df = ss.sql(query)
    return df

