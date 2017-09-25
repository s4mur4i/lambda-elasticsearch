# -*- coding: utf-8 -*-
import logging
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

logging.basicConfig(level=os.environ.get("LOGLEVEL", os.environ['LOGLEVEL']))
ES_HOST = os.environ['ES_HOST']
REGION = os.environ['REGION']
logging.info(ES_HOST)

auth = BotoAWSRequestsAuth(aws_host=ES_HOST,
                           aws_region=REGION,
                           aws_service='es')

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def index_managment():
    logging.debug("Checking if index needs to be created")
    if es.indices.exists('age', ignore=400):
        logging.debug("Indice for age exists")
    else:
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        res = es.indices.create(index='age', body=request_body)
        logging.debug("response: %s" % res)


def event_to_document(event):
    doc = {"need_check": False, "name": "", "age": 0}
    ## Name has no checks currently
    doc['name'] = event.get('name')

    ## Age need verification
    try:
        doc['age'] = int(event.get('age'))
    except ValueError:
        logging.error("Not int age, setting need_check flag")
        doc["need_check"] = True
    # Always add age to document
    doc['real_age'] = event.get('age')
    return doc


def handler(event, context):
    logging.debug("Started handler")
    document = event_to_document(event=event)

    index_managment()
    ## Es connection ready
    logging.debug("Adding event to Elasticsearch")

    es.index(index='age', doc_type='name-age', body=document)
    logging.debug("Finished handler")
    return document
    # return {name: age}
