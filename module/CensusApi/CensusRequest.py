import requests
import pandas as pd

class CensusRequest:
    def __init__(self, api_key: str, year: int, dataset: str):
        self.api_key = api_key
        self.year = year
        self.dataset = dataset

    def get(self, fields: list[str], geo: str, filters: dict[str, str]):
        value = requests.get(f'https://api.census.gov/data/{self.year}/{self.dataset}', params={
            'get': ','.join(fields),
            'for': geo,
            'key': self.api_key,
            **filters
        })
        value_json = value.json()
        columns = value_json[0]
        values = value_json[1:]
        return pd.DataFrame(values, columns=columns)
    
# Census = CensusRequest('1f76be8ce6d9fa33836cb9fbdfe958a9cf672ed5', 2019, 'acs/acs1')

# Census.get(['NAME', 'B02015_009E', 'B02015_009M'], 'state:*', {}).to_csv('data.csv', index=False)