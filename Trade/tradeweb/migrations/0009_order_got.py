# Generated by Django 3.2 on 2021-04-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeweb', '0008_order_beforeorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='got',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
