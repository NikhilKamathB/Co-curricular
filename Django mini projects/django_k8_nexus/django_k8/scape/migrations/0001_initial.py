# Generated by Django 3.2.3 on 2021-06-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScapeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file_data', models.FileField(upload_to='django_k8/scape/')),
            ],
            options={
                'verbose_name_plural': 'Scaple Model',
            },
        ),
    ]