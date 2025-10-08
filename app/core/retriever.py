from langchain_chroma import Chroma, vectorstores
from langchain_huggingface import HuggingFaceEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_langchain_db")

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs)



vector_store = Chroma(
    collection_name="collection",
    embedding_function=EMBEDDING_MODEL,
    persist_directory=CHROMA_DIR,
    collection_metadata={"hnsw:space": "cosine"}
)

ROOT_FOLDERS = [
    "events",
    "food_festivals",
    "general_info_&_history",
    "museums",
    "music",
    "sports",
    "tax",
    "operating_budget"
]

def get_context(query, k = 3):
  """
  Args:
    - query ,str: the user's query
    - root_folders ,List[str]: list of strings indicating the top root folders
    - k, int: number of chunks returned

  retrieve the docs that will be used by the LLM

  Returns:
  - context , List[str]: list of chunks
  """

  root_embeds = EMBEDDING_MODEL.embed_documents(ROOT_FOLDERS)
  query_embedding = EMBEDDING_MODEL.embed_query(query)
  # a dict mapping folder names with their cosine similarty with query
  cosine_sims = {}
  for i, embed in enumerate(root_embeds):
    sim = vectorstores.cosine_similarity([embed], [query_embedding])
    cosine_sims.update({ROOT_FOLDERS[i]: sim[0] })

  cosine_sims = list(sorted(cosine_sims.items(), key=lambda item: item[1], reverse=True))

  result  = vector_store.similarity_search_with_relevance_scores(query,
                                                          k = 3,
                                                          filter={
                                                              "root_folder": cosine_sims[0][0]
                                                              })

  context = []
  for res in result:
    context.append(res[0].page_content)

  return context
