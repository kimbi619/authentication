import spacy

class NamedEntities:
    @staticmethod
    def getName(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        return doc
