import spacy
import pandas as pd

def pos_code(pos):
    pos_map = {
        "NOUN": "ЙВ", "VERB": "ГЕ", "ADJ": "АС", "ADV": "Н0",
        "ADP": "ПР", "CCONJ": "СС", "DET": "ОС", "PRON": "МИ",
        "NUM": "ЧН", "PUNCT": "", "PART": "Ь0", "SCONJ": "МС",
        "PROPN": "ЙК", "AUX": "ГР", "INTJ": "Ґ0", "SYM": "СМ",
    }
    return pos_map.get(pos, "XX")  # XX для невідомих тегів


def create_ct(token, head):
    dep_to_ct = {
        "nsubj": "КЗ",  # Координаційний зв'язок
        "case": "ПП",  # Прийменникова сполука
        "obl": "ІП" if "AdpType=Prep" in token.morph else "ІС",  # Prepositional or not
        "amod": "АС",  # Adjective modification
        "advmod": "РС",  # Adverbial modification
        "conj": "СУ",  # Сурядна сполука
        "cc": "СУ",  # Coordinating conjunction
        "obj": "ДП" if "Case=Acc" in token.morph else "ДС",  # Accusative vs other objects
        "xcomp": "ДІ",  # Infinitival complement
        "advcl": "0D",  # Adverbial clause
        "vocative": "ЗВ",  # Звертання
    }

    ct = dep_to_ct.get(token.dep_, "XX")

    if ct == "XX":
        if "Aspect=Perf" in token.morph and token.pos_ == "VERB":
            ct = "ГБ"
        elif token.pos_ == "NUM" and token.dep_ == "nummod":
            ct = "ЧП"
        elif token.pos_ == "NUM" and token.dep_ == "compound":
            ct = "ЧС"

    return ct


def markup(nlp, text):
    paragraphs = text.split("\n\n")

    data = []
    for fk_id, paragraph in enumerate(paragraphs, start=1):
        doc = nlp(paragraph)
        for sent_id, sentence in enumerate(doc.sents, start=1):
            for token in sentence:
                row = {
                    "word": token.text,
                    "code": pos_code(token.pos_),
                    "lemm": token.lemma_,
                    "text_fk": fk_id,
                    "sentence_number": sent_id,
                    "word_Id": token.i + 1,
                }
                data.append(row)

    df = pd.DataFrame(data)

    return df


def tree(nlp, text):
    paragraphs = text.split("\n\n")

    rows = []
    word_counter = 0
    for fk_id, paragraph in enumerate(paragraphs, start=1):
        doc = nlp(paragraph)
        for sent_id, sentence in enumerate(doc.sents, start=1):
            for token in sentence:
                word_counter += 1
                w1 = word_counter
                w2 = word_counter + 1 if token.head != token else word_counter
                ct = create_ct(token, token.head)
                vidn = 1.0 if token.dep_ != "ROOT" else 0.0  # Вага зв'язку
                comm = token.text if token.dep_ == "ROOT" else None
                rows.append({
                    "TextFK": fk_id,
                    "w1": w1,
                    "w2": w2,
                    "ct": ct,
                    "sentence_number": sent_id,
                    "vidn": vidn,
                    "comm": comm
                })

    df = pd.DataFrame(rows)

    return df

