import requests
import json

class annoq:

    def __init__(self):
        self.BASE_URL = 'http://annoq.org/api-v2/'
        self.GRAPHQL_ENDPOINT = 'graphql'

    
    def testing(self):
        return "chr"


    def GetSNPsByChromosome(self, chr, start, end, fields):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        query = f"""
            query MyQuery {{
                GetSNPsByChromosome(chr: {json.dumps(chr)}, end: {end}, start: {start}) {{
                    {fields_str}
                }}
            }}
            """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        snps_by_chromosome = data['data']['GetSNPsByChromosome']
        return snps_by_chromosome