# Generated by Django 3.2 on 2021-04-26 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tradeweb', '0004_messages_msgtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='goodID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tradeweb.goods'),
            preserve_default=False,
        ),
    ]
