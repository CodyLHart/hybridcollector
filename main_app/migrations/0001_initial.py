# Generated by Django 3.0.2 on 2020-03-17 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hybrid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('animal', models.CharField(max_length=100)),
                ('produce', models.CharField(max_length=100)),
            ],
        ),
    ]
