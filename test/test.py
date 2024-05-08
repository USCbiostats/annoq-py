from src.annoq import annoq

def test_get_SNPs_by_chromosome():
    response = annoq().get_SNPs_by_chromosome(chr="2", start=1, end=10000000, 
                                fields=['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'], 
                                filter=['chr'], page_from=2, page_size=4)
    for elt in response:
        assert elt['chr'] == '2'
        assert elt['pos'] > 1
        assert elt['pos'] < 10000000
        assert elt['ANNOVAR_ensembl_Effect'] == 'intergenic' or 'upstream'


def test_get_SNPs_by_gene_product():
    response = annoq().get_SNPs_by_gene_product(gene="Q9BVC4", fields=["chr", "id"], filter=["chr", "pos"], page_from=0, page_size=10)
    
    for elt in response:
        assert elt['chr'] == '16'


def test_get_SNPs_by_IDs():
    response = annoq().get_SNPs_by_IDs(ids=["2:10632C>A", "16:2255492G>A"], fields=["id", "chr"], filter=["chr"], page_from=0, page_size=5)

    for elt in response:
        assert elt['id'] == "2:10632C>A" or elt['id'] == "16:2255492G>A"


def test_get_SNPs_by_RsID():
    response = annoq().get_SNPs_by_RsID(rsID='rs189126619', fields=["rs_dbSNP151", "ref"], filter=["rs_dbSNP151"], page_from=0, page_size=2)

    for elt in response:
        assert elt['rs_dbSNP151'] == 'rs189126619'
        assert elt['ref'] == 'C'


def test_get_SNPs_by_RsIDs():
    response = annoq().get_SNPs_by_RsIDs(rsIDs=['rs189126619', 'rs115366554'], fields=["rs_dbSNP151", "ref"], filter=["rs_dbSNP151"], page_from=0, page_size=2)

    for elt in response:
        assert elt['rs_dbSNP151'] == 'rs189126619' or elt['rs_dbSNP151'] == 'rs115366554'
        assert elt['ref'] == 'C' or elt['ref'] == 'G'


def test_count_SNPs_by_chromosome():
    response = annoq().count_SNPs_by_chromosome(chr="2", start=1, end=10000000, filter=["chr", "ANNOVAR_ensembl_Closest_gene(intergenic_only)"])
    assert response == 79869


def test_count_SNPs_by_gene_product():
    response = annoq().count_SNPs_by_gene_product(gene="Q9BVC4", filter=["chr", "pos"])
    assert response == 51


def test_count_SNPs_by_IDs():
    response = annoq().count_SNPs_by_IDs(ids=["2:10632C>A", "2:10632C>A"], filter=["chr"])
    assert response == 1


def test_count_SNPs_by_RsID():
    response = annoq().count_SNPs_by_RsID(rsID='rs189126619', filter=["rs_dbSNP151"])
    assert response == 1


def test_count_SNPs_by_RsIDs():
    response = annoq().count_SNPs_by_RsIDs(rsIDs=['rs189126619', 'rs115366554'], filter=["rs_dbSNP151"])
    assert response == 2