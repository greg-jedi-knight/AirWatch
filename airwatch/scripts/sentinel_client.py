from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import math

EVALSCRIPT = """


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
    var sumCO = 0;
    var count = 0;

    // Loop through all samples (time instances)
    for (var i = 0; i < samples.length; i++) {
        var sample = samples[i];

        // Access CO data (replace 'CO_column_number' with the actual band number for CO)
        var CO = sample.CO

        // Check if CO value is valid (not a fill value or invalid data)
        if (!isNaN(CO) && CO !== null) {
            sumCO += CO;
            count++;
        }
    }

    // Calculate average CO concentration
    var averageCO = count > 0 ? sumCO / count : null;

    return {
        output_co: [averageCO], // Output the average CO concentration
        dataMask: [count > 0 ? 1 : 0] // Output data mask (1 where data is valid, 0 otherwise)
    };
}

// Setup the input for the scrip

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