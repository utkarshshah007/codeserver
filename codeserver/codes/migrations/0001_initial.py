# Generated by Django 2.1.5 on 2019-02-05 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('max_uses_per_ticket', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redemption_datetime', models.DateTimeField(auto_now_add=True)),
                ('redemption_location', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Scanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('location', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=36)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('max_uses', models.IntegerField(blank=True, null=True)),
                ('bundle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codes.Bundle')),
            ],
        ),
        migrations.AddField(
            model_name='redemption',
            name='scanner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='codes.Scanner'),
        ),
        migrations.AddField(
            model_name='redemption',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codes.Ticket'),
        ),
    ]