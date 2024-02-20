from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import math

def epsg3857toEpsg4326(pos):
  x = pos[0]
  y = pos[1]

  x = (x * 180) / 20037508.34
  y = (y * 180) / 20037508.34
  y = (math.atan(math.pow(math.e, y * (math.pi / 180))) * 360) / math.pi - 90

  return [x, y]

EVALSCRIPT = """

//VERSION=3

function setup() {
  return {
    input: [{
      bands: [
        "CO",
        "dataMask"
      ]
    }],
    output: [
      {
        id: "output_co",
        bands: 1,
        sampleType: "FLOAT32"
      },
      {
        id: "dataMask",
        bands: 1      
      }
    ]
  }
}

function evaluatePixel(samples) {
  return {
    output_co: [samples.CO],
    dataMask: [samples.dataMask]
  }
}

"""

client_id = 'd1e2eebf-0e43-40f2-a64b-ceca033f679c'
client_secret = 'F41cuO5xBkxrXasa3EZc2Ykv79Nxa6X5'

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

json = {
  'input': {
    'bounds': {
      'properties': {
        'crs': 'http://www.opengis.net/def/crs/EPSG/0/3857'
      },
      'bbox': [
        114.4529,
        113.8259,
        22.561949,
        22.1435
      ]
    },
    'data': [{
      'type': 'sentinel-5p-l2'
    }]  
  },
  'aggregation': {
    'timeRange': {
      'from': '2023-08-24T14:15:22Z',
      'to': '2023-09-20T14:15:22Z'
    },
    'aggregationInterval': {
      'of': 'P20D'
    },
    'evalscript': EVALSCRIPT
  }
}

url = 'https://creodias.sentinel-hub.com/api/v1/statistics'
response = oauth.request("POST", url=url , headers=headers, json=json)
print(response.json())


from sentinelhub import (
  BBox,
  CRS,
  DataCollection,
  SentinelHubStatistical,
  SHConfig
)

EVALSCRIPT = """

//VERSION=3

function setup() {
  return {
    input: [{
      bands: ['CO']
    }],
    output: {
      bands: 1
    }
  };
}

function evaluatePixel(sample) {
  return [sample.CO]
}

"""

class SentinelClient:
  def __init__(self, client_id, client_secret):
    self._config = SHConfig()
    self._config.client_id = client_id
    self._config.client_secret = client_secret

  def get_air_pollution_data(self, coordinates, time_from, time_to):

    aggregation = SentinelHubStatistical.aggregation(
      evalscript=EVALSCRIPT,
      time_interval=(time_from, time_to),
      aggregation_interval='P1D',
      size=(631, 1047)
    )

    input_data=[SentinelHubStatistical.input_data(DataCollection.SENTINEL5P, maxcc=0.8)]

    bbox = BBox(coordinates, CRS.POP_WEB)

    request = SentinelHubStatistical(
      aggregation=aggregation,
      input_data=input_data,
      bbox=bbox,
      config=self._config
    )

    return request.get_data()

def run():
  client_id = 'd1e2eebf-0e43-40f2-a64b-ceca033f679c'
  client_secret = 'F41cuO5xBkxrXasa3EZc2Ykv79Nxa6X5'
  time_from = '2020-06-07'
  time_to = '2020-06-13'
  coordinates = (52.097877, 20.85129, 52.367999, 21.271098)

  client = SentinelClient(client_id, client_secret)
  data = client.get_air_pollution_data(coordinates, time_from, time_to)
  print(data)


run()

