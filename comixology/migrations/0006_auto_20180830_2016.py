# Generated by Django 2.1 on 2018-08-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("comixology", "0005_auto_20180830_2016")]

    operations = [
        migrations.AlterField(
            model_name="wishlistcomic",
            name="platform_id",
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        )
    ]
