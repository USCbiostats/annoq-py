import requests
import json

class annoq:

    def __init__(self):
        self.BASE_URL = 'http://annoq.org/api-v2/'
        self.GRAPHQL_ENDPOINT = 'graphql'


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
        return data['data']['GetSNPsByChromosome']
    

    def GetSNPsByGeneProduct(self, gene, fields, filter=None, page_from=None, page_size=None):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        base = f"""
                query MyQuery {{
                    GetSNPsByGeneProduct(gene: {json.dumps(gene)}
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
        return data['data']['GetSNPsByGeneProduct']
    
    
    def GetSNPsByIDs(self, ids, fields, filter=None, page_from=None, page_size=None):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        base = f"""
                query MyQuery {{
                    GetSNPsByIDs(ids: {json.dumps(ids)}
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
        return data['data']['GetSNPsByIDs']
    

    def GetSNPsByRsID(self, rsID, fields, filter=None, page_from=None, page_size=None):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        base = f"""
                query MyQuery {{
                    GetSNPsByRsID(rsID: {json.dumps(rsID)}
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
        return data['data']['GetSNPsByRsID']
    

    def GetSNPsByRsIDs(self, rsIDs, fields, filter=None, page_from=None, page_size=None):
        fields_str = ''
        for elt in fields:
            fields_str += elt + '\n'
        base = f"""
                query MyQuery {{
                    GetSNPsByRsIDs(rsIDs: {json.dumps(rsIDs)}
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
        return data['data']['GetSNPsByRsIDs']