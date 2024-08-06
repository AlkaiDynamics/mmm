## language_support.py

from googletrans import Translator

class LanguageSupport:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to the target language.

        Args:
            text: The text to be translated.
            target_lang: The language code to translate the text into.

        Returns:
            The translated text.
        """
        translated = self.translator.translate(text, dest=target_lang)
        return translated.text

    def detect_language(self, text: str) -> str:
        """Detect the language of the given text.

        Args:
            text: The text whose language needs to be detected.

        Returns:
            The detected language code.
        """
        detected = self.translator.detect(text)
        return detected.lang
