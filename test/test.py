from src.annoq import annoq

def test_GetSNPsByChromosome():
    response = annoq().GetSNPsByChromosome(chr="2", start=1, end=10000000, 
                                fields=['chr', 'ref', 'pos', 'rs_dbSNP151', 'ANNOVAR_ensembl_Effect', 'ANNOVAR_refseq_Effect'], 
                                filter=['chr'], page_from=2, page_size=4)
    for elt in response:
        assert elt['chr'] == '2'
        assert elt['pos'] > 1
        assert elt['pos'] < 10000000
        assert elt['ANNOVAR_ensembl_Effect'] == 'intergenic'


def test_GetSNPsByGeneProduct():
    response = annoq().GetSNPsByGeneProduct(gene="Q9BVC4", fields=["chr", "id"], filter=["chr", "pos"], page_from=0, page_size=10)
    
    for elt in response:
        assert elt['chr'] == '16'