from pymongo import MongoClient
import json
import utils


class MongoConnection:
    """
    A helper class to handle easy functionality of MongoDB
    """

    def get_database(self):
        """
        Get the current database you're at
        :return:
        """
        return self.db

    def get_collection(self):
        """
        Get the current collection you're at
        :return:
        """
        return self.collection

    def set_database(self, database):
        """
        Set the database you want to
        :param database: Name of the database
        :return:
        """
        self.db = self.client[database]

    def set_collection(self, collection):
        """
        Set the collection you want to
        :param collection: Name of the collection
        :return:
        """
        self.collection = self.db[collection]

    def load_creds(self, creds_path):
        """
        Load the spotify credentials
        :param creds_path: path to the credentials
        :return:
        """
        self.creds = utils.load_json_data(creds_path)
        print('MongoDB User credentials has been loaded')

    def connect(self, cluster_url=None):
        """
        Initiate the connection required
        :param cluster_url: You can give the custom url but it has to be with the credentials
        :return:
        """
        if cluster_url is None:
            cluster_url = f"mongodb+srv://{self.creds.get('username')}:{self.creds.get('password')}" \
                          f"@spotify-cluster.lixsh.mongodb.net/admin"
        client = MongoClient(cluster_url)
        print('Database names: %s' % client.list_database_names())
        self.client = client
        print('Connection to cluster has been created')

    def create_database(self, database_name):
        self.db = self.client[database_name]
        return self.db

    def create_collection(self, collection_name):
        self.collection = self.db[collection_name]
        return self.collection

    def insert_one_document(self, document):
        """
        Inserts one document into the db
        :param document: document you want to insert
        :return:
        """
        self.collection.insert_one(document)

    def insert_many_documents(self, documents):
        """
        Insert multiple documents at once
        :param documents: The documents you would want to insert
        :return:
        """
        self.collection.insert_many(documents)

