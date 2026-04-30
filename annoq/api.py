"""
Annoq API Python Client

A Python package for accessing SNP data from Annoq.org
"""

import json
import os
import re
import requests
from typing import Union, List, Dict, Any, Optional


# Base URL for the Annoq API
BASE_URL = "https://api-v2.annoq.org"
DEFAULT_SNPWAY_BASE_URL = "http://snpway.annoq.org"


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


def _resolve_snpway_base_url(base_url: Optional[str]) -> str:
    if base_url and base_url.strip():
        return base_url.strip().rstrip("/")

    env_value = os.getenv("ANNOQ_SNPWAY_BASE_URL", "").strip()
    if env_value:
        return env_value.rstrip("/")

    return DEFAULT_SNPWAY_BASE_URL.rstrip("/")


def _normalize_chromosome_label(raw_chromosome: str) -> str:
    normalized = str(raw_chromosome).strip()
    if not normalized:
        return ""
    return re.sub(r"^chr", "", normalized, flags=re.IGNORECASE)


def _unique_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _parse_vcf_to_ids(vcf_text: str) -> List[str]:
    ids: List[str] = []

    for line in vcf_text.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue

        fields = trimmed.split("\t")
        if len(fields) < 2:
            fields = re.split(r"\s+", trimmed)
        if len(fields) < 2:
            continue

        chrom = _normalize_chromosome_label(fields[0])
        pos = str(fields[1]).strip()

        if not chrom or not pos.isdigit():
            continue

        ids.append(f"{chrom}:{pos}")

    return _unique_preserve_order(ids)


def _normalize_rsid_list(rsid_list: Union[str, List[str]]) -> List[str]:
    if isinstance(rsid_list, list):
        parsed = [str(rsid).strip() for rsid in rsid_list if str(rsid).strip()]
        return _unique_preserve_order(parsed)

    parsed = [
        segment.strip() for segment in re.split(r"[\s,]+", rsid_list) if segment.strip()
    ]
    return _unique_preserve_order(parsed)


def _build_snpway_payload(
    vcf_text: Optional[str],
    chrom_pos_ids: Optional[List[str]],
    chromosome_identifier: Optional[str],
    start_position: Optional[int],
    end_position: Optional[int],
    rsid_list: Union[str, List[str], None],
) -> Dict[str, Any]:
    modes_used = 0

    has_vcf = bool(vcf_text and vcf_text.strip())
    has_chrom_pos = bool(chrom_pos_ids)
    has_region = (
        chromosome_identifier is not None
        or start_position is not None
        or end_position is not None
    )
    has_rsid = rsid_list is not None

    modes_used += 1 if has_vcf else 0
    modes_used += 1 if has_chrom_pos else 0
    modes_used += 1 if has_region else 0
    modes_used += 1 if has_rsid else 0

    if modes_used != 1:
        raise ValueError(
            "Provide exactly one SNP input mode: vcf_text, chrom_pos_ids, "
            "chromosome range (chromosome_identifier/start_position/end_position), "
            "or rsid_list."
        )

    if has_vcf:
        ids = _parse_vcf_to_ids(vcf_text or "")
        if not ids:
            raise ValueError("No valid CHROM/POS entries were found in vcf_text.")
        return {
            "input_type": "ids",
            "idsQuery": {"ids": ids},
        }

    if has_chrom_pos:
        normalized_ids = []
        for raw_id in chrom_pos_ids or []:
            normalized_id = str(raw_id).strip()
            if normalized_id:
                normalized_ids.append(normalized_id)
        normalized_ids = _unique_preserve_order(normalized_ids)
        if not normalized_ids:
            raise ValueError("chrom_pos_ids must contain at least one non-empty ID.")
        return {
            "input_type": "ids",
            "idsQuery": {"ids": normalized_ids},
        }

    if has_region:
        if (
            chromosome_identifier is None
            or start_position is None
            or end_position is None
        ):
            raise ValueError(
                "chromosome_identifier, start_position, and end_position are required "
                "when using chromosome range input mode."
            )

        normalized_chr = _normalize_chromosome_label(chromosome_identifier)
        if not normalized_chr:
            raise ValueError("chromosome_identifier cannot be empty.")

        return {
            "input_type": "chromosome",
            "chrQuery": {
                "chr": normalized_chr,
                "start": int(start_position),
                "end": int(end_position),
            },
        }

    normalized_rsids = _normalize_rsid_list(rsid_list or [])
    if not normalized_rsids:
        raise ValueError("rsid_list must contain at least one rsID.")

    return {
        "input_type": "rsIdList",
        "rsIdListQuery": {"rsIdList": normalized_rsids},
    }


def _parse_error_detail(response: requests.Response) -> str:
    try:
        response_payload = response.json()
        if isinstance(response_payload, dict) and "detail" in response_payload:
            return str(response_payload["detail"])
    except ValueError:
        pass

    fallback = response.text.strip()
    if fallback:
        return fallback

    return f"Request failed with status {response.status_code}."


def _post_snpway_request(
    endpoint: str,
    payload: Dict[str, Any],
    base_url: Optional[str],
    timeout_seconds: int,
) -> Dict[str, Any]:
    resolved_base_url = _resolve_snpway_base_url(base_url)
    url = f"{resolved_base_url}{endpoint}"

    try:
        response = requests.post(url, json=payload, timeout=timeout_seconds)
    except requests.RequestException as exc:
        raise ValueError(f"Failed to reach SNPWay API at {url}: {exc}") from exc

    if not response.ok:
        raise ValueError(_parse_error_detail(response))

    try:
        response_data = response.json()
    except ValueError as exc:
        raise ValueError("SNPWay API returned a non-JSON response.") from exc

    if not isinstance(response_data, dict):
        raise ValueError("SNPWay API returned an unexpected response shape.")

    return response_data


def _build_snpway_mapping_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mapping": {
            "gene_list": response_data.get("gene_list", []),
            "variant_gene_map": response_data.get("rsId_genes_map", {}),
        },
        "panther": {
            "gene_info": response_data.get("panther_gene_info", {}),
            "gene_to_panther_map": response_data.get("gene_panther_mapping", {}),
        },
    }


def _get_relevant_columns(annotation_dataset: Optional[str]) -> List[str]:
    base_columns = ["rsId", "PANTHER_ID", "mappedGenes"]

    all_columns = [
        *base_columns,
        "PANTHER_family",
        "PANTHER_Subfamily",
        "PANTHER_Pathway",
        "Protein_Class",
        "Reactome_Pathway",
        "GO_database_MF_complete",
        "GO_database_BP_complete",
        "GO_database_CC_complete",
        "PANTHER_GO_slim_Molecular_Function",
        "PANTHER_GO_slim_Biological_Process",
        "PANTHER_GO_slim_Cellular_Component",
    ]

    if annotation_dataset is None:
        return all_columns

    dataset_column_map = {
        "GO:0008150": [*base_columns, "GO_database_BP_complete"],
        "GO:0003674": [*base_columns, "GO_database_MF_complete"],
        "GO:0005575": [*base_columns, "GO_database_CC_complete"],
        "ANNOT_TYPE_ID_PANTHER_PATHWAY": [*base_columns, "PANTHER_Pathway"],
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_MF": [
            *base_columns,
            "PANTHER_GO_slim_Molecular_Function",
        ],
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_BP": [
            *base_columns,
            "PANTHER_GO_slim_Biological_Process",
        ],
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_CC": [
            *base_columns,
            "PANTHER_GO_slim_Cellular_Component",
        ],
        "ANNOT_TYPE_ID_PANTHER_PC": [*base_columns, "Protein_Class"],
        "ANNOT_TYPE_ID_REACTOME_PATHWAY": [*base_columns, "Reactome_Pathway"],
    }

    return dataset_column_map.get(annotation_dataset, all_columns)


def _create_results_table_data(
    response_data: Dict[str, Any],
    panther_ids_to_include: Optional[List[str]] = None,
    annotation_dataset: Optional[str] = None,
) -> List[Dict[str, Any]]:
    rs_id_genes_map = response_data.get("rsId_genes_map", {})
    panther_gene_info = response_data.get("panther_gene_info", {})
    gene_panther_mapping = response_data.get("gene_panther_mapping", {})

    if not isinstance(rs_id_genes_map, dict):
        rs_id_genes_map = {}
    if not isinstance(panther_gene_info, dict):
        panther_gene_info = {}
    if not isinstance(gene_panther_mapping, dict):
        gene_panther_mapping = {}

    panther_ids_set = (
        set(panther_ids_to_include) if panther_ids_to_include is not None else None
    )
    table_data: List[Dict[str, Any]] = []
    processed_pairs: set[str] = set()

    for rs_id, genes_for_rs_id in rs_id_genes_map.items():
        if not isinstance(genes_for_rs_id, list):
            continue

        for gene in genes_for_rs_id:
            panther_ids_for_gene = gene_panther_mapping.get(gene, [])
            if not isinstance(panther_ids_for_gene, list):
                continue

            for panther_id in panther_ids_for_gene:
                panther_id = str(panther_id).strip()
                if not panther_id:
                    continue

                if panther_ids_set is not None and panther_id not in panther_ids_set:
                    continue

                pair_key = f"{rs_id}-{panther_id}"
                if pair_key in processed_pairs:
                    continue
                processed_pairs.add(pair_key)

                mapped_genes = [
                    mapped_gene
                    for mapped_gene in genes_for_rs_id
                    if panther_id in gene_panther_mapping.get(mapped_gene, [])
                ]

                gene_info = panther_gene_info.get(panther_id)
                if not isinstance(gene_info, dict):
                    continue

                table_data.append(
                    {
                        "rsId": rs_id,
                        "PANTHER_ID": panther_id,
                        "mappedGenes": mapped_genes,
                        "PANTHER_family": gene_info.get("PANTHER_family", ""),
                        "PANTHER_Subfamily": gene_info.get("PANTHER_Subfamily", ""),
                        "PANTHER_Pathway": gene_info.get("PANTHER_Pathway", ""),
                        "Protein_Class": gene_info.get("Protein_Class", ""),
                        "Reactome_Pathway": gene_info.get("Reactome_Pathway", ""),
                        "GO_database_MF_complete": gene_info.get(
                            "GO_database_MF_complete", ""
                        ),
                        "GO_database_BP_complete": gene_info.get(
                            "GO_database_BP_complete", ""
                        ),
                        "GO_database_CC_complete": gene_info.get(
                            "GO_database_CC_complete", ""
                        ),
                        "PANTHER_GO_slim_Molecular_Function": gene_info.get(
                            "PANTHER_GO_slim_Molecular_Function", ""
                        ),
                        "PANTHER_GO_slim_Biological_Process": gene_info.get(
                            "PANTHER_GO_slim_Biological_Process", ""
                        ),
                        "PANTHER_GO_slim_Cellular_Component": gene_info.get(
                            "PANTHER_GO_slim_Cellular_Component", ""
                        ),
                    }
                )

    if annotation_dataset is None:
        return table_data

    selected_columns = _get_relevant_columns(annotation_dataset)
    return [
        {column: row.get(column, "") for column in selected_columns}
        for row in table_data
    ]


def _get_significant_results(
    rows: List[Dict[str, Any]], correction: str
) -> List[Dict[str, Any]]:
    correction_name = str(correction).upper()

    if correction_name == "FDR":
        return [row for row in rows if float(row.get("fdr", 0.0)) < 0.05]

    return [row for row in rows if float(row.get("pValue", 0.0)) < 0.05]


def _get_significant_genes(rows: List[Dict[str, Any]]) -> List[str]:
    unique_rows_by_term: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        key = str(row.get("termId") or row.get("process") or "")
        if key and key not in unique_rows_by_term:
            unique_rows_by_term[key] = row

    genes: List[str] = []
    seen_genes = set()
    for row in unique_rows_by_term.values():
        for gene in row.get("mapped_ids", []):
            normalized_gene = str(gene).strip()
            if normalized_gene and normalized_gene not in seen_genes:
                seen_genes.add(normalized_gene)
                genes.append(normalized_gene)

    return genes


def _build_panther_id_filter_from_genes(
    gene_panther_mapping: Dict[str, Any], genes_to_include: Optional[List[str]]
) -> List[str]:
    if genes_to_include is None:
        return []

    normalized_genes = [
        gene.strip() for gene in genes_to_include if gene and gene.strip()
    ]
    if not normalized_genes:
        return []

    panther_ids: List[str] = []
    seen_panther_ids = set()

    for gene in normalized_genes:
        for panther_id in gene_panther_mapping.get(gene, []):
            normalized_panther_id = str(panther_id).strip()
            if normalized_panther_id and normalized_panther_id not in seen_panther_ids:
                seen_panther_ids.add(normalized_panther_id)
                panther_ids.append(normalized_panther_id)

    return panther_ids


def get_snpway_gene_mappings(
    *,
    vcf_text: Optional[str] = None,
    chrom_pos_ids: Optional[List[str]] = None,
    chromosome_identifier: Optional[str] = None,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    rsid_list: Union[str, List[str], None] = None,
    base_url: Optional[str] = None,
    timeout_seconds: int = 120,
) -> Dict[str, Any]:
    """
    Run SNPWay mapping workflow and return SNP-to-gene and PANTHER mappings.

    Exactly one input mode must be provided:
    - vcf_text
    - chrom_pos_ids
    - chromosome range (chromosome_identifier, start_position, end_position)
    - rsid_list

    Returns:
        dict: A nested response with these top-level keys:
            - mapping.gene_list: List of unique genes found in the input SNPs.
            - mapping.variant_gene_map: Mapping from SNP ID (rsID or chr:pos) to associated genes.
            - panther.gene_info: PANTHER annotations (families, pathways, GO terms) for each gene.
            - panther.gene_to_panther_map: Mapping from gene symbol to PANTHER protein family ID.
    """

    payload = _build_snpway_payload(
        vcf_text=vcf_text,
        chrom_pos_ids=chrom_pos_ids,
        chromosome_identifier=chromosome_identifier,
        start_position=start_position,
        end_position=end_position,
        rsid_list=rsid_list,
    )

    response_data = _post_snpway_request(
        endpoint="/workflow/gene_mappings",
        payload=payload,
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )

    return _build_snpway_mapping_response(response_data)


def run_snpway_overrepresentation_workflow(
    *,
    annot_data_set: str = "GO:0008150",
    correction: str = "FDR",
    enrichment_test_type: str = "FISHER",
    vcf_text: Optional[str] = None,
    chrom_pos_ids: Optional[List[str]] = None,
    chromosome_identifier: Optional[str] = None,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None,
    rsid_list: Union[str, List[str], None] = None,
    base_url: Optional[str] = None,
    timeout_seconds: int = 300,
) -> Dict[str, Any]:
    """
    Run full SNPWay overrepresentation workflow and return normalized outputs.

    The backend response is compact; this helper adds convenience views locally.

    Returns:
        dict: A nested response with these top-level keys:
            - mapping.gene_list: List of unique genes found in the input SNPs.
            - mapping.variant_gene_map: Mapping from SNP ID (rsID or chr:pos) to associated genes.
            - panther.gene_info: PANTHER annotations (families, pathways, GO terms) for each gene.
            - panther.gene_to_panther_map: Mapping from gene symbol to PANTHER protein family ID.
            - overrepresentation.results: All enrichment analysis results from PANTHER.
            - overrepresentation.significant_results: Only results meeting the significance threshold (FDR or p-value).
            - overrepresentation.settings: Analysis parameters (annotation dataset, correction method, test type).
            - overrepresentation.significance_cutoff: The p-value/FDR threshold used to filter significant results.
            - csv.all_mappings: Table of all SNP-gene-PANTHER associations with selected columns.
            - csv.all_mappings_all_columns: Table of all SNP-gene-PANTHER associations with complete annotations.
            - csv.significant_mappings: Table of significant enrichment results with selected columns.
            - csv.significant_mappings_all_columns: Table of significant enrichment results with complete annotations.
    """

    payload = _build_snpway_payload(
        vcf_text=vcf_text,
        chrom_pos_ids=chrom_pos_ids,
        chromosome_identifier=chromosome_identifier,
        start_position=start_position,
        end_position=end_position,
        rsid_list=rsid_list,
    )

    payload["annotDataSet"] = annot_data_set
    payload["correction"] = correction
    payload["enrichmentTestType"] = enrichment_test_type

    response_data = _post_snpway_request(
        endpoint="/workflow/overrepresentation",
        payload=payload,
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )

    overrepresentation_results = response_data.get("overrepresentation_results", [])
    if not isinstance(overrepresentation_results, list):
        overrepresentation_results = []

    significant_results = _get_significant_results(
        overrepresentation_results, correction
    )
    significant_genes = _get_significant_genes(significant_results)
    significant_panther_ids = _build_panther_id_filter_from_genes(
        response_data.get("gene_panther_mapping", {}), significant_genes
    )

    significance_field = "fdr" if str(correction).upper() == "FDR" else "pValue"

    return {
        **_build_snpway_mapping_response(response_data),
        "overrepresentation": {
            "results": overrepresentation_results,
            "significant_results": significant_results,
            "settings": {
                "annot_data_set": annot_data_set,
                "correction": correction,
                "enrichment_test_type": enrichment_test_type,
            },
            "significance_cutoff": {
                "field": significance_field,
                "p_value": 0.05,
            },
        },
        "csv": {
            "all_mappings": _create_results_table_data(
                response_data,
                annotation_dataset=annot_data_set,
            ),
            "all_mappings_all_columns": _create_results_table_data(
                response_data,
                annotation_dataset=None,
            ),
            "significant_mappings": _create_results_table_data(
                response_data,
                panther_ids_to_include=significant_panther_ids,
                annotation_dataset=annot_data_set,
            ),
            "significant_mappings_all_columns": _create_results_table_data(
                response_data,
                panther_ids_to_include=significant_panther_ids,
                annotation_dataset=None,
            ),
        },
    }
