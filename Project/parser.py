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
    return f"{token.dep_}-{head.dep_}-{token.pos_}"


def markup(nlp, path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

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

    output_file = "syntactic_analysis.tsv"
    df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

    print(f"Файл збережено: {output_file}")


def tree(nlp, path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

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

    output_file = "tree_structure.tsv"
    df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

    print(f"Файл збережено: {output_file}")


if __name__ == "__main__":
    nlp = spacy.load("uk_core_news_sm")
    input_text_file = "text_ІВАН ДРАЧ.txt"

    markup(nlp, input_text_file)
    tree(nlp, input_text_file)
