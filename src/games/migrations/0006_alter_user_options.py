# Generated by Django 4.2.16 on 2024-09-29 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0005_alter_list_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["username"]},
        ),
    ]
