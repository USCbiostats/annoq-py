"""
Basic tests for the Annoq API Python Client.
"""

import json
from annoq import (
    get_snp_attributes,
    get_snps_by_chr,
    get_snps_by_rsid_list,
    get_snps_by_gene_product,
    count_snps_by_chr,
    count_snps_by_rsid_list,
    count_snps_by_gene_product,
)


def test_imports():
    """Test that all functions can be imported."""
    assert get_snp_attributes is not None
    assert get_snps_by_chr is not None
    assert get_snps_by_rsid_list is not None
    assert get_snps_by_gene_product is not None
    assert count_snps_by_chr is not None
    assert count_snps_by_rsid_list is not None
    assert count_snps_by_gene_product is not None


def test_process_fields_function():
    """Test the internal fields processing function."""
    from annoq.api import _process_fields_param

    # Test with None
    assert _process_fields_param(None) is None

    # Test with JSON string
    json_str = '{"_source":["chr","pos","ref","alt"]}'
    result = _process_fields_param(json_str)
    assert result == json_str

    # Test with list of attributes
    attr_list = ["chr", "pos", "ref", "alt"]
    result = _process_fields_param(attr_list)
    # Parse and compare the JSON to avoid string formatting issues
    assert result is not None
    assert json.loads(result) == {"_source": attr_list}


if __name__ == "__main__":
    test_imports()
    test_process_fields_function()
    print("All tests passed!")
