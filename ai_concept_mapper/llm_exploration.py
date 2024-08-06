## llm_exploration.py

import openai
from typing import Dict, List

class LLMExploration:
    def __init__(self, api_key: str):
        """Initialize the LLMExploration class with the OpenAI API key.

        Args:
            api_key: The OpenAI API key for authentication.
        """
        openai.api_key = api_key

    def explore(self, concept: str) -> Dict[str, str]:
        """Explore a concept using GPT-3 or GPT-4 API.

        Args:
            concept: The concept to be explored.

        Returns:
            A dictionary containing exploration data about the concept.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Explore the concept of {concept}. Provide detailed information.",
            max_tokens=150
        )
        exploration_data = response.choices[0].text.strip()
        return {"concept": concept, "exploration_data": exploration_data}

    def generate_summary(self, concept: str) -> str:
        """Generate a summary for a given concept using GPT-3 or GPT-4 API.

        Args:
            concept: The concept to generate a summary for.

        Returns:
            A string containing the summary of the concept.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the concept of {concept}.",
            max_tokens=50
        )
        summary = response.choices[0].text.strip()
        return summary

    def generate_flashcards(self, concept: str) -> List[Dict[str, str]]:
        """Generate flashcards for a given concept using GPT-3 or GPT-4 API.

        Args:
            concept: The concept to generate flashcards for.

        Returns:
            A list of dictionaries, each containing a question and answer pair.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate flashcards for the concept of {concept}.",
            max_tokens=100
        )
        flashcards_text = response.choices[0].text.strip()
        flashcards = self._parse_flashcards(flashcards_text)
        return flashcards

    def _parse_flashcards(self, flashcards_text: str) -> List[Dict[str, str]]:
        """Parse the flashcards text into a list of question and answer pairs.

        Args:
            flashcards_text: The raw text containing flashcards.

        Returns:
            A list of dictionaries, each containing a question and answer pair.
        """
        flashcards = []
        lines = flashcards_text.split('\n')
        for line in lines:
            if ':' in line:
                question, answer = line.split(':', 1)
                flashcards.append({"question": question.strip(), "answer": answer.strip()})
        return flashcards
