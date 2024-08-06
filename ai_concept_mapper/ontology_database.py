## ontology_database.py

import sqlite3
from typing import Dict

class OntologyDatabase:
    def __init__(self, db_path: str = 'ontology.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Create the ontology table if it doesn't exist."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ontology (
                id INTEGER PRIMARY KEY,
                concept TEXT NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def save_ontology(self, concepts: Dict[str, str]) -> None:
        """Save the ontology data to the database.

        Args:
            concepts: A dictionary where the key is the concept and the value is the associated data.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.executemany('''
            INSERT INTO ontology (concept, data) VALUES (?, ?)
            ON CONFLICT(concept) DO UPDATE SET data=excluded.data
        ''', concepts.items())
        connection.commit()
        connection.close()

    def load_ontology(self) -> Dict[str, str]:
        """Load the ontology data from the database.

        Returns:
            A dictionary where the key is the concept and the value is the associated data.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT concept, data FROM ontology')
        rows = cursor.fetchall()
        connection.close()
        return {concept: data for concept, data in rows}
