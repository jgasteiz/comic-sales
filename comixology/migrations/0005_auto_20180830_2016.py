# Generated by Django 2.1 on 2018-08-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("comixology", "0004_sale_cover_url")]

    operations = [
        migrations.AlterModelOptions(
            name="sale", options={"ordering": ["-created_at", "title"]}
        ),
        migrations.RemoveField(model_name="wishlistcomic", name="cover_url"),
        migrations.AddField(
            model_name="wishlistcomic",
            name="platform_id",
            field=models.IntegerField(null=True),
        ),
    ]
