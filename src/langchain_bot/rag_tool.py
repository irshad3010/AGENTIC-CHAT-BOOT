
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# 8.1 Imports and module cache
# --------------------------------------------------

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

POLICY_DIR = PROJECT_ROOT / "policies"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

_vector_store = None


# --------------------------------------------------
# 8.2 Load policy documents
# --------------------------------------------------

def load_policy_documents():

    documents = []

    if not POLICY_DIR.exists():
        raise FileNotFoundError(
            f"Policies folder not found: {POLICY_DIR}"
        )

    policy_files = list(POLICY_DIR.glob("*.txt"))

    if not policy_files:
        raise FileNotFoundError(
            f"No .txt policy files found in {POLICY_DIR}"
        )

    for file_path in policy_files:

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        loaded_documents = loader.load()

        for document in loaded_documents:
            document.metadata["source"] = file_path.name

        documents.extend(loaded_documents)

    print(f"Loaded {len(documents)} policy documents.")

    return documents


# --------------------------------------------------
# 8.3 Split documents into chunks
# --------------------------------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} policy chunks.")

    return chunks


# --------------------------------------------------
# 8.4 Get or create Chroma vector store
# --------------------------------------------------

def get_vector_store():

    global _vector_store

    if _vector_store is not None:
        return _vector_store

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Reuse an existing vector database
    if any(CHROMA_DIR.iterdir()):

        print("Loading existing ChromaDB...")

        _vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name="shopease_policies"
        )

        print("Loaded existing ChromaDB.")

    else:

        print("Building new ChromaDB...")

        documents = load_policy_documents()

        chunks = split_documents(documents)

        _vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(CHROMA_DIR),
            collection_name="shopease_policies"
        )

        print("ChromaDB created successfully.")

    return _vector_store


# --------------------------------------------------
# 8.5 Policy search tool
# --------------------------------------------------

@tool
def search_policies(query: str) -> str:
    """
    Search ShopEase policy and FAQ documents.

    Use this tool for policy and FAQ questions only,
    such as returns, shipping, and refunds.

    Do not use this tool to retrieve individual user
    orders, order status, customer information, or tickets.
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=4
    )

    if not results:
        return "No relevant policy information was found."

    formatted_results = []

    for index, document in enumerate(results, start=1):

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        formatted_results.append(
            f"Source: {source}\n"
            f"Policy information:\n{document.page_content}"
        )

    return "\n\n---\n\n".join(formatted_results)


# --------------------------------------------------
# 8.6 Public initializer and exports
# --------------------------------------------------

def initialize_vector_store():
    """Initialize the policy vector database at startup."""

    return get_vector_store()


__all__ = [
    "search_policies",
    "initialize_vector_store",
    "load_policy_documents",
    "split_documents",
    "get_vector_store"
]
