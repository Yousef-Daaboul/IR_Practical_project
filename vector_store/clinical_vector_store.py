from pinecone import Pinecone


def get_vector_store_index(index_name):
    pc = Pinecone(api_key='e07a8850-6879-43dd-8087-c4841a61d2fd')

    return pc.Index(index_name)

