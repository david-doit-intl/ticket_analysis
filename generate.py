import requests
import os
import json

cookies = dict({cookie.split("=")[0]:cookie.split("=")[1] for cookie in os.environ["COOKIE"].split(";")})

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

def write_json_file(current_api):
  current_api_data = []
  counter = 1
  current_page = fetch(current_api, counter)
  current_api_data.extend(current_page[current_api])
  
  while current_page.get('next_page', None) != None:
    counter += 1
    current_page = fetch(current_api, counter)
    current_api_data.extend(current_page[current_api])

  with open(f'{current_api}.json', 'w') as outfile:
    for item in current_api_data:
      json.dump(item, outfile)
      outfile.write('\n')

def main():
  apis = ['users', 'groups', 'organizations', 'tickets', 'ticket_metrics']
  [write_json_file(api) for api in apis]

if __name__ == "__main__":
    main()
