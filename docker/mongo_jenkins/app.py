from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = MongoClient(self.host, self.port, username=self.username, password=self.password)
        return self.client

    def close(self):
        if self.client:
            self.client.close()

    def drop_database(self, database_name):
        if self.client:
            self.client.drop_database(database_name)
            print(f"Database '{database_name}' dropped.")


class DocumentHandler:
    def __init__(self, connection, database_name, collection_name):
        self.connection = connection
        self.database_name = database_name
        self.collection_name = collection_name
        self.collection = None

    def connect_to_collection(self):
        db = self.connection.connect()[self.database_name]
        self.collection = db[self.collection_name]

    def insert_document(self, document):
        if not self.collection:
            self.connect_to_collection()
        insert_result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {insert_result.inserted_id}")


class StudentHandler(DocumentHandler):
    def __init__(self, connection, database_name, collection_name, students_data):
        super().__init__(connection, database_name, collection_name)
        self.students_data = students_data

    def insert_students(self):
        if not self.collection:
            self.connect_to_collection()
        result = self.collection.insert_many(self.students_data)
        print(f"Inserted {len(result.inserted_ids)} students into the collection.")

    def print_students(self):
        students = self.collection.find()
        print("Students in the collection:")
        for student in students:
            print(student)


class CollectionFinder:
    def __init__(self, connection, database_name):
        self.connection = connection
        self.database_name = database_name

    def find_collection_by_name(self, collection_name):
        db = self.connection.connect()[self.database_name]
        collections = db.list_collection_names()

        if collection_name in collections:
            print(f"Collection '{collection_name}' found in the database '{self.database_name}'.")
        else:
            print(f"Collection '{collection_name}' not found in the database '{self.database_name}'.")


# Usage
mongo_connection = MongoDBConnection(username='admin', password='password')

# # Add a document
document_handler = DocumentHandler(mongo_connection, 'demo', 'devops_students')
document_handler.insert_document({"name": "Alice", "age": 25, "city": "London"})

#
# # Add students
# students_data = [
#     {"name": "John Doe", "age": 20, "course": "Computer Science"},
#     {"name": "Jane Smith", "age": 22, "course": "Mathematics"},
#     {"name": "Bob Johnson", "age": 21, "course": "Physics"},
# ]
# student_handler = StudentHandler(mongo_connection, 'university', 'students', students_data)
# student_handler.insert_students()
# student_handler.print_students()
#
# Find a collection by name
collection_finder = CollectionFinder(mongo_connection, 'demo')
collection_finder.find_collection_by_name('devops_students')
# Drop the database (for clearing all data)
# mongo_connection.drop_database('mydatabase')
# mongo_connection.drop_database('university')
# Close the connection
mongo_connection.close()
