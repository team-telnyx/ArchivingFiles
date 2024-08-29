import boto3
import requests
import json
import datetime

client = boto3.client('s3')

API_KEY = 'YOU_API_KEY'
BUCKET_NAME = 'YOUR_TELNYX_STORAGE_BUCKET_NAME'
REGION='REGION_FOR_YOUR_BUCKET'
URL=  f'https://{REGION}.telnyxstorage.com'

def get_faxes(page=1):
    date_from = (datetime.datetime.now() + datetime.timedelta(days=-30)).date()
    endpoint = f'https://api.telnyx.com/v2/faxes?filter[created_at][gte]={date_from}T00%3A00%3A00Z&page[number]={page}'
    headers = {'Content-Type': 'application/json',
               'Authorization' : f'Bearer {API_KEY}'}

    return json.loads(requests.get(endpoint, headers = headers).content)


def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)    
        return filename
    else:
        print(f"Failed to download file: {response.status_code}")
        return None

def upload_to_s3(file_name):
    session = boto3.Session(
            aws_access_key_id=API_KEY,
            region_name=REGION,
        )

    client = session.client(
        service_name = "s3",
        endpoint_url = URL,
        use_ssl = True,
        config = boto3.session.Config(signature_version="s3v4"),
    )
    try:
        client.upload_file(file_name, BUCKET_NAME, file_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials")
        return False
    return True

def archive_fax(url, id, preview = False):
    file_name = download_file(url, f"Preview_{id}" if preview else f"Fax_{id}")
    upload_to_s3(file_name)
    os.remove(file_name)

def archive_inbound_fax(fax):
    if('media_url' in fax):
        archive_fax(fax['media_url'], fax['id'])   

def archive_outbound_fax(fax):
    if('stored_media_url' in fax):
        archive_fax(fax['stored_media_url'], fax['id']) 
    if('preview_url' in fax):
        archive_fax(fax['preview_url'], fax['id'], True) 

page_no = 1

while(True):
    response = get_faxes(page_no)
    total_pages = response['meta']['total_pages']

    for fax in response['data']:
        if(fax['direction'] == 'inbound'):
            archive_inbound_fax(fax)
        else:
            archive_outbound_fax(fax)
    if(total_pages >= page_no):
        break
    else:
        page_no = page_no + 1