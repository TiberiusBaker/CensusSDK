import requests
import pandas as pd

class CensusRequest:
    def __init__(self, api_key: str, year: int, dataset: str):
        self.api_key = api_key
        self.year = year
        self.dataset = dataset

    def get(self, group: str, fields: list[str], geo: str, filters: dict[str, str]):
        fields = ",".join(fields)
        value = requests.get(f'https://api.census.gov/data/{self.year}/{self.dataset}', params={
            'get': fields + ',group(' + group + ')',
            'for': geo,
            'key': self.api_key,
            **filters
        })
        value_json = value.json()
        columns = value_json[0]
        values = value_json[1:]
        return pd.DataFrame(values, columns=columns)
    
# Census = CensusRequest('', 2019, 'acs/acs1')

# Census.get(['NAME', 'B02015_009E', 'B02015_009M'], 'state:*', {}).to_csv('data.csv', index=False)