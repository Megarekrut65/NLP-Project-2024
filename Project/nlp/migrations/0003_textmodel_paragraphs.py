# Generated by Django 5.1.4 on 2024-12-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0002_rename_morf_file_textmodel_morf_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='textmodel',
            name='paragraphs',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
