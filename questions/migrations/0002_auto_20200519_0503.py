# Generated by Django 3.0.6 on 2020-05-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='question',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='downvotes',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvotes',
            field=models.PositiveIntegerField(),
        ),
    ]
