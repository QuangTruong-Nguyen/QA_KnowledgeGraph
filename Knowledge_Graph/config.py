import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from langchain_community.graphs import Neo4jGraph
import instructor
import os
from dotenv import load_dotenv



config = GenerationConfig(
    temperature=0,
    # max_tokens=128,  # Optional: Maximum number of tokens to generate
    # stop_sequences=["<|endoftext|>"]  # Optional: Stop generation at these sequences
)


def configure_setup():
    load_dotenv()

    # Set up Neo4J & Gemini API
    os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI")
    os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USERNAME")
    os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD")
    os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

    neo4j_graph = Neo4jGraph()

    # Set up Gemini Flash API
    genai.configure(api_key = os.environ["GEMINI_API_KEY"]) # alternative API key configuration

    # Create Gemini Client
    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
            generation_config= config# model defaults to "gemini-pro"
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    return neo4j_graph , client