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
    get_snpway_gene_mappings,
    run_snpway_overrepresentation_workflow,
)

__all__ = [
    "get_snp_attributes",
    "get_snps_by_chr",
    "get_snps_by_rsid_list",
    "get_snps_by_gene_product",
    "count_snps_by_chr",
    "count_snps_by_rsid_list",
    "count_snps_by_gene_product",
    "get_snpway_gene_mappings",
    "run_snpway_overrepresentation_workflow",
]

__version__ = "1.1.0"
