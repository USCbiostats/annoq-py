"""
Annoq API Python Client

A Python package for accessing SNP data from Annoq.org
"""

import json
import requests
from typing import Union, List, Dict, Any, Optional


# Base URL for the Annoq API
BASE_URL = "https://api-v2-dev.annoq.org"


def _process_fields_param(fields: Union[str, List[str], None]) -> Optional[str]:
    """
    Process the fields parameter to handle the three possible input types:
    1. JSON string: {"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}
    2. File path: path to a file containing the JSON config
    3. List of attributes: ["Basic Info", "chr", "pos", "ref", "alt", "rs_dbSNP151"]

    Returns the JSON string representation or None if fields is None.
    """
    if fields is None:
        return None

    if isinstance(fields, str):
        # Check if it's a file path by attempting to read it
        if fields.startswith("{") and fields.endswith("}"):
            # It's a JSON string
            return fields
        else:
            # It might be a file path, try to read it
            try:
                with open(fields, "r") as f:
                    content = f.read()
                return content
            except FileNotFoundError:
                # If it's not a valid file path, treat it as a JSON string (though invalid)
                raise ValueError(
                    f"Fields parameter appears to be a file path but file not found: {fields}"
                )
    elif isinstance(fields, list):
        # Convert list to the required JSON format
        return json.dumps({"_source": fields})
    else:
        raise ValueError(
            f"Fields parameter must be a string (JSON or file path), list of attributes, or None. Got: {type(fields)}"
        )


def get_snp_attributes() -> List[Dict[str, Any]]:
    """
    Retrieve available list of SNP attributes.

    Returns:
        An array of dictionaries containing the available SNP attributes.
    """
    url = f"{BASE_URL}/fastapi/snpAttributes"

    response = requests.post(url)
    response.raise_for_status()

    if 'results' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")
    
    return response.json()["results"]


def get_snps_by_chr(
    chromosome_identifier: str,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[list[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Search for SNPs by chromosome id and position range.

    Args:
        chromosome_identifier: Chromosome id to search (e.g., "1", "2", "X")
        start_position: Start position region of search (default: 1)
        end_position: End position region of search (default: 100000)
        fields: Fields to return, can be JSON string, file path, or list of attributes
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        An array of dictionaries containing the SNP information.
    """
    url = f"{BASE_URL}/fastapi/snp/chr"

    params = {"chromosome_identifier": chromosome_identifier}

    if start_position is not None:
        params["start_position"] = str(start_position)
    if end_position is not None:
        params["end_position"] = str(end_position)

    processed_fields = _process_fields_param(fields)
    if processed_fields is not None:
        params["fields"] = processed_fields

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    # Note: pagination parameters are ignored as they don't function
    # But they are still required by the API (dummy values used)
    params["pagination_from"] = "0"
    params["pagination_size"] = "100"

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def get_snps_by_rsid_list(
    rsid_list: Optional[Union[str, List[str]]] = None,
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[list[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Search for specified list of RSIDs.

    Args:
        rsid_list: List of RSIDs to search, can be comma-separated string or list of strings
        fields: Fields to return, can be JSON string, file path, or list of attributes
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        An array of dictionaries containing the SNP information.
    """
    url = f"{BASE_URL}/fastapi/snp/rsidList"

    params = {}

    if rsid_list is not None:
        if isinstance(rsid_list, list):
            params["rsid_list"] = ",".join(rsid_list)
        else:
            params["rsid_list"] = rsid_list

    processed_fields = _process_fields_param(fields)
    if processed_fields is not None:
        params["fields"] = processed_fields

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    # Note: pagination parameters are ignored as they don't function
    # But they are still required by the API (dummy values used)
    params["pagination_from"] = "0"
    params["pagination_size"] = "100"

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def get_snps_by_gene_product(
    gene: Optional[str] = None,
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[list[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Search for specified gene product; this can be a gene id, gene symbol or UniProt id.

    Args:
        gene: Gene product to search
        fields: Fields to return, can be JSON string, file path, or list of attributes
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        An array of dictionaries containing the SNP information.
    """
    url = f"{BASE_URL}/fastapi/snp/gene_product"

    params = {}

    if gene is not None:
        params["gene"] = gene

    processed_fields = _process_fields_param(fields)
    if processed_fields is not None:
        params["fields"] = processed_fields

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    # Note: pagination parameters are ignored as they don't function
    # But they are still required by the API (dummy values used)
    params["pagination_from"] = "0"
    params["pagination_size"] = "100"

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_chr(
    chromosome_identifier: str,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    filter_fields: Optional[list[str]] = None,
) -> int:
    """
    Count SNPs based on specified chromosome, start position, end position and filter arguments.

    Args:
        chromosome_identifier: The chromosome number (or 'X' for the X-chromosome)
        start_position: Start position region of search (default: 1)
        end_position: End position region of search (default: 100000)
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        The count of SNPs matching the criteria.
    """
    url = f"{BASE_URL}/fastapi/count/chr"

    params = {"chromosome_identifier": chromosome_identifier}

    if start_position is not None:
        params["start_position"] = str(start_position)
    if end_position is not None:
        params["end_position"] = str(end_position)

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_rsid_list(
    rsid_list: Optional[Union[str, List[str]]] = None,
    filter_fields: Optional[list[str]] = None,
) -> int:
    """
    Count the number of SNPs defined in the system that have matching RSIDs from the specified list.

    Args:
        rsid_list: List of RSIDs to search, can be comma-separated string or list of strings
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        The count of SNPs matching the criteria.
    """
    url = f"{BASE_URL}/fastapi/count/rsidList"

    params = {}

    if rsid_list is not None:
        if isinstance(rsid_list, list):
            params["rsid_list"] = ",".join(rsid_list)
        else:
            params["rsid_list"] = rsid_list

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_gene_product(
    gene: Optional[str] = None, filter_fields: Optional[list[str]] = None
) -> int:
    """
    Count the number of SNPs defined in the system that have been associated for the specified gene product.

    Args:
        gene: Gene product to search (gene id, gene symbol or UniProt id)
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        The count of SNPs matching the criteria.
    """
    url = f"{BASE_URL}/fastapi/count/gene_product"

    params = {}

    if gene is not None:
        params["gene"] = gene

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.post(url, params=params)
    response.raise_for_status()

    if 'details' not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]
