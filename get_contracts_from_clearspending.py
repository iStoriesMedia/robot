from clearspending_contract_parser import parse_contract

class ClearSpending:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.search_query = ''.join(f'{key}={value}&' for key, value in self.kwargs.items())
        self.url = f"http://openapi.clearspending.ru/restapi/v3/contracts/search/?{self.search_query}sort=-price"
    
    def get_contracts(self, limit=500):
        import requests
        page = 1
        contracts = []
        while len(contracts) < limit:
            try:
                url = self.url + f'&page={page}'
                print(url)
                r = requests.get(url)
                data = r.json()['contracts']['data']
                if not len(data):
                    break
                for el in data:
                    if len(contracts) < limit:
                        contract = parse_contract(el)
                        contracts.append(contract)
                    else:
                        break

                page += 1
            except Exception as e:
                print(e)
                break
        return contracts

    def to_csv(self, file_name):
        import csv
        contracts = self.get_contracts()
        with open(file_name, 'w') as file:
            fieldnames = [key for key in contracts[0]]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contract in contracts:
                writer.writerow(contract)

    def to_pd(self):
        import pandas as pd
        df = pd.DataFrame(self.get_contracts())
        return df



if __name__ == "__main__":
    url = ClearSpending(okdp_okpd='6220010').to_csv('flights2.csv')