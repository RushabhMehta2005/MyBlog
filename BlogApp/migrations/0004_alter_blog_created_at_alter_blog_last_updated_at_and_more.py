# Generated by Django 5.0.6 on 2024-07-05 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("BlogApp", "0003_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="blog",
            name="last_updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="blog",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="BlogApp.blog",
            ),
        ),
    ]
