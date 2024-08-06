## mindmap.py

from typing import Dict
import json

class MindMap:
    def __init__(self):
        self.concepts = {}

    def render_map(self, concepts: Dict[str, str]) -> None:
        """Render the mind map with the given concepts.

        Args:
            concepts: A dictionary where the key is the concept and the value is the associated data.
        """
        self.concepts = concepts
        print("Rendering mind map with the following concepts:")
        print(json.dumps(self.concepts, indent=2))

    def add_node(self, concept: str, data: str) -> None:
        """Add a node to the mind map.

        Args:
            concept: The concept to be added.
            data: The associated data for the concept.
        """
        self.concepts[concept] = data
        print(f"Added node: {concept} with data: {data}")

    def remove_node(self, concept: str) -> None:
        """Remove a node from the mind map.

        Args:
            concept: The concept to be removed.
        """
        if concept in self.concepts:
            del self.concepts[concept]
            print(f"Removed node: {concept}")
        else:
            print(f"Node {concept} does not exist in the mind map.")
