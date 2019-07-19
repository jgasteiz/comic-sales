# Generated by Django 2.1 on 2018-08-28 13:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("comixology", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="sale", options={"ordering": ["date_end", "title"]}
        ),
        migrations.AddField(
            model_name="sale",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
