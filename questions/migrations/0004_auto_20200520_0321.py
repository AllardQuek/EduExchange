# Generated by Django 3.0.6 on 2020-05-20 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20200519_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
