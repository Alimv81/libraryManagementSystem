# Generated by Django 5.0.4 on 2024-05-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0002_alter_book_author_remove_borrowrecord_due_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="role",
            field=models.TextField(default="Member"),
        ),
    ]
