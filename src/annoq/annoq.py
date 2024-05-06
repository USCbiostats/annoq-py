import requests
import json

class annoq:

    def __init__(self):
        self.BASE_URL = 'http://annoq.org/api-v2/'
        self.GRAPHQL_ENDPOINT = 'graphql'


    def get_SNPs_by_chromosome(self, chr, start, end, fields, query_type_option='SNPS', filter=None, page_from=None, page_size=None):
        try:
            fields_str = ''
            for elt in fields:
                fields_str += elt + '\n'
            base = f"""
                    query MyQuery {{
                        get_SNPs_by_chromosome(chr: {json.dumps(chr)}, end: {end}, start: {start}, query_type_option: {query_type_option}
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
                ) {{ snps {{
                        {fields_str}
                        }}
                    }}
                }}
                """

            response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

            data = json.loads(response.text)
            return data['data']['get_SNPs_by_chromosome']['snps']
        except Exception as e:
            print('Unexpected error:', e)
    

    def get_SNPs_by_gene_product(self, gene, fields, filter=None, page_from=None, page_size=None):
        try:
            fields_str = ''
            for elt in fields:
                fields_str += elt + '\n'
            base = f"""
                    query MyQuery {{
                        get_SNPs_by_gene_product(gene: {json.dumps(gene)}, query_type_option: SNPS
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
                ) {{ snps {{
                            {fields_str}
                        }}
                    }}
                }}
                """
            response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

            data = json.loads(response.text)
            return data['data']['get_SNPs_by_gene_product']['snps']
        except Exception as e:
            print('Unexpected error:', e)
    

    def get_SNPs_by_IDs(self, ids, fields, filter=None, page_from=None, page_size=None):
        try:
            fields_str = ''
            for elt in fields:
                fields_str += elt + '\n'
            base = f"""
                    query MyQuery {{
                        get_SNPs_by_IDs(ids: {json.dumps(ids)}, query_type_option: SNPS
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
                ) {{ snps {{
                            {fields_str}
                        }}
                    }}
                }}
                """

            response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

            data = json.loads(response.text)
            return data['data']['get_SNPs_by_IDs']['snps']
        except Exception as e:
            print('Unexpected error:', e)
    

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
    

    def CountSNPsByChromosome(self, chr, start, end, filter=None):
        query = f"""
                query MyQuery {{
                    CountSNPsByChromosome(chr: {json.dumps(chr)}, end: {end}, start: {start}
                """
        
        if filter != None:
            query += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}})
                    }}
                    """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        return data['data']['CountSNPsByChromosome']
    

    def CountSNPsByGeneProduct(self, gene, filter=None):
        query = f"""
                query MyQuery {{
                    CountSNPsByGeneProduct(gene: {json.dumps(gene)}
                """
        
        if filter != None:
            query += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}})
                    }}
                    """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        return data['data']['CountSNPsByGeneProduct']
    

    def CountSNPsByIDs(self, ids, filter=None):
        query = f"""
                query MyQuery {{
                    CountSNPsByIDs(ids: {json.dumps(ids)}
                """
        
        if filter != None:
            query += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}})
                    }}
                    """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        return data['data']['CountSNPsByIDs']
    

    def CountSNPsByRsID(self, rsID, filter=None):
        query = f"""
                query MyQuery {{
                    CountSNPsByRsID(rsID: {json.dumps(rsID)}
                """
        
        if filter != None:
            query += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}})
                    }}
                    """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        return data['data']['CountSNPsByRsID']


    def CountSNPsByRsIDs(self, rsIDs, filter=None):
        query = f"""
                query MyQuery {{
                    CountSNPsByRsIDs(rsIDs: {json.dumps(rsIDs)}
                """
        
        if filter != None:
            query += f"""
                    , filter_args: {{exists: {json.dumps(filter)}}})
                    }}
                    """

        response = requests.post(f"{self.BASE_URL}{self.GRAPHQL_ENDPOINT}", json={'query': query})

        data = json.loads(response.text)
        return data['data']['CountSNPsByRsIDs']