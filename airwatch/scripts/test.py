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
      bands: ['CO', 'dataMask']
    }],
    output: [
      {
        id: 'output_co',
        bands: 1
      },
      {
        id: 'dataMask',
        bands: 1
      }
    ]
  };
}

function evaluatePixel(sample) {
  return {
      output_co: [sample.CO],
      dataMask: [sample.dataMask]
  }
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

    bbox = BBox(coordinates, CRS.WGS84)

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
  time_from = '2024-02-17'
  time_to = '2024-02-18'
  coordinates = (113.8259, 22.1435, 114.4529, 22.561949)

  client = SentinelClient(client_id, client_secret)
  data = client.get_air_pollution_data(coordinates, time_from, time_to)
  print(data)


run()

