
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit


load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "ecommerce.db"


# Get SQLite database
def get_database():

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    db = SQLDatabase.from_uri(
        f"sqlite:///{DB_PATH.as_posix()}"
    )

    return db


# Get SQL toolkit tools
def get_sql_tools():

    db = get_database()

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )

    tools = toolkit.get_tools()

    return tools


# Test
if __name__ == "__main__":

    tools = get_sql_tools()

    print("SQL toolkit initialized!")

    for tool in tools:
        print(tool.name)
