# TODO(Project 1): Implement Backend according to the requirements.
"""Creates the backend system for the wiki's specific functions

Adds text files to bucket, handles user login and sign up, returns images, and
sets up the route of the different wiki pages.

Typical usage example:

  backend = Backend()
  user = User()
"""
import os
import json
import pathlib
import io
import base64
from pathlib import Path
from google.cloud import storage
import hashlib


class User:
    """Creates a Class that describes a user interacts with the login an sign-up functionality.

    Attributes:
        username: A string with the username of the user
        password: A string with the password of the user
    """

    def __init__(self, username, password):
        """Inits User instance with username and password."""
        self.username = username
        self.password = password
        self.file_lst = []



class Backend:
    """Creates a Class that describes the functionality of the wikiviewer

    Attributes:
        
    """

    def __init__(self):
        """Inits Backend instance """
        pass

    def get_wiki_page(self, name):  #Danny
        """Gets specific text file chosen from GCS Bucket to dispaly as pages"""
        storage_client = storage.Client()
        bucket = storage_client.bucket("bt-wikiviewer-content")
        blob = bucket.get_blob(name)
        #print("hello", blob)
        with blob.open() as f:
            return f.read()

    def get_all_page_names(self):  #Danny
        """Shows user all available pages that are viewable"""
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("bt-wikiviewer-content")

        blob_name_lst = []

        for blob in blobs:
            if (blob.name.endswith(".txt")):
                blob_name_lst.append(blob.name)

        #print(blob_name_lst)

        return blob_name_lst

    def upload(self, file_uploaded):  #Enrique
        """Allows user to upload a text file into the GCS Bucket"""
        storage_client = storage.Client()
        bucket = storage_client.bucket("bt-wikiviewer-content")
        if (file_uploaded.endswith(".txt")):
            filename = "%s%s" % ('', file_uploaded)
            blob = bucket.blob(filename)
            basedir = os.path.abspath(os.path.dirname(file_uploaded))
            with open(file_uploaded, 'rb') as f:
                blob.upload_from_file(f)
        pass

    def sign_up(self, username, password):  #Asis
        """Allows user to sign up"""
        hashed = hashlib.sha256(password.encode()).hexdigest()

        bucket_name = "bt-wikiviewer-users_passwords"

        storage_client = storage.Client()

        blobs = storage_client.list_blobs(bucket_name)

        for blob in blobs:
            if username == blob.name:
                return None
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(username)
        with blob.open('w') as f:
            f.write(hashed)
        return True

    def sign_in(self, username, password):  #Asis
        """Once the user has an account, they can login using their credentials"""
        hashed = hashlib.sha256(password.encode()).hexdigest()
        bucket_name = "bt-wikiviewer-users_passwords"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            if username == blob.name:
                blob = bucket.get_blob(username)
                with blob.open("r") as f:
                    stored = f.read()
                if stored == hashed:
                    return True

    def get_image(self, image):  #Enrique
        """Encodes image from GCS Bucket in order to view in pages"""
        storage_client = storage.Client()
        bucket = storage_client.bucket("bt-wikiviewer-content")
        blobs = storage_client.list_blobs("bt-wikiviewer-content")
        for blob in blobs:
            if blob.name == image:
                blob = bucket.get_blob(image)
                with blob.open("rb") as f:
                    encoded_string = base64.b64encode(f.read())
                    return encoded_string
        print("Does not exist")
        pass

    def search_keyword(self, keyword): #Asis
        '''Searches through all of the valid articles in the Content bucket for the keyword that was input by the user

        Returns:
            A list of article names (valid) if the keyword is valid. Otherwise, an empty list.
        '''
        bucket_name = "bt-wikiviewer-content"
 
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blobs = storage_client.list_blobs(bucket_name)
        
        valid = []
        for blob in blobs:
            if (blob.name.endswith(".txt")):
                blob = bucket.get_blob(blob.name)
                count = 0
                with blob.open("r") as f:
                    lines = f.readlines()
                    for line in lines:
                        for word in line.split():
                            if word.lower() == keyword.lower() and blob.name not in valid:
                                valid.append(blob.name)
                            else:
                                count += 1
                            if count == 100:
                                break
                        if count == 100:
                            break
        return valid
                
    def get_discussion_post(self,post): #Enrique
        """Gets a specific discussion posts page"""
        storage_client = storage.Client()
        bucket = storage_client.bucket("bt-wikiviewer-discussions")
        blob = bucket.get_blob(post)
        with blob.open() as f:
            return f.read()

    def get_all_discussion_posts(self): #Enrique
        """Shows user all available discussion posts"""
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("bt-wikiviewer-discussions")
        discussion_list = []
        for blob in blobs:
            if (blob.name.endswith(".txt")):
                discussion_list.append(blob.name)
        return discussion_list
    
    def create_discussion(self,file,title,context): #Enrique
        """Creates layout of text file with user inputs"""
        with open(file, 'w') as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n\n")
            f.write("<head>\n")
            f.write("   <head>\n")
            f.write("       <title>Wiki Music Museum</title>\n\n")
            f.write("       <div align = 'center'>\n")
            f.write("           <h1>")
            f.write(title)
            f.write("</h1>\n")
            f.write("       </div>\n\n\n")
            f.write("   <head>\n")
            f.write("</head>\n\n")
            f.write("<body>\n\n")
            f.write("   <div align = 'center'>\n")
            f.write("       <h3>")
            f.write(context)
            f.write("<h3>\n")
            f.write("</body>\n\n")
            f.write("</html>")
            f.write("<style>\n")
            f.write("   body {\n")
            f.write("       background-color: #5FA8B0;")
            f.write("   }")
            f.write("<style>\n")
        pass

    def upload_discussion_post(self, file_uploaded): #Enrique
        """Allows user to upload a text file discussion into the GCS Discussions Bucket"""
        storage_client = storage.Client()
        bucket = storage_client.bucket("bt-wikiviewer-discussions")
        if (file_uploaded.endswith(".txt")):
            filename = "%s%s" % ('', file_uploaded)
            blob = bucket.blob(filename)
            with open(file_uploaded, 'rb') as f:
                blob.upload_from_file(f)
        pass

    def user_exists(self, user):  #Danny
        #checks if user exists within
        bucket_name = "bt-wikiviewer-users_passwords"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            if user == blob.name:
                return True
        return False

    def get_user_pages(self, user): #Danny
        #returns a list of the users pages
        user_list = None

        bucket_name = "bt-wikiviewer-users_passwords"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.get_blob(user)

        with blob.open("r") as f:
            user_String = f.read()
        print("hello", user_list)

        user_list = user_String.split()

        final_pages = user_list[1:]

        return final_pages

    def user_add_file(self, user, file): #Danny

        previous_list = None

        storage_client = storage.Client()
        blobs = storage_client.list_blobs("bt-wikiviewer-content")

        for blob in blobs:
            if file == blob.name:
                return False

        bucket_name = "bt-wikiviewer-users_passwords"
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(bucket_name)

        for blob in blobs:
            if user == blob.name:
                with blob.open("r") as f:
                    previous_list = f.readlines()
                    
                previous_list.append(file)

                data = ' '.join(previous_list)

                with blob.open('w') as f:
                    f.write(data)

        return True