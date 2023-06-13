# STB

## Description
 This pipeline involves fetching data from ODH Kafka, performing transformations using Cloud Run, and subsequently publishing the transformed data to a PubSub topic.  Finally, the data is seamlessly propagated from PubSub to a required BigQuery table using BigQuery subscription.

## Services Used
- Cloud Run
- Pub/Sub
- BigQuery
- Cloud Composer / Airflow


## Prerequisites
- Service Account with below permissions for Cloud Run 
   - Editor
   - Secret Manager Secret Accessor
   - PubSub Admin
- A VPC connector which ensures the connectivity can be established with ODH Kafka   

## Pipeline flow

**Cloud Run** - This function fetches the data from ODH Kafka using a KafkaConsumer(kafka-python API). This consumer seamlessly manages server failures within the Kafka cluster, adjusting as topic-partitions are created or migrated between brokers. Additionally, it collaborates with the assigned Kafka Group Coordinator node to facilitate load balancing among multiple consumers for topic consumption. After the consumption, the messages are transformed in order to filter out the desired fields/columns and published to pubsub topic. This function runs 5 different processes in order to assign consumers to all 5 partitions and avoid group rebalancing.  Here's an example of KafkaConsumer config 
```
kafka_config = {
            'bootstrap_servers': <bootstrap-servers-list>,
            'group_id': 'gcp',
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




**Pub/Sub** - A Pub/Sub topic is created with a predefined schema to ensure that only messages containing the expected fields/columns are allowed for publishing. Additionally, a BigQuery subscription is created to efficiently transfer the received messages from the topic to the desired BigQuery table. Both the topic and the subscription have a retention period of 1 day, meaning that messages are retained for that duration. Once the message is published to the Pub/Sub topic from Cloud Run, it is immediately pushed to the corresponding BigQuery table.



**BigQuery** - The BigQuery table holds the complete data that is being pushed from pubsub topic.




**Airflow** - This automated pipeline is implemented using Airflow, leveraging a DAG (Directed Acyclic Graph) with a BashOperator to trigger the Cloud Run URL. This action initiates the consumption process, which retrieves data from the ODH Kafka. The Airflow DAG is scheduled to execute daily at 8 am CEST, ensuring regular data processing. Additionally, email notifications are enabled to promptly alert stakeholders about any failures occurring within the pipeline, enabling swift resolution. 



