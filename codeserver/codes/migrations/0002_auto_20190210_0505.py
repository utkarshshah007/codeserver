# Generated by Django 2.1.5 on 2019-02-10 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.CharField(max_length=36, unique=True),
        ),
    ]
