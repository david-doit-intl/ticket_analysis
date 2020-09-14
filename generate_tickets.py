import requests
import os

cookies = dict({cookie.split("=")[0]:cookie.split("=")[1] for cookie in os.environ["COOKIE"].split(";")})

def org_tickets(org_id, page_num=1):
  return get(f'https://doitintl.zendesk.com/api/v2/organizations/{org_id}/tickets.json?page={page_num}', cookies, page_num)

def org_page(page_num=1):
  return get(f'https://doitintl.zendesk.com/api/v2/organizations.json?page={page_num}', cookies, page_num)

def get(uri, cookies, page_num):
  response = requests.get(uri, cookies=cookies)
  return response.json()

def main():
  org_ids = {}
  counter = 1
  current_org_page = org_page()
  org_ids.update({org['id']: {"name": org['name']} for org in current_org_page['organizations']})
  
  while org_page(counter)['next_page'] != None:
    counter += 1
    current_org_page = org_page(counter)
    org_ids.update({org['id']: {"name": org['name']} for org in current_org_page['organizations']})

  for key in org_ids.keys():
    tickets = org_tickets(key)
    number_of_tickets = len(tickets['tickets'])
    counter = 1
    while tickets['next_page'] != None:
        counter += 1
        tickets = org_tickets(key, counter)
        number_of_tickets = len(tickets['tickets'])

    print(f'{org_ids[key]["name"]} has created {number_of_tickets} tickets')



if __name__ == "__main__":
    main()
