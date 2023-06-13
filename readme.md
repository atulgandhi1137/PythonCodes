# Cockpit

## Description
 This pipeline streams wifi and in-house related customer data from LG to GCP. This pipeline fetches data from below topics for 8 types of data feeds.
- odhat_pr_connectivity_ch_prd_conncockpit_plume_client_stats
- odhat_pr_connectivity_ch_prd_conncockpit_plume_modem_stats
- odhecx_connect_cockpit_ch_pod_health_metrics_v1
- odhat_pr_various_ch_prd_cockpit_outbound_care_mvp_v1
- odhat_pr_various_ch_prd_plume_pod_inventory_feed_v1
- odhat_pr_various_ch_prd_connect_hist_issues_v1
- odhat_pr_various_ch_prd_coverage_issues_node_v1
- odhat_pr_various_ch_prd_coverage_issues_location_v1
- odhat_pr_various_ch_prd_chronic_issues_device_v1
- odhat_pr_various_ch_prd_chronic_issues_location_v1
- odhat_pr_various_ch_prd_chronic_pod_v1



## Services Used
- Cloud Run
- Pub/Sub
- BigQuery
- Cloud Composer / Airflow
- Secret Manager


## Prerequisites
- Service Account with below permissions for Cloud Run 
   - Editor
   - Secret Manager Secret Accessor
   - PubSub Admin
   - BigQuery Admin
- A VPC connector which ensures the connectivity can be established with ODH Kafka   
- Serverless VPC Access User permission to google managed service account used for cloud run from host project
- Bootstrap servers from LG side ( SSL port is 9097 and without SSL port is 9096 )
  - odh-tenant-proxy-1-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
  - odh-tenant-proxy-2-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
  - odh-tenant-proxy-3-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
  - odh-tenant-proxy-4-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
  - odh-tenant-proxy-5-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
  - odh-tenant-proxy-6-chu-svc2-prod-chu.odh.obo.libgbl.biz:port
- SSL username and password for kafka accessibility

## Pipeline flow

**Cloud Run** - This service utilizes the kafka-python API to retrieve data from ODH Kafka. The data is then processed, specifically extracting the necessary fields, and subsequently published to the PubSub topic. As a final step, it logs the number of processed messages and the time taken on the BigQuery table. (Cockpit.cockpit_log). Here's an example of KafkaConsumer config used to connect to Kafka Cluster
```
kafka_config = {
            'bootstrap_servers': <bootstrap-servers-list>,
            'group_id': 'cockpit',
            'auto_offset_reset': 'earliest',
            'security_protocol': 'SASL_SSL',
            'sasl_mechanism': 'PLAIN',
            'sasl_plain_username': username,
            'sasl_plain_password': password,
            'ssl_check_hostname' : True,
            'api_version' : (2,5,1),
            'consumer_timeout_ms': 120000
            'value_deserializer': lambda v: json.loads(v.decode('utf-8'))
        }
```
In the above config, <br>
- group_id : It will make sure that the consumer reads the messages from last committed message. Also helps to allow multiple consumers to load balance consumption of topics.
- auto_offset_reset : It sets the offest i.e. from which point the consumer should read the messages. (earliest, latest)
- ssl_check_hostname : This is set to False if bootstrap-server-list contains IP instead of hostname.
- consumer_timeout_ms : It sets the timeout for consumer to break out of the loop if there is no message. 


**Pub/Sub** - To ensure efficient data handling, a dedicated Pub/Sub topic is created for each of the 11 feeds. These topics are designed with predefined schemas, ensuring that only relevant fields are included, thus preventing the publication of messages containing unnecessary data. By applying the schema to the topic, any messages that contain fields outside the schema are not published. Furthermore, a BigQuery subscription is established to facilitate the seamless transfer of data to the respective BigQuery tables. Both the topic and subscription have a retention period of 1 day, ensuring data availability within the defined timeframe.
To validate that pubsub is recieving data from cloud run , Please ensure following things are created before hand 

1. Schema - As per requirement 
2. Topic 
3. Subscription - Mapped to the particular topic and BQ table 

**BigQuery** - The BigQuery tables serve as storage for the data being seamlessly transferred from the Pub/Sub topic. They securely store and manage the incoming data, allowing for efficient querying, analysis, and insights generation.


**Airflow** - The Cockpit pipeline is orchestrated and automated through Airflow, ensuring smooth and scheduled execution. The Airflow DAG is set to run on an hourly basis and initiates the consumer process by triggering the Cloud Run URL. This action initiates the necessary steps for processing the data within the pipeline.

## Troubleshooting

### Validating the streaming
1. Navigate to project snr-ebd-dev and open Virtual Instances
2. Check for the instance instance-1 which is connected to LG as it is mapped to kafka
3. Start the instance ssh client and run below command.
```
$ kafkacat -C -b <bootstrap-server> -X security.protocol=SASL_SSL -X sasl.mechanism=PLAIN -X sasl.username=username -X sasl.password=<password> -t <topic_name> 
```
If the messages are streaming then it will start printing messages which means streaming from source is okay else report to source for any kafka related queries.

To check the number of partitions on the topic, all the metadata about topic can be listed using below command
```
$ kafkacat -C -b <bootstrap-server> -L
```

### Validating the message publishing to BigQuery 

1. Open Cloud shell and run below command 
```
$ gcloud pubsub topics publish TOPIC_ID --message=MESSAGE_DATA
```
2. Check the BQ table which is aligned to that topic subscription , if published json data is inserted to BQ then you can say that the pubsub to BQ is working, if not check the subscription push metrics (ex. push_success_count or invalid_argument).


### Steps/Queries to ensure that the streaming is fine and validate the numbers :

Table Name : cockpit_log
1. To validate the number of dag runs, run below query on BigQuery
```
Select topic,count(*) from <project_name>.Cockpit.cockpit_log where date(execution_ts) = '<date>' group by topic
```
2. To check the time every topic is taking on each run
```
Select topic,execution_ts,time_taken,record_count from <project_name>.Cockpit.cockpit_log where topic ='<Topic_name>' and date(execution_ts) = 'Date'
```


