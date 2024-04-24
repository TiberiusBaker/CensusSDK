import os, sys

# use os and sys to allow access to a parent directories folders, which is two folders up from the current directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import CensusApi.CensusRequest as CensusRequest

class ACS:
    def __init__(self, year: int):
        self.census = CensusRequest.CensusRequest('1f76be8ce6d9fa33836cb9fbdfe958a9cf672ed5', year, 'acs/acs1')
    
    def get(self, fields: list[str], geo: str, filters: dict[str, str]):
        return self.census.get(fields, geo, filters)
    
ACS(2019).get(['NAME', 'B02015_009E', 'B02015_009M'], 'state:*', {}).to_csv('data.csv', index=False)