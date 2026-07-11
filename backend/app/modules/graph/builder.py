from neo4j import GraphDatabase, exceptions
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class Neo4jConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
            cls._instance.driver = None
            cls._instance._init_driver()
        return cls._instance

    def _init_driver(self):
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            self.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j")
        except exceptions.ServiceUnavailable:
            logger.error("Failed to connect to Neo4j. Ensure database is running and credentials are correct.")
        except Exception as e:
            logger.error(f"Neo4j connection error: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

neo4j_conn = Neo4jConnection()
