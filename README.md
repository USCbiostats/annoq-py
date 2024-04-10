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

## Chromosome Query
GetSNPsByChromosome(self, chr, start, end, fields, filter, page_from, page_size)

#### Parameters

**chr (str)** -  Chromosome string in double quotes ("")

**start (int)** - Start of chromosome

**end (int)** - End of chromosome

**fields (list)** - List of strings with the fields that you

**filters (list)** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page
```
annoq().GetSNPsByChromosome("2", 1, 10000000, ['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'], ['chr'], 2, 4)
```


## Gene Product Query
GetSNPsByGeneProduct(self, gene, fields, filter=None, page_from=None, page_size=None)

#### Parameters 

**gene (str)** -  Gene product string in double quotes ("")

**fields (list)** - List of strings with the fields that you

**filters (list)** - List of strings with fields that you want to filter on

**page_from (int)** - Starting page number

**page_size (int)** - Size of the page

```
annoq().GetSNPsByGeneProduct("Q9BVC4", ["chr", "id"], ["chr", "pos"], 0, 10)
```