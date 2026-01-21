"""
Annoq API Python Client

A Python package for accessing SNP data from Annoq.org
"""

import json
import requests
from typing import Union, List, Dict, Any, Optional


# Base URL for the Annoq API
BASE_URL = "https://api-v2.annoq.org"


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


def _download_all_snps(url: str, params: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Helper function to download all SNPs using the download API endpoint.

    Args:
        url: The API endpoint URL for downloading SNPs.
        params: The parameters to be sent with the request.

    Returns:
        An array of dictionaries containing the SNP information.
    """
    params["format"] = "ndjson"

    response = requests.post(url, params=params, stream=True)
    response.raise_for_status()
    snp_list = []
    for line in response.iter_lines():
        if line:
            snp_record = json.loads(line.decode("utf-8"))
            snp_list.append(snp_record)

    return snp_list


def get_snp_attributes() -> List[Dict[str, Any]]:
    """
    Retrieve available list of SNP attributes.

    Returns:
        An array of dictionaries containing the available SNP attributes.
    """
    url = f"{BASE_URL}/snpAttributes"

    response = requests.get(url)
    response.raise_for_status()

    if "results" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["results"]


def get_snps_by_chr(
    chromosome_identifier: str,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[List[str]] = None,
    pagination_from: int = 0,
    pagination_size: int = 1000,
    fetch_all: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search for SNPs by chromosome id and position range using pagination.

    Args:
        chromosome_identifier: Chromosome id to search (e.g., "1", "2", "X")
        start_position: Start position region of search (default: 1)
        end_position: End position region of search (default: 100000)
        fields: Fields to return, can be JSON string, file path, or list of attributes. Number of fields is limited to 20.
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved
        pagination_from: Pagination start index (default: 0)
        pagination_size: Pagination page size (default: 1000)
        fetch_all: If True, retrieves all matching SNPs by downloading all pages (default: False)

    Returns:
        An array of dictionaries containing the SNP information.

    Notes:
        - If fetch_all is True, pagination_from and pagination_size are ignored.
        - The function will return all matching SNPs in a single list.
        - It only supports up to 1,000,000 SNPs being fetched in total.

        - If using pagination (fetch_all=False), you cannot fetch more than the first 10,000 SNPs over all pages.
        - pagination_from + pagination_size must be <= 10,000.

    Raises:
        ValueError: If the response from the server is unexpected.
        ValueError: If fetch_all is False and pagination_from + pagination_size > 10,000.
    """

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

    if fetch_all:
        # Use the download api to fetch all results
        url = f"{BASE_URL}/snp/chr/download"
        return _download_all_snps(url, params)

    if pagination_from < 0 or pagination_size <= 0:
        raise ValueError(
            "pagination_from must be >= 0 and pagination_size must be > 0."
        )

    if pagination_from + pagination_size > 10000:
        raise ValueError(
            "When fetch_all is False, pagination_from + pagination_size must be <= 10,000."
        )

    url = f"{BASE_URL}/snp/chr"

    params["pagination_from"] = str(pagination_from)
    params["pagination_size"] = str(pagination_size)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def get_snps_by_rsid_list(
    rsid_list: Union[str, List[str]],
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[List[str]] = None,
    pagination_from: int = 0,
    pagination_size: int = 1000,
    fetch_all: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search for specified list of RSIDs.

    Args:
        rsid_list: List of RSIDs to search, can be comma-separated string or list of strings
        fields: Fields to return, can be JSON string, file path, or list of attributes. Number of fields is limited to 20.
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved
        pagination_from: Pagination start index (default: 0)
        pagination_size: Pagination page size (default: 1000)
        fetch_all: If True, retrieves all matching SNPs by downloading all pages (default: False)

    Returns:
        An array of dictionaries containing the SNP information.

    Notes:
        - If fetch_all is True, pagination_from and pagination_size are ignored.
        - The function will return all matching SNPs in a single list.
        - It only supports up to 1,000,000 SNPs being fetched in total.

        - If using pagination (fetch_all=False), you cannot fetch more than the first 10,000 SNPs over all pages.
        - pagination_from + pagination_size must be <= 10,000.

    Raises:
        ValueError: If the response from the server is unexpected.
        ValueError: If fetch_all is False and pagination_from + pagination_size > 10,000.
    """
    url = f"{BASE_URL}/snp/rsidList"

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

    if fetch_all:
        # Use the download api to fetch all results
        url = f"{BASE_URL}/snp/rsidList/download"
        return _download_all_snps(url, params)

    if pagination_from < 0 or pagination_size <= 0:
        raise ValueError(
            "pagination_from must be >= 0 and pagination_size must be > 0."
        )

    if pagination_from + pagination_size > 10000:
        raise ValueError(
            "When fetch_all is False, pagination_from + pagination_size must be <= 10,000."
        )

    params["pagination_from"] = str(pagination_from)
    params["pagination_size"] = str(pagination_size)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def get_snps_by_gene_product(
    gene: str,
    fields: Union[str, List[str], None] = None,
    filter_fields: Optional[List[str]] = None,
    pagination_from: int = 0,
    pagination_size: int = 1000,
    fetch_all: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search for specified gene product; this can be a gene id, gene symbol or UniProt id.

    Args:
        gene: Gene product to search
        fields: Fields to return, can be JSON string, file path, or list of attributes. Number of fields is limited to 20.
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved
        pagination_from: Pagination start index (default: 0)
        pagination_size: Pagination page size (default: 1000)
        fetch_all: If True, retrieves all matching SNPs by downloading all pages (default: False)

    Returns:
        An array of dictionaries containing the SNP information.

    Notes:
        - If fetch_all is True, pagination_from and pagination_size are ignored.
        - The function will return all matching SNPs in a single list.
        - It only supports up to 1,000,000 SNPs being fetched in total.

        - If using pagination (fetch_all=False), you cannot fetch more than the first 10,000 SNPs over all pages.
        - pagination_from + pagination_size must be <= 10,000.

    Raises:
        ValueError: If the response from the server is unexpected.
        ValueError: If fetch_all is False and pagination_from + pagination_size > 10,000.
    """
    url = f"{BASE_URL}/snp/gene_product"

    params = {}

    if gene is not None:
        params["gene"] = gene

    processed_fields = _process_fields_param(fields)
    if processed_fields is not None:
        params["fields"] = processed_fields

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    if fetch_all:
        # Use the download api to fetch all results
        url = f"{BASE_URL}/snp/gene_product/download"
        return _download_all_snps(url, params)

    if pagination_from < 0 or pagination_size <= 0:
        raise ValueError(
            "pagination_from must be >= 0 and pagination_size must be > 0."
        )

    if pagination_from + pagination_size > 10000:
        raise ValueError(
            "When fetch_all is False, pagination_from + pagination_size must be <= 10,000."
        )

    params["pagination_from"] = str(pagination_from)
    params["pagination_size"] = str(pagination_size)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_chr(
    chromosome_identifier: str,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    filter_fields: Optional[List[str]] = None,
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
    url = f"{BASE_URL}/count/chr"

    params = {"chromosome_identifier": chromosome_identifier}

    if start_position is not None:
        params["start_position"] = str(start_position)
    if end_position is not None:
        params["end_position"] = str(end_position)

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_rsid_list(
    rsid_list: Union[str, List[str]],
    filter_fields: Optional[List[str]] = None,
) -> int:
    """
    Count the number of SNPs defined in the system that have matching RSIDs from the specified list.

    Args:
        rsid_list: List of RSIDs to search, can be comma-separated string or list of strings
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        The count of SNPs matching the criteria.
    """
    url = f"{BASE_URL}/count/rsidList"

    params = {}

    if rsid_list is not None:
        if isinstance(rsid_list, list):
            params["rsid_list"] = ",".join(rsid_list)
        else:
            params["rsid_list"] = rsid_list

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]


def count_snps_by_gene_product(
    gene: str, filter_fields: Optional[List[str]] = None
) -> int:
    """
    Count the number of SNPs defined in the system that have been associated for the specified gene product.

    Args:
        gene: Gene product to search (gene id, gene symbol or UniProt id)
        filter_fields: SNP attribute labels that should not be empty for the record to be retrieved

    Returns:
        The count of SNPs matching the criteria.
    """
    url = f"{BASE_URL}/count/gene_product"

    params = {}

    if gene is not None:
        params["gene"] = gene

    if filter_fields is not None:
        params["filter_fields"] = ",".join(filter_fields)

    response = requests.get(url, params=params)
    response.raise_for_status()

    if "details" not in response.json():
        raise ValueError(f"Unexpected response from server: {response.json()}")

    return response.json()["details"]
