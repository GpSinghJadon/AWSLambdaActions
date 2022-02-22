import boto3
import requests

def download_file(url):
    local_filename = f'{func_name}.zip'
    print(func_name, url)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

def publish_new_version(function_arn):
    return client.publish_version(
        FunctionName=function_arn
    )

def update_alias(func_name, version):
    return client.update_alias(
        FunctionName=func_name,
        Name='prod',
        FunctionVersion=version,
        Description='Category Module Release'
    )

def list_alias(arn):
    return client.list_aliases(
        FunctionName=arn
    )
def is_prod_alias_present(aliases):
    for alias in aliases.get('Aliases', []):
        if alias.get('Name', False) == 'prod':
            return True
    return False

def create_alias(arn, alias_name, version):
    return client.create_alias(
    FunctionName=arn,
    Name=alias_name,
    FunctionVersion=version,
    Description='checkpoint Name: Category Module Release'
)

client = boto3.client('lambda')
# response = client.list_functions(
#     MasterRegion='ap-southeast-1',
#     FunctionVersion='ALL',
#     MaxItems=500
# )
# print(response)
import json
# json.dump(response, open('lambdas-list.json', 'r'))
response = json.load(open('lambdas-list.json', 'r'))
# response = json.load(open('/mnt/d/workspace/Pilgrim_app_backend/pythonsctipt/lambdas-list.json', 'r'))

for funct in response['Functions']:
    try:
        func_name = funct['FunctionName']
        print(f"Function name: {func_name}")
        print(f"Publish started for {func_name}")
        func_data = client.get_function(
            FunctionName= func_name
        )
        # loc = func_data['Code']['Location']
        # print(f"Location is: {loc}")
        # download_file(loc)
        published_data = publish_new_version(funct['FunctionArn'])
        version = published_data['Version']
        aliases = list_alias(funct['FunctionArn'])
        if not is_prod_alias_present(aliases):
            create_alias(funct['FunctionArn'], 'prod', version)
        else:
            update_alias(func_name, version)
        print(f"Successfully published {func_name}")

    except Exception as e:
        print(f"{func_name} got into an error")
