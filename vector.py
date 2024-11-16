import logging
from langchain_community.document_loaders import DirectoryLoader, JSONLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomJSONLoader(JSONLoader):
    def _get_text(self, sample):
        # Extract text content from JSON files, assuming `content` key holds the data
        if isinstance(sample, dict):
            if 'content' in sample:  # Update this key based on your JSON structure
                return sample['content']
            else:
                logger.warning("JSON structure does not contain a 'content' key.")
                return json.dumps(sample)  # Fallback: serialize the entire JSON object
        return super()._get_text(sample)

def load_documents(directory: str) -> list:
    """Load documents from the specified directory."""
    loader = DirectoryLoader(
        directory,
        glob="*.json",
        loader_cls=CustomJSONLoader,
        loader_kwargs={'jq_schema': '.'}  # Adjust schema as needed
    )
    logger.debug("Loading data from directory...")
    data = loader.load()
    logger.debug(f"Loaded {len(data)} documents.")
    return data

# Main execution
if __name__ == "__main__":
    # Load JSON documents
    json_directory = '/workspaces/scraper/scraped_data'  # Directory containing JSON files
    documents = load_documents(json_directory)

    # Create embeddings
    embeddings = OllamaEmbeddings(model="mxbai-embed-large", show_progress=True)

    # Create Semantic Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        add_start_index=True,
    )

    # Split documents into chunks
    texts = text_splitter.split_documents(documents)

    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory="./db-hormozi"  # Directory to persist the vector store
    )

    logger.debug("Vectorstore created and saved.")
