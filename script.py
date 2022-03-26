import json
import requests
from requests.structures import CaseInsensitiveDict
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from requests.structures import CaseInsensitiveDict
import datetime as dt
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


url = "https://account.divvybikes.com/bikesharefe-gql"

total_ride_history = []

headers = CaseInsensitiveDict()
headers["Host"] = "account.divvybikes.com"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0"
headers["Accept"] = "*/*"
headers["Accept-Language"] = "en-US,en;q=0.5"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Referer"] = "https://account.divvybikes.com/ride-history"
headers["Content-Type"] = "application/json"
headers["Origin"] = "https://account.divvybikes.com"
headers["Content-Length"] = "656"
headers["Connection"] = "keep-alive"
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "same-origin"
headers["TE"] = "trailers"
headers["Authorization"] = "Bearer " + os.getenv('AUTHORIZATION')


query = """query GetCurrentUserRides($startTimeMs: String, $userId: String) {
  me {
    id
    rideHistory(startTimeMs: $startTimeMs, userId: $userId) {
      hasMore
      limit
      rideHistoryList {
        rideId
        startTimeMs
        endTimeMs
        distance {
          __typename
        }
        price {
          ...MoneyFields
          __typename
        }
        duration
        rideableName
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment MoneyFields on Money {
  amount
  exponent
  __typename
}

"""

d = {'query': query, 'variables': {}}

payload = json.dumps(d)

resp = requests.post(url, headers=headers, data=payload, verify=False)
print(resp)

total_ride_history = total_ride_history + resp.json()['data']['me']['rideHistory']['rideHistoryList']

variables = {
  "startTimeMs": total_ride_history[-1]['startTimeMs'],
} 

# print(payload)

while resp.json()['data']['me']['rideHistory']['hasMore']:
    payload = {
        "query": query,
        "variables": variables,
    }

    resp = requests.post(url, headers=headers, json=payload, verify=False)
    total_ride_history = total_ride_history + resp.json()['data']['me']['rideHistory']['rideHistoryList']
    variables = {
      "startTimeMs": total_ride_history[-1]['startTimeMs'],
    } 


print('all done!')


#print(json.dumps(resp.json(), indent=2))
print(total_ride_history)

df = pd.DataFrame(total_ride_history).drop_duplicates('rideId') # it'll duplicate some rides for w/e reason

df['startTime'] = pd.to_datetime(df['startTimeMs'], unit='ms', utc=True).dt.tz_convert('US/Central') # convert to
df['endTime'] = pd.to_datetime(df['endTimeMs'], unit='ms', utc=True).dt.tz_convert('US/Central')
df['duration_min'] = df['duration'] * (1/60000)
df['cost'] = [obj['amount']/100 for obj in df['price']]

print(sum(df['cost']))
print(sum(df['duration_min']/60))


query2 = """query GetCurrentUserRideDetails($rideId: String!) {
  me {
    id
    rideDetails(rideId: $rideId) {
      distance {
        str
      }
      startAddressStr      
      endAddressStr
      startAddress {
        lat
        lng
      }
      endAddress
      {
        lat
        lng
      }
    }
    __typename
  }
}

"""
d2 = {'query': query2, 'variables': { 'rideId': '1583317146768795904'}}
payload2 = json.dumps(d2)


resp = requests.post(url, headers=headers, data=payload2, verify=False)

distances = []
startAddresses = []
endAddresses = []

for rideId in df['rideId']:
  d2 = {'query': query2, 'variables': { 'rideId': rideId}}
  payload2 = json.dumps(d2)
  resp = requests.post(url, headers=headers, data=payload2, verify=False)
  distances.append(resp.json()['data']['me']['rideDetails']['distance']['str'])
  startAddresses.append(resp.json()['data']['me']['rideDetails']['startAddressStr'])
  endAddresses.append(resp.json()['data']['me']['rideDetails']['endAddressStr'])

distances = [float(d[0:len(d)-2]) for d in distances]
df['distance'] = distances
df['startAddress'] = startAddresses
df['endAddress'] = endAddresses

df.to_csv('my_divvy_data.csv')
print('fin.')