# Generated by Django 3.0.6 on 2020-05-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('core', '0001_initial'), ('core', '0002_auto_20200513_1816')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('file_type', models.PositiveIntegerField(choices=[(0, 'Text'), (1, 'Markdown'), (2, 'Binary')])),
                ('content', models.FileField(unique=True, upload_to='')),
            ],
        ),
    ]