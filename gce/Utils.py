import spacy

class NamedEntities:
    @staticmethod
    def getName(text):
        date = ''
        person = ''
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                date = ent.text.split()[1]
            if ent.label_ == 'ORG':
                person = ent.text

        return date, person
