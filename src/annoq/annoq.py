import requests
import json

class annoq:

    def __init__(self):
        self.BASE_URL = 'http://annoq.org/api-v2/'
        self.GRAPHQL_ENDPOINT = 'graphql'

    
    def testing(self):
        return "chr"


    def GetSNPsByChromosome(self, chr, start, end, fields, filter=None, page_from=None, page_size=None):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        base = f"""
                query MyQuery {{
                    GetSNPsByChromosome(chr: {json.dumps(chr)}, end: {end}, start: {start}
                """
        if filter != None:
            base += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}}
                    """
        if page_from != None and page_size != None:
            base += f"""
                    , page_args: {{from_: {page_from}, size: {page_size}}}
                    """
            
        query = base + f"""
            ) {{
                    {fields_str}
                }}
            }}
            """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        snps_by_chromosome = data['data']['GetSNPsByChromosome']
        return snps_by_chromosome