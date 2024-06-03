# Information Retrival Project

<!-- TOC -->
* [Information Retrival Project](#information-retrival-project)
  * [Folder Structure](#folder-structure)
    * [data_loaders](#data_loaders)
    * [eval](#eval)
    * [offline](#offline-)
    * [pickle_files (ignored from git)](#pickle_files-ignored-from-git)
    * [query_refinement](#query_refinement)
    * [service_registry](#service_registry-)
    * [services](#services)
    * [.env](#env)
    * [constants.py](#constantspy)
    * [.db files](#db-files)
<!-- TOC -->

---
## Folder Structure

### data_loaders
this folder contains files to load the data from datasets and store it in sqlite database , our first dataset files was xml and the second one was json so we have both json & xml loaders.

### eval
this folder contains the evaluation functions for both datasets.

### offline 
this folder contains scripts to build the offline stage of the project like init the tfidf matrix and store it in a pickle file.

### pickle_files (ignored from git)
this folder contains the binary files that used during the project like vectorizer , tfidf matrix , qrels , queries ... , for both data sets.

### query_refinement
this folder contains the files and scripts for the query refinement.

### service_registry 
this folder contains the registry service to serve the SOA, and also contains the service model class.

### services
in this folder we have : 
1. folder for every service in the system contains the service file that run the fastAPI server and another file hold the business logic for that service.
2. `registry_client.py` : file hold the http client that communicate with the server registry to avoid repeating the same code in the services.

### .env
the environment file that contains the ip and port for each service.

### constants.py
this file contains the files paths , some constants variables and some functions that shared cross all the project.

### .db files
sqlite database files that store the data from datasets.
