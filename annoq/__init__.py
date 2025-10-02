"""
Annoq API Python Client

A Python package for accessing SNP data from Annoq.org
"""

from .api import (
    get_snp_attributes,
    get_snps_by_chr,
    get_snps_by_rsid_list,
    get_snps_by_gene_product,
    count_snps_by_chr,
    count_snps_by_rsid_list,
    count_snps_by_gene_product,
)

__all__ = [
    "get_snp_attributes",
    "get_snps_by_chr",
    "get_snps_by_rsid_list",
    "get_snps_by_gene_product",
    "count_snps_by_chr",
    "count_snps_by_rsid_list",
    "count_snps_by_gene_product",
]

__version__ = "1.0.0"
