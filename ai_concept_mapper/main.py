## main.py

from flask import Flask, render_template, request, jsonify
from mindmap import MindMap
from llm_exploration import LLMExploration
from language_support import LanguageSupport
from ontology_database import OntologyDatabase
import os

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.mind_map = MindMap()
        self.llm_exploration = LLMExploration(api_key=os.getenv('OPENAI_API_KEY', 'your-default-api-key'))
        self.language_support = LanguageSupport()
        self.ontology_database = OntologyDatabase()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup the Flask routes for the web application."""
        @self.app.route('/')
        def index():
            concepts = self.ontology_database.load_ontology()
            return render_template('index.html', concepts=concepts)

        @self.app.route('/explore', methods=['POST'])
        def explore():
            concept = request.json.get('concept')
            if not concept:
                return jsonify({'error': 'Concept is required'}), 400
            exploration_data = self.llm_exploration.explore(concept)
            return jsonify(exploration_data)

        @self.app.route('/summary', methods=['POST'])
        def summary():
            concept = request.json.get('concept')
            if not concept:
                return jsonify({'error': 'Concept is required'}), 400
            summary = self.llm_exploration.generate_summary(concept)
            return jsonify({'summary': summary})

        @self.app.route('/flashcards', methods=['POST'])
        def flashcards():
            concept = request.json.get('concept')
            if not concept:
                return jsonify({'error': 'Concept is required'}), 400
            flashcards = self.llm_exploration.generate_flashcards(concept)
            return jsonify({'flashcards': flashcards})

        @self.app.route('/translate', methods=['POST'])
        def translate():
            text = request.json.get('text')
            target_lang = request.json.get('target_lang')
            if not text or not target_lang:
                return jsonify({'error': 'Text and target language are required'}), 400
            translated_text = self.language_support.translate(text, target_lang)
            return jsonify({'translated_text': translated_text})

        @self.app.route('/detect_language', methods=['POST'])
        def detect_language():
            text = request.json.get('text')
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            language = self.language_support.detect_language(text)
            return jsonify({'language': language})

        @self.app.route('/save_ontology', methods=['POST'])
        def save_ontology():
            concepts = request.json.get('concepts')
            if not concepts:
                return jsonify({'error': 'Concepts are required'}), 400
            self.ontology_database.save_ontology(concepts)
            return jsonify({'status': 'success'})

        @self.app.route('/load_ontology', methods=['GET'])
        def load_ontology():
            concepts = self.ontology_database.load_ontology()
            return jsonify({'concepts': concepts})

    def run(self) -> None:
        """Run the Flask web application."""
        self.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main_app = Main()
    main_app.run()
