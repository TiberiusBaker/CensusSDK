import os, sys
import requests
import pandas as pd

# use os and sys to allow access to a parent directories folders, which is two folders up from the current directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import CensusApi.CensusRequest as CensusRequest

class ACS:
    def __init__(self, year: int):
        self.year = year
        self.census = CensusRequest.CensusRequest('', year, 'acs/acs1')
    
    def get(self, group: str, fields: list[str], geo: str, filters: dict[str, str]):
        return self.census.get(group, fields, geo, filters)
    
    def get_variables(self):
        dataframe = self.__read_variables()
        self.variables = dataframe

    def __read_variables(self) -> pd.DataFrame:
        if (os.path.exists(f'variables_{self.year}.csv')):
            return pd.read_csv(f'variables_{self.year}.csv')
        else:
            # This link says it is a csv file, but it is actually an excel file
            dataframe = pd.read_excel(f'https://www2.census.gov/data/api-documentation/{self.year}-1yr-api-changes.csv')
            bad_columns = [f'{self.year - 1} Variable', f'{self.year - 1} Label']
            dataframe.drop(columns=bad_columns, inplace=True)
            dataframe.to_csv(f'variables_{self.year}.csv', index=False)
            return dataframe
        
    def get_random_data(self):
        random_row = self.variables.sample()
        group = random_row['Table ID'].values[0]
        variable = random_row[f'{self.year} Variable'].values[0]
        description = random_row[f'{self.year} Label'].values[0]
        dataframe = self.census.get(group, ['NAME', variable], 'state:*', {})
        dataframe = dataframe[['NAME', variable]].copy()
        dataframe = dataframe.loc[:,~dataframe.columns.duplicated()].copy()
        dataframe.rename(columns={variable: description}, inplace=True)
        dataframe.to_csv(f'{variable}.csv', index=False)

        print(f'Variable: {variable}\nDescription: {description}\n')
            
    
# ACS(2019).get(['NAME', 'B02015_009E', 'B02015_009M'], 'state:*', {}).to_csv('data.csv', index=False)

# ACS(2022).get('B01001', ['NAME', 'DP02_0059E'], 'state:*', {}).to_csv('pop_education_attainment_over_25.csv', index=False)

acs = ACS(2022)
acs.get_variables()
acs.get_random_data()