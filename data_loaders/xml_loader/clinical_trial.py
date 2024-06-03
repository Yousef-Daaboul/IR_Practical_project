class ClinicalTrial:
    doc_id: str
    description: str
    title: str
    summary: str

    def __init__(self, doc_id: str, title: str, description: str, summary: str):
        super().__init__()
        self.doc_id = doc_id
        self.description = description
        self.title = title
        self.summary = summary
