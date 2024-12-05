import pandas
import spacy
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.drawing import Drawing
from app.parser import tree, markup
from nlp.models import TextModel

nlp_var = spacy.load("uk_core_news_sm")


def index(request):
    types_frame = pandas.read_csv("System/syntaxtypes.csv")
    vid_frame = pandas.read_csv("System/sintaxvind.csv")

    text_fk = request.GET.get("text_fk", None)
    sentence = int(request.GET.get("sentence", 1))

    if request.method == "GET":
        if text_fk:
            instance = TextModel.objects.filter(id=text_fk).first()
            if instance:
                tree_frame = pandas.DataFrame(instance.tree_json)
                morf_frame = pandas.DataFrame(instance.morf_json)
                drawing = Drawing(tree_frame, morf_frame, types_frame, vid_frame)
                canvas = drawing.make_canvas(1, sentence)
                return render(request, "index.html", {
                    "canvas": canvas,
                    "text": instance.text,
                    "sentence": sentence,
                    "sentences": instance.sentences,
                    "sentence_prev": (sentence - 1) if sentence > 1 else None,
                    "sentence_next": (sentence+1) if sentence < instance.sentences else None,
                    "text_fk": text_fk
                })

        return render(request, "index.html")

    if request.method == "POST":
        text = request.POST["text"]
        tree_frame = tree(nlp_var, text)
        morf_frame = markup(nlp_var, text)

        sentences = tree_frame["sentence_number"].max()
        instance = TextModel.objects.create(text=text, tree_json=tree_frame.to_dict(orient="records"),
                                            morf_json=morf_frame.to_dict(orient="records"), sentences=sentences)

        return redirect("/?text_fk={}".format(instance.id))

    return HttpResponse("Not found")
