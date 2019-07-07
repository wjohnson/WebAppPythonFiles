import requests
import json
import _io

class AzureSearchClient():

    def __init__(self, service_name, key, api_version=None):
        self.key = key
        self.service_name = service_name
        self.search_url = "https://{}.search.windows.net".format(self.service_name)
        self.api_version = api_version or "2019-05-06" # Most up-to-date as 20190705
        self.headers = {"Content-Type":"application/json","api-key":key}

    def __generic_create_or_update(self, object_name, schema, object_type):
        """
        :param object_name: Name of the search object to create or update.
        :type object_name: str
        :param schema: The file path or dictionary that contains the schema definition.
        :type schema: str or dict
        :param object_type: Type of the search object to create or update.
        :type object_type: str
        """
        if isinstance(schema, str):
            with open(schema, 'r') as fp:
                schema = json.load(fp)
        
        results = requests.put(
            url=self.search_url+"/{object_type}/{object_name}?api-version={api_version}".format(
                object_type=object_type,
                object_name=object_name,
                api_version=self.api_version
                ),
            headers=self.headers,
            json=schema
        )
        try:
            results.raise_for_status()
        except:
            print(results.content)
            raise

        if results.status_code == 204:
            response = None
        else:
            response = results.json()
        return (results.status_code, response)
    
    def __generic_get(self, object_name, object_type):
        """
        :param object_name: Name of the search object to create or update.
        :type object_name: str
        :param object_type: Type of the search object to create or update.
        :type object_type: str
        """
        results = requests.get(
            url=self.search_url+"/{object_type}/{object_name}?api-version={api_version}".format(
                object_type=object_type,
                object_name=object_name,
                api_version=self.api_version
                ),
            headers=self.headers
        )
        try:
            results.raise_for_status()
        except:
            print(results.content)
            raise

        return (results.status_code, results.json())

    def create_or_update_search_index(self, index_name, index_schema):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/create-index#request-body-syntax

        :param index_name: Name of the search index to create or update.
        :type index_name: str
        :param index_schema: The file path or dictionary that contains the index schema definition.
        :type index_schema: str or dict
        """
        code, results = self.__generic_create_or_update(index_name, index_schema, "indexes")
        
        return (code, results)
        

    def create_or_update_indexer(self, indexer_name, indexer_schema):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/create-indexer#request-syntax

        :param indexer_name: Name of the search indexer to create or update.
        :type indexer_name: str
        :param indexer_schema: The file path or dictionary that contains the indexer schema definition.
        :type indexer_schema: str or dict
        """
        code, results = self.__generic_create_or_update(indexer_name, indexer_schema, "indexers")
        
        return (code, results)


    def create_or_update_datasource(self, datasource_name, datasource_schema):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/create-data-source#request-body-syntax

        :param datasource_name: Name of the data source to create or update.
        :type datasource_name: str
        :param datasource_schema: The file path or dictionary that contains the data source schema definition.
        :type datasource_schema: str or dict
        """
        code, results = self.__generic_create_or_update(datasource_name, datasource_schema, "datasources")
        
        return (code, results)
    
    def create_or_update_skillset(self, skillset_name, skillset_schema):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/create-skillset

        :param skillset_name: Name of the skillset to create or update.
        :type skillset_name: str
        :param skillset_schema: The file path or dictionary that contains the skillset schema definition.
        :type skillset_schema: str or dict
        """
        code, results = self.__generic_create_or_update(skillset_name, skillset_schema, "skillsets")
        
        return (code, results)
    
    def get_search_index(self, index_name):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/get-index

        :param index_name: Name of the search index to create or update.
        :type index_name: str
        """
        code, results = self.__generic_get(index_name, "indexes")
        
        return (code, results)
        

    def get_indexer(self, indexer_name):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/get-indexer

        :param indexer_name: Name of the search indexer to create or update.
        :type indexer_name: str
        """
        code, results = self.__generic_get(indexer_name, "indexers")
        
        return (code, results)


    def get_datasource(self, datasource_name):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/get-data-source

        :param datasource_name: Name of the data source to create or update.
        :type datasource_name: str
        """
        code, results = self.__generic_get(datasource_name, "datasources")
        
        return (code, results)

    def get_skillset(self, skillset_name):
        """
        See more information here: https://docs.microsoft.com/en-us/rest/api/searchservice/get-skillset

        :param skillset_name: Name of the skillset to create or update.
        :type skillset_name: str
        """
        code, results = self.__generic_get(skillset_name, "skillsets")
        
        return (code, results)
    
    def run_indexer(self, indexer_name):
        """
        For more information see: https://docs.microsoft.com/en-us/rest/api/searchservice/run-indexer

        :param indexer_name: Name of the search indexer to run.
        :type indexer_name: str
        """
        results = requests.post(
            url=self.search_url+"/indexers/{index_name}/run?api-version={api_version}".format(
                index_name=indexer_name,
                api_version=self.api_version
                ),
            headers=self.headers
        )
        try:
            results.raise_for_status()
            if results.status_code == 202:
                response = {"status":"success", "message":"An indexing run was successfully queued"}
            else:
                response = results.json()
        except requests.HTTPError:
            if results.status_code == 409:
                response = {"status":"warning", "message":"The indexer is already running"}
            else:
                print(results.content)
                raise
        except json.decoder.JSONDecodeError:
            response = {
                "status":"warning",
                "message": "There was an issue reading the json",
                "status_code": results.status_code
            }

        return (results.status_code, response)
