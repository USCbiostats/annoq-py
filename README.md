This is a Python package for annoq-api-v2

# Local Usage

Clone this repository
```
git clone https://github.com/USCbiostats/annoq-py.git
```

Install the package 
```
pip install .
```

Open python on the terminal and import the package
```
python 
>>> from src.annoq import annoq
```

## Get SNP by Chromosome Query
GetSNPsByChromosome(self, chr, start, end, fields, filter=None, page_from=None, page_size=None)

Returns list of json

#### Parameters

**chr (str)** -  Chromosome string

**start (int)** - Start of chromosome

**end (int)** - End of chromosome

**fields (list[str])** - List of strings with the fields that you

**filter (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page
```
annoq().GetSNPsByChromosome(chr="2", start=1, end=10000000, fields=['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'], filter=['chr'], page_from=2, page_size=4)
```


## Get SNP by Gene Product Query
GetSNPsByGeneProduct(self, gene, fields, filter=None, page_from=None, page_size=None)

Returns list of json

#### Parameters 

**gene (str)** -  Gene product string

**fields (list[str])** - List of strings with the fields that you

**filter (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByGeneProduct(gene="Q9BVC4", fields=["chr", "id"], filter=["chr", "pos"], page_from=0, page_size=10)
```

## Get SNP by ID Query
GetSNPsByIDs(self, ids, fields, filter=None, page_from=None, page_size=None)

Returns list of json

#### Parameters 

**ids (list[str])** -  List of IDs

**fields (list[str])** - List of strings with the fields that you

**filter (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByIDs(ids=["2:10632C>A", "2:10632C>A"], fields=["id", "chr"], filter=["chr"], page_from=0, page_size=5)
```

## Get SNP by RsID Query
GetSNPsByRsID(self, rsID, fields, filter=None, page_from=None, page_size=None)

Returns list of json

#### Parameters 

**rsID (str)** -  rsID string

**fields (list[str])** - List of strings with the fields that you

**filter (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByRsID(rsID='rs189126619', fields=["rs_dbSNP151", "ref"], filter=["rs_dbSNP151"], page_from=0, page_size=2)
```

## Get SNP by RsIDs Query
GetSNPsByRsIDs(self, rsIDs, fields, filter=None, page_from=None, page_size=None)

Returns list of json

#### Parameters 

**rsIDs (list[str])** -  list of rsIDs

**fields (list[str])** - List of strings with the fields that you

**filter (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByRsIDs(rsIDs=['rs189126619', 'rs115366554'], fields=["rs_dbSNP151", "ref"], filter=["rs_dbSNP151"], page_from=0, page_size=2)
```

## Count SNP by Chromosome Query
CountSNPsByChromosome(self, chr, start, end, filter)

return int

#### Parameters

**chr (str)** -  Chromosome string

**start (int)** - Start of chromosome

**end (int)** - End of chromosome

**filter (list[str])** - List of strings with fields that you want to filter on

```
annoq().CountSNPsByChromosome(chr="2", start=1, end=10000000, filter=["chr", "ANNOVAR_ensembl_Closest_gene(intergenic_only)"])
```

## Count SNP by Gene Product Query
CountSNPsByGeneProduct(self, gene, filter)

return int

#### Parameters

**gene (str)** -  Gene product string

**filter (list[str])** - List of strings with fields that you want to filter on

```
annoq().CountSNPsByGeneProduct(gene="Q9BVC4", filter=["chr", "pos"])
```

## Count SNP by ID Query
CountSNPsByIDs(self, ids, filter)

return int

#### Parameters

**ids (list[str])** -  List of IDs

**filter (list[str])** - List of strings with fields that you want to filter on

```
annoq().CountSNPsByIDs(ids=["2:10632C>A", "2:10632C>A"], filter=["chr"])
```

## Count SNP by RsID Query
CountSNPsByRsID(self, rsID, filter)

return int

#### Parameters

**rsID (str)** -  rsID string

**filter (list[str])** - List of strings with fields that you want to filter on

```
annoq().CountSNPsByRsID(rsID='rs189126619', filter=["rs_dbSNP151"])
```

## Count SNP by RsIDs Query
CountSNPsByRsID(self, rsIDs, filter)

return int

#### Parameters

**rsIDs (list[str])** -  list of rsIDs

**filter (list[str])** - List of strings with fields that you want to filter on

```
annoq().CountSNPsByRsIDs(rsIDs=['rs189126619', 'rs115366554'], filter=["rs_dbSNP151"])
```