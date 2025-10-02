# Annoq API Python Client

A Python package for accessing SNP data from Annoq.org

## Installation

```bash
pip install annoq-py
```

## Usage

### Getting Started

```python
import annoq

# Get available SNP attributes
attributes = annoq.get_snp_attributes()
print(attributes)
```

### Get SNP Attributes

```python
# Retrieve available SNP attributes
attributes = annoq.get_snp_attributes()
```

### Search SNPs by Chromosome

```python
# Search SNPs on chromosome 1 from position 1 to 100000
snps = annoq.get_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=100000
)

# With custom fields (as a list)
snps = annoq.get_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=10000,
    fields=["chr", "pos", "ref", "alt", "rs_dbSNP151"]
)

# With custom fields (as JSON string)
snps = annoq.get_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=1000,
    fields='{"_source":["chr", "pos", "ref", "alt", "rs_dbSNP151"]}'
)

# With custom fields (from file path)
snps = annoq.get_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=100000,
    fields="/path/to/fields_config.json"
)
```

### Search SNPs by RSID List

```python
# Search by RSID list (as string)
snps = annoq.get_snps_by_rsid_list(
    rsid_list="rs1219648,rs2912774,rs2981582"
)

# Search by RSID list (as list)
snps = annoq.get_snps_by_rsid_list(
    rsid_list=["rs1219648", "rs291274", "rs2981582"]
)
```

### Search SNPs by Gene Product

```python
# Search SNPs by gene product
snps = annoq.get_snps_by_gene_product(
    gene="ZMYND11"
)
```

### Count SNPs

```python
# Count SNPs by chromosome
count_result = annoq.count_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=100000
)

# Count SNPs by RSID list
count_result = annoq.count_snps_by_rsid_list(
    rsid_list=["rs1219648", "rs2912774"]
)

# Count SNPs by gene product
count_result = annoq.count_snps_by_gene_product(
    gene="ZMYND11"
)
```

### Filter Fields

You can also filter results to only include records where specific fields are not empty:

```python
# Filter to only include records with non-empty annotation fields
snps = annoq.get_snps_by_chr(
    chromosome_identifier="1",
    start_position=1,
    end_position=100000,
    filter_fields="ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID"
)
```

## API Functions

The package provides 7 main functions:

1. `get_snp_attributes()` - Retrieve available SNP attributes
2. `get_snps_by_chr()` - Get SNPs by chromosome and position range
3. `get_snps_by_rsid_list()` - Get SNPs by RSID list
4. `get_snps_by_gene_product()` - Get SNPs by gene product
5. `count_snps_by_chr()` - Count SNPs by chromosome and position range
6. `count_snps_by_rsid_list()` - Count SNPs by RSID list
7. `count_snps_by_gene_product()` - Count SNPs by gene product

## Fields Parameter

The `fields` parameter accepts three formats:

- **List of attributes**: `["chr", "pos", "ref", "alt"]`
- **JSON string**: `'{"_source":["chr", "pos", "ref", "alt"]}'`
- **File path**: `"/path/to/config.json"` (file containing the JSON config)

## License

MIT License
