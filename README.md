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

## SNP Chromosome Query
GetSNPsByChromosome(self, chr, start, end, fields, filter=None, page_from=None, page_size=None)

#### Parameters

**chr (str)** -  Chromosome string in double quotes ("")

**start (int)** - Start of chromosome

**end (int)** - End of chromosome

**fields (list[str])** - List of strings with the fields that you

**filters (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page
```
annoq().GetSNPsByChromosome(chr="2", start=1, end=10000000, fields=['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'], filter=['chr'], page_from=2, page_size=4)
```


## SNP Gene Product Query
GetSNPsByGeneProduct(self, gene, fields, filter=None, page_from=None, page_size=None)

#### Parameters 

**gene (str)** -  Gene product string in double quotes ("")

**fields (list[str])** - List of strings with the fields that you

**filters (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByGeneProduct(gene="Q9BVC4", fields=["chr", "id"], filter=["chr", "pos"], page_from=0, page_size=10)
```

## SNP ID Query
GetSNPsByIDs(self, ids, fields, filter=None, page_from=None, page_size=None)

#### Parameters 

**ids (list[str])** -  List of IDs

**fields (list[str])** - List of strings with the fields that you

**filters (list[str])** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByIDs(ids=["2:10632C>A", "2:10632C>A"], fields=["id", "chr"], filter=["chr"], page_from=0, page_size=5)
```