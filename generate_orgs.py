import requests
import os
import json

cookies = dict({cookie.split("=")[0]:cookie.split("=")[1] for cookie in os.environ["COOKIE"].split(";")})

def org_page(page_num=1):
  return get(f'https://doitintl.zendesk.com/api/v2/organizations.json?page={page_num}', cookies, page_num)

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

def main():
  orgs = []
  counter = 1
  current_org_page = org_page()
  orgs.extend([org for org in current_org_page['organizations']])

  while org_page(counter)['next_page'] != None:
    counter += 1
    current_org_page = org_page(counter)
    orgs.extend(current_org_page['organizations'])

  with open('org.json', 'w') as outfile:
    json.dump(orgs, outfile)

if __name__ == "__main__":
    main()
