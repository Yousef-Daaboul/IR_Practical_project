class Argument:
    doc_id: str
    title: str
    description: str
    conclusion: str

    def __init__(self, doc_id: str, title: str, description: str, conclusion: str):
        super().__init__()
        self.doc_id = doc_id
        self.description = description
        self.title = title
        self.conclusion = conclusion
