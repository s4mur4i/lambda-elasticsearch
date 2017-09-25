# Scalability

## Lambda

Scaling is dependent on aws settings according to throttle limits

## Elasticsearch

Depending on forecasted load shard and replica count can be increased and adjusted to
forcasted data amount. 

## Production readiness

Not really, to improve following points would be needed

- validate input better
- handle ES outage better in connection buildup or request error handling
- harden ES reachability to smaller scope
- IAM scope for needed privilages only
- Provide event source like apigateway or dynamodb, etc.
- better sharding for the indice
- move lambda deployment to s3 (more reliable)
- for lambda deployment use alias or tags

# How to run

I tested and used the deployment on a Mac 10.12.6
AWS cli was installed and used with 
```
aws configure
```
run first to use a master account for deployment.
Then from project root folder run 
```
./deploy.sh
```

To fire off the events:
```
aws lambda invoke

```

# Local dev

Just some points for me during development

#### Local Elasticsearch dev

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.host=0.0.0.0" docker.elastic.co/elasticsearch/elasticsearch:5.6.1
```
#### Dev Running

```
source /usr/local/bin/virtualenvwrapper.sh 
mkvirtualenv pylambda
pip install python-lambda
lambda init
lambda invoke -v --event-file=event3.json
```
