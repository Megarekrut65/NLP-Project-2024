import pandas
import spacy
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.drawing import Drawing
from app.parser import tree, markup
from nlp.models import TextModel

nlp_var = spacy.load("uk_core_news_sm")


def handle_text(text):
    tree_frame = tree(nlp_var, text)
    morf_frame = markup(nlp_var, text)

    sentences = tree_frame["sentence_number"].max()
    paragraphs = tree_frame["TextFK"].max()
    instance = TextModel.objects.create(text=text, tree_json=tree_frame.to_dict(orient="records"),
                                        morf_json=morf_frame.to_dict(orient="records"), sentences=sentences,
                                        paragraphs=paragraphs)

    return instance


def create_page(request, text_id, text_fk, sentence, types_frame, vid_frame):
    if text_fk:
        instance = TextModel.objects.filter(id=text_id).first()
        if instance:
            tree_frame = pandas.DataFrame(instance.tree_json)
            sentences = tree_frame[tree_frame["TextFK"] == text_fk]["sentence_number"].max()
            morf_frame = pandas.DataFrame(instance.morf_json)
            drawing = Drawing(tree_frame, morf_frame, types_frame, vid_frame)
            canvas = drawing.make_canvas(text_fk, sentence)

            return render(request, "handler.html", {
                "canvas": canvas,
                "text": instance.text,
                "sentence": sentence,
                "sentences": sentences,
                "sentence_prev": (sentence - 1) if sentence > 1 else None,
                "sentence_next": (sentence + 1) if sentence < sentences else None,
                "text_fk": text_fk,
                "text_fk_prev": (text_fk - 1) if text_fk > 1 else None,
                "text_fk_next": (text_fk + 1) if text_fk < instance.paragraphs else None,
                "text_id": text_id,
                "paragraphs": instance.paragraphs
            })

    return render(request, "handler.html")


def handler_view(request):
    types_frame = pandas.read_csv("System/syntaxtypes.csv")
    vid_frame = pandas.read_csv("System/sintaxvind.csv")

    text_id = request.GET.get("text_id", None)
    text_fk = int(request.GET.get("text_fk", 1))
    sentence = int(request.GET.get("sentence", 1))

    if request.method == "GET":
        return create_page(request, text_id, text_fk, sentence, types_frame, vid_frame)

    return HttpResponse("Not found")


def index_view(request):
    if request.method == "POST":
        text_id = request.POST.get("text_id", None)
        if not text_id:
            instance = handle_text(request.POST.get("text"))
            text_id = instance.id

        return redirect("/handler?text_id={}".format(text_id))

    if request.method == "GET":
        return render(request, "index.html")

    return HttpResponse("Not found")
