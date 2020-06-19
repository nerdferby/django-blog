# Generated by Django 3.0.7 on 2020-06-19 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("like", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(
                fields=("post", "user"), name="like-post-user"
            ),
        ),
    ]
