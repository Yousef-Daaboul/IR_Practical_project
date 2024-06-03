class ClinicalQuery:
    query_id: str
    disease: str
    gene: str
    demographic: str
    other: str

    def __init__(self, query_id: str, disease: str, gene: str, demographic: str, other: str):
        self.query_id = query_id
        self.disease = disease
        self.gene = gene
        self.demographic = demographic
        self.other = other

