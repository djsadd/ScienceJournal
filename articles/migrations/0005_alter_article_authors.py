# Generated by Django 5.2 on 2025-04-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
