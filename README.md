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
GetSNPsByChromosome(self, chr, start, end, fields)

chr: chromosome string in double quotes ("") <br>
start: integer for start of chromosome <br>
end: integer for end of chromosome <br>
fields: list of strings with the fields that you require
```
annoq().GetSNPsByChromosome("2", 1, 10000000, ['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'])
```