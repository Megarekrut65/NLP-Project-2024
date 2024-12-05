import django.db.models as models


class TextModel(models.Model):
    text = models.TextField()
    tree_json = models.JSONField()
    morf_json = models.JSONField()
    sentences = models.IntegerField()
    paragraphs = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
