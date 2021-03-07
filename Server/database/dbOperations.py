import mongoengine
import logging
from datetime import datetime

from mongoengine import (
    register_connection, connect, disconnect, 
    Document, DynamicDocument, EmbeddedDocument, 
    IntField, ListField, StringField, BooleanField, URLField, EmailField, DateTimeField
)
from mongoengine.errors import (
    NotUniqueError,
    InvalidDocumentError,
    LookUpError,
    DoesNotExist,
    MultipleObjectsReturned,
    InvalidQueryError,
    OperationError,
    NotUniqueError,
    BulkWriteError,
    FieldDoesNotExist,
    ValidationError,
    SaveConditionError
 )
from mongoengine.queryset.visitor import Q
from mongoengine.connection import ConnectionFailure

"""
 MongoDB CRUD Operations 
    References: 
        *** https://cheatography.com/amicheletti/cheat-sheets/mongoengine
        *** http://docs.mongoengine.org
        *** https://docs.mongoengine.org/apireference.html
        *** https://github.com/MongoEngine/mongoengine/tree/master/mongoengine 
"""

DB_CONNECTED = 'CONNECTED'
DB_DISCONNECTED = 'DISCONNECTED'
DB_NEW_CONNECTION = 'NEW CONNECTION'
DB_FAILED_CONNECTION = 'FAILED CONNECTION'

class DBOperationsHandler:
    """
    Handles all CRUD Operations on the MongoDB server.
    """

    def __init__(self):
        """
        sets the address of the server, specifies the database to use
        """
        super().__init__()
        self.db_server = 'localhost'
        self.db_port = 27017
        self.db_name = 'cluelite'
        self.db_status = DB_NEW_CONNECTION

    def conn(self, alias=None):
        """
        connects to the specified database and server
        """
        try:
            if alias is None:
                disconnect(alias='default')
            self.connect = connect(db=self.db_name, host=self.db_server, port=self.db_port, alias=alias)
            self.db_status = DB_CONNECTED
            return self.connect
        except ConnectionFailure as e:
            self.db_status =  DB_FAILED_CONNECTION
            logging.fatal("Failed to connect to " + self.db_name)
            raise e
    
    def disconn(self, alias=None):
        """
        disconnects the current sessions from the databse for the associated alias
        """
        try:
            if alias is None:
                alias='default'
            disconnect(alias=alias)
            self.db_status = DB_DISCONNECTED
            return disconnect
        except ConnectionFailure as e:
            logging.fatal("Failed to disconnect "+self.db_name)
            raise e

    def insert_document(self, obj_col, document=None):
        """
        inserts a new document in the database
        """
        try:
            if document is None:
                document = dict()
            document = obj_col(**document)
            document.save()
            return document
        except NotUniqueError as n:
            logging.error("Failed to insert document. Duplicate email.")
            raise n

    def update_document(self, obj_col, update, filter=None):
        """
        updates all documents macthing the specified query from the database
        """
        if filter is None:
            filter = dict()
        document = obj_col.objects(**filter)
        document.update(**update)
        return document

    def get_document(self, obj_col, filter=None):
        """
        returns a document list macthing the specified query from the database
        """
        try:
            if filter is None:
                filter = dict()
            document = obj_col.objects.filter(__raw__=filter)
            #document = obj_col.objects.only('email')  #Return only a specific column form the DB. Opposite is exclude
            return document
        except IndexError as i:
            logging.error("No such item in the document.")
            raise i

    def delete_document(self, obj_col, filter=None):
        """
        deletes all documents macthing the specified query from the database
        """
        if filter is None:
            filter = dict()
        document = obj_col.objects(**filter)
        document.delete()

class Users(Document):
    """
    Users documents to hold user related information: email, username, firstName, and lastName
    """
    email = EmailField(required=True, unique=True, default=None)
    username = StringField(max_length=50, unique=True, required=False, default=None)
    firstName = StringField(max_length=50, required=False, default=None)
    lastName = StringField(max_length=50, required=False, default=None)
    created = DateTimeField(required=True, default=datetime.now())
    updated = DateTimeField(required=False, default=None)
    status = StringField(required=True, default='active')

    meta = {
        "db_alias": "users-db", 
        'collection':'users',
        'auto_create_index': True,
        'index_background': True,
        'indexes': [ #Add #for hashed indexes and $ for text indexes. Note hased indexes do not support multi-key (i.e. arrays) indexes.
            {
                'name': 'properties',
                'fields': ('status', 'created', 'updated')
            },
            {
                'name': 'full_name',
                'fields': ('firstName', 'lastName')
            },
            {
                'name': 'identifiers',
                'fields': ('email', 'username'),
                'unique': True
            }
        ]
    }

class Weapons(DynamicDocument):
    """
    TO_DO: Define layout of the collection
    """
class Characters(Document):
    """
    TO_DO: Define layout of the collection
    """
"""
Testing calls for DBOperationsHandler() and its methods
"""
newDocument = {'updated':datetime.now()}
filter = {'email': 'hatakora@alarm.com'}

object = DBOperationsHandler()
# object.conn('users-db')
# object.disconn('users-db')
# object.insert_document(Users, newDocument)
# object.update_document(Users, newDocument,filter)
# object.get_document(Users, filter)
# object.delete_document(Users, filter)
