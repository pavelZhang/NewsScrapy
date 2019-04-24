from elasticsearch import Elasticsearch
from myScrapy.settings import elasticsearch_config


class ESUtils(object):

    def __init__(self, host='localhost', port='9200', user='', password=''):
        if elasticsearch_config:
            host = elasticsearch_config.get('host', host)
            port = elasticsearch_config.get('port', port)
            user = elasticsearch_config.get('user', user)
            password = elasticsearch_config.get('host', password)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.es = None

    def connect(self):
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port}],
                                http_auth=(self.user, self.password))
        return self.es


"""
    def count(self, indexname):
        '''
        count index numbers
        '''
        return self.es.count(index=indexname)
    
    def index(self, indexname, doc_type, body, id=None):
        '''
        create new document
        '''
        return  self.es.index(indexname, doc_type, body, id)

    def delete(self, indexname, doc_type, id):
        '''
        delete one document
        '''
        self.es.delete(index=indexname, doc_type=doc_type, id=id)

    def update(self, indexname, doc_type, id, body):
        '''
        update one document
        '''
        return self.es.update(indexname, doc_type, id, body)

    def get(self, indexname, doc_type, id):
        return self.es.get(indexname, doc_type, id)

    def search(self, indexname, size=10):
        try:
            #return self.es.search(index=indexname, size=size, sort="@timestamp:desc")
            return self.es.search(index=indexname, size=size, sort="_score:desc")
        except Exception as e:
            print(e)
"""
