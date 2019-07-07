import os
import json
import random
import argparse
# For creating resource group and credentials
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials
# Azure Web Apps Management
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import AppServicePlan, SkuDescription, Site, SiteConfig
# Azure Storage Management
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku
from azure.mgmt.storage.models import Sku as StorageSku
# Azure Search Management
from azure.mgmt.search import SearchManagementClient
from azure.mgmt.search.models import SearchService, Sku as SearchSku
# Azure Cognitive Services
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Sku as CogSvcsSku, 
    CognitiveServicesAccount, 
    CognitiveServicesAccountCreateParameters
)

# Azure Search Client (Custom)
from setup import search
# For File Download and Unzip
import zipfile
import urllib.request
# For Blob Upload
from azure.storage.blob import BlockBlobService

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-download",action="store_true")
    parser.add_argument("--skip-upload",action="store_true")
    args = parser.parse_args()
        
    # Load Environment Variables from File
    with open('.env', 'r') as envs:
        for row in envs.readlines():
            k,v = row.strip('\n').split('=',1)
            os.environ[k] = v

    # Shared variables
    rg_location = os.environ.get("RESOURCE_GROUP_LOCATION", "centralus")
    app_svc_plan_name = os.environ.get("APP_SERVICE_PLAN_NAME", "PythonFilesAppSvcPlan")
    rg_name = os.environ.get("RESOURCE_GROUP_NAME","PythonFiles")
    site_name = os.environ.get("APP_SERVICE_SITE_NAME", 
        ''.join(["PythonFiles", str(random.randint(0,100000))])
    )
    subscription_id = os.environ.get(
        "AZURE_SUBSCRIPTION_ID", "11111111-1111-1111-1111-111111111111"
    )
    storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME",
        ''.join(["PythonFilesStorage", str(random.randint(0,100000))])
    )
    search_service_name = os.environ.get("SEARCH_SERVICE_NAME",
        ''.join(["PythonFilesSearchSvc", str(random.randint(0,100000))]).lower()
    )
    blob_container = os.environ.get("STORAGE_CONTAINER_DATA_NAME", "abstracts")
    search_index_name = os.environ.get("SEARCH_INDEX_NAME", "abstracts")
    search_data_source_name = os.environ.get("SEARCH_DATA_SOURCE_NAME","pyblobdata")
    search_indexer_name = os.environ.get("SEARCH_INDEXER","pyindexer")
    search_skillet_name = os.environ.get("SEARCH_SKILLSET","pyskills")
    cog_service_name = os.environ.get("COGNITIVE_SERVICE_NAME", "PythonFilesCogSvc")

    # Create a Resource Group
    ## Set up credentials
    credentials = ServicePrincipalCredentials(
        client_id=os.environ["AZURE_CLIENT_ID"],
        secret=os.environ["AZURE_CLIENT_SECRET"],
        tenant=os.environ["AZURE_TENANT_ID"]
    )

    ARMClient = ResourceManagementClient(credentials, subscription_id)
    activity_create_rg = ARMClient.resource_groups.create_or_update(
        resource_group_name=rg_name, 
        parameters={"location": rg_location}
    )
    print("Resource Group ID: {}".format(activity_create_rg.id))

    # Create an App Service Plan
    web_client = WebSiteManagementClient(credentials, subscription_id)

    service_plan_async_operation = web_client.app_service_plans.create_or_update(
        resource_group_name = rg_name,
        name = app_svc_plan_name,
        app_service_plan = AppServicePlan(
            kind="linux",
            location=rg_location,
            reserved=True, # Without this set, it acts like a Windows App Service Plan
            sku=SkuDescription(
                name='P1v2',
                capacity=1,
                tier='Standard'
            )
        )
    )
    service_plan = service_plan_async_operation.result()
    print("Service Plan ID: {}".format(service_plan.id))

    # Create a Python Web App
    site_async_operation = web_client.web_apps.create_or_update(
        resource_group_name = rg_name,
        name = site_name,
        site_envelope = Site(
            location=rg_location,
            server_farm_id=service_plan.id,
            site_config=SiteConfig(
                python_version="3.7",
                linux_fx_version="PYTHON|3.7",
                app_command_line="startup.txt",
                scm_type="LocalGit"
            )
        )
    )
    site = site_async_operation.result()
    print("Site ID: {}".format(site.id))

    # Create an Azure Blob Storage Account
    storage_client = StorageManagementClient(credentials, subscription_id)
    storage_async_operation = storage_client.storage_accounts.create(
        rg_name,
        storage_account_name,
        StorageAccountCreateParameters(
            sku=StorageSku(name="standard_lrs"),
            kind="StorageV2",
            location=rg_location
        )
    )
    storage_account = storage_async_operation.result()

    storage_keys = storage_client.storage_accounts.list_keys(
        resource_group_name=rg_name,
        account_name=storage_account_name
    )
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    storage_primary_key = storage_keys['key1']
    storage_connection_string = "DefaultEndpointsProtocol=https;AccountName={name};AccountKey={key};EndpointSuffix=core.windows.net".format(
        name=storage_account_name,
        key=storage_primary_key
    )
    
    print("Storage Account ID: {}".format(storage_account.id))

    # Create an Azure Search Service
    search_mgmt_client = SearchManagementClient(credentials, subscription_id)
    search_async_operation = search_mgmt_client.services.create_or_update(
        resource_group_name=rg_name,
        search_service_name=search_service_name,
        service = SearchService(
            location=rg_location,
            sku=SearchSku(name="basic")
        )
    )
    search_async_results = search_async_operation.result()
    search_admin_key = search_mgmt_client.admin_keys.get(
        resource_group_name=rg_name,
        search_service_name=search_async_results.name
        ).primary_key

    print("Azure Search ID: {}".format(search_async_results.id))
    print("Azure Search Primary Key: {}".format(search_admin_key))

    # Create an Azure Cognitive Services Key
    # Create an Azure Cognitive Services Key
    cog_svcs_client = CognitiveServicesManagementClient(credentials, subscription_id)

    cog_svc_request = cog_svcs_client.accounts.create(
        resource_group_name=rg_name,
        account_name=cog_service_name,
        parameters=CognitiveServicesAccountCreateParameters(
            sku=CogSvcsSku(name="S0"),
            kind="CognitiveServices",
            location=rg_location, 
            properties = {},
        )
    )

    cog_primary_key = cog_svcs_client.accounts.list_keys(
        resource_group_name=rg_name,
        account_name=cog_svc_request.name
    ).key1

    print("Successfully created all necessary resources!")

    # Download data from UCI Machine Learning Repo
    if args.skip_download:
        print("Skipped download of abstract files")
    else:
        print("Downloading Abstracts... this operation may take a while")
        download = urllib.request.urlretrieve(
            "http://archive.ics.uci.edu/ml/machine-learning-databases/nsfabs-mld/Part1.zip",
            "./abstracts_part1.zip"
        )
        with zipfile.ZipFile("./abstracts_part1.zip","r") as zip_ref:
            zip_ref.extractall("./nsfabs")
        print("Completed Download and Extraction")
    
    # Move data into Blob Storage Account
    blob_client = BlockBlobService(
        account_name = storage_account_name,
        account_key = storage_primary_key
    )
    
    
    blob_client.create_container(
        container_name=blob_container
    )
    print("Successfully created {cont} blob container".format(cont=blob_container))
    if args.skip_upload:
        print("Skipped upload of abstract files")
    else:
        print("Uploading a subset of files downloaded... this operation may take a while")
        for root, _, files in os.walk("./nsfabs/Part1/awards_1990/awd_1990_00"):
            for f in files:
                file_path = os.path.join(root, f)
                
                blob_client.create_blob_from_path(
                    container_name=blob_container,
                    blob_name=file_path[2:],
                    file_path=file_path
                )
        print("Successfully uploaded abstract files to abstracts blob container")

    # Azure Search 
    print("Beginning creation of Azure Search Objects")
    ## Load Schemas and Modify them with keys and env variables
    with open('./setup/searchschema/index.json', 'r') as fp:
        schema_index=json.load(fp)
        schema_index["name"] = search_index_name
    with open('./setup/searchschema/datasource.json', 'r') as fp:
        schema_datasource=json.load(fp)
        schema_datasource["name"] = search_data_source_name
        schema_datasource["container"]["name"] = blob_container
        schema_datasource["credentials"]["connectionString"] = storage_connection_string
    with open('./setup/searchschema/indexer.json', 'r') as fp:
        schema_indexer=json.load(fp)
        schema_indexer["name"] = search_indexer_name
        schema_indexer["dataSourceName"] = search_data_source_name
        schema_indexer["skillsetName"] = search_skillet_name
        schema_indexer["targetIndexName"] = search_index_name
    with open('./setup/searchschema/skillset.json', 'r') as fp:
        schema_skillset=json.load(fp)
        schema_skillset["name"] = search_skillet_name
        schema_skillset["cognitiveServices"]["description"] = "/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{cog_svc}".format(
            subscription_id=subscription_id,
            resource_group=rg_name,
            cog_svc=cog_service_name
        )
        schema_skillset["cognitiveServices"]["key"] = cog_primary_key

    # Create an Azure Search Index
    search_service_client = search.AzureSearchClient(
        service_name=search_service_name,
        key=search_admin_key
    )

    _,index_results = search_service_client.create_or_update_search_index(
        index_name=search_index_name,
        index_schema=schema_index
    )
    print("Succeeded Created Index")

    # Create an Azure Search Data Source
    _,datasource_results = search_service_client.create_or_update_datasource(
        datasource_name=search_data_source_name,
        datasource_schema=schema_datasource
    )
    print("Succeeded Created Data Source")
    # Create an Azure Search Skillset
    _,skillset_results = search_service_client.create_or_update_skillset(
        skillset_name=search_skillet_name,
        skillset_schema=schema_skillset
    )
    print("Succeeded Created Skillset")
    # Create an Azure Search Indexer
    _,indexer_results = search_service_client.create_or_update_indexer(
        indexer_name=search_indexer_name,
        indexer_schema=schema_indexer
    )
    print("Succeeded Created Indexer")
    # Run Azure Search Indexer

    _,indexer_run_results = search_service_client.run_indexer(
        indexer_name=search_indexer_name
    )
    print(json.dumps(indexer_run_results, indent=2))
    print("Queued Indexer Run.  This operation may take awhile to complete.")