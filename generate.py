from google.cloud import secretmanager
from google.cloud import storage
from datetime import date
import requests
import os
import json

from flask import Flask

app = Flask(__name__)

client = secretmanager.SecretManagerServiceClient()


def get_secret(project_id, secret_id, version_id=8):
  parent = client.secret_path(project_id, secret_id)
  versions = [version.name for version in client.list_secret_versions(request={"parent": parent})]
  latest_version = versions[0]
  response = client.access_secret_version(request={"name": latest_version})
  return str(response.payload.data.decode("UTF-8"))

def fetch(api, cookies, page_num=1):
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

def iterate_through_pages(current_api, cookies, current_api_data, counter=1):
  current_page = fetch(current_api, cookies, counter)
  current_api_data.extend(current_page[current_api])
  if current_page.get('next_page', None) != None:
    counter += 1
    iterate_through_pages(current_api, cookies, current_api_data, counter)

def get_json_data(current_api, cookies):
  current_api_data = []
  iterate_through_pages(current_api, cookies, current_api_data)

  return '\n'.join([json.dumps(item) for item in current_api_data])

@app.route("/")
def main():
  raw_cookie = get_secret('warehouse-302911','ZENDESK_COOKIE')
  cookies = dict({
    cookie.split("=")[0].strip():cookie.split("=")[1]
    for cookie in raw_cookie.split(";")
  })

  bucket_name = os.environ["BUCKET"]
  apis = ['users', 'groups', 'organizations', 'tickets']

  api_data = {api: get_json_data(api, cookies) for api in apis}

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  for api in apis:
    blob_name = f'{api}/ingest_date={str(date.today())}/{api}.json'
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data=api_data[api])
    print(
      f'Uploaded to gs://{bucket_name}/{blob.name}'
    )
  return "Files Uploaded Successfully"


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
