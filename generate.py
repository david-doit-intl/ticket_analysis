from google.cloud import storage
from datetime import date
import requests
import os
import json

cookies = dict({cookie.split("=")[0]:cookie.split("=")[1] for cookie in os.environ["COOKIE"].split(";")})
bucket_name = os.environ["BUCKET"]

def fetch(api, page_num=1):
  return get(f'https://doitintl.zendesk.com/api/v2/{api}.json?page={page_num}', cookies, page_num)

def get(uri, cookies, page_num):
  response = requests.get(uri, cookies=cookies)
  while response.status_code != 200:
    if response.status_code == 429:
      print('Rate limited! Please wait.')
      time.sleep(int(response.headers['retry-after']))
      continue
    else:
      print('Error with status code {}'.format(response.status_code))
      exit()
  return response.json()

def extract_all(current_api, current_api_data, counter=1): 
  current_page = fetch(current_api, counter)
  current_api_data.extend(current_page[current_api])
  if current_page.get('next_page', None) != None:
    counter += 1
    extract_all(current_api, current_api_data, counter)

def write_json_file(current_api):
  current_api_data = []
  extract_all(current_api, current_api_data)

  return '\n'.join([json.dumps(item) for item in current_api_data])

def main():
  apis = ['users', 'groups', 'organizations', 'tickets']
  api_data = {api: write_json_file(api) for api in apis}

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  for api in apis:
    blob_name = f'{api}/ingest_date={str(date.today())}/{api}.json'
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data=api_data[api])
    print(
      f'Uploaded to gs://{bucket_name}/{blob.name}'
    )

if __name__ == "__main__":
    main()
