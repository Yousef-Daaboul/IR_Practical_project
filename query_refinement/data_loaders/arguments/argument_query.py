class ArgumentQuery:
    query_id: str
    title: str
    description: str
    narrative: str

    def __init__(self, query_id: str, title: str, description: str, narrative: str):
        self.query_id = query_id
        self.title = title
        self.description = description
        self.narrative = narrative