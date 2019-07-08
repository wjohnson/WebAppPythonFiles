# A Simplified Azure Search Project (Like the JFK Files) for 100% Python

A flask app that mimics the functionality of the JFK Files (but with abstracts).

## Getting Started

* Create a Service Principal with Contributor acccess to your subscription.
* Create a file called .env with the below environment variables filled in.
* Create a virutal env `virtualenv env` and activate it `env\Scripts\activate`
* Run `pip install -r requirements.txt`
* Run `python main.py` # Deploys all of the services, downloads data from UCI, and upload to blob 
  * Deploys Azure Search
  * Deploys Cognitive Service Key
  * Deploys Blob Storage Account
  * Deploys App Service Plan and Web App
* Go to your Azure Search Service > Keys > first query key
 

You'll need to set up these environment variables in your .env file.  APP_SERVICE_SITE_NAME, STORAGE_ACCOUNT_NAME, and SEARCH_SERVICE_NAME need to be globally unique so add a few random numbers or letters to them.

    AZURE_CLIENT_ID=
    AZURE_TENANT_ID=
    AZURE_CLIENT_SECRET=
    AZURE_SUBSCRIPTION_ID=
    RESOURCE_GROUP_LOCATION=centralus
    RESOURCE_GROUP_NAME=PythonFiles
    APP_SERVICE_PLAN_NAME=PythonFilesAppSvcPlan
    APP_SERVICE_SITE_NAME=PythonFiles
    STORAGE_ACCOUNT_NAME=pythonfilesblob
    STORAGE_CONTAINER_DATA_NAME=abstracts
    SEARCH_SERVICE_NAME=pythonfilessearchsvc
    SEARCH_DATA_SOURCE_NAME=blobabstractsdatasrc
    SEARCH_INDEXER=blobabstractsindexer
    SEARCH_API_VERSION=2019-05-06`
    SEARCH_QUERY_KEY=****TOBEFILLEDIN****