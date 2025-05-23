# Generated by Django 5.2 on 2025-04-15 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0002_alter_bid_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('submitted', 'Отправлено'), ('editor_review', 'На проверке у редактора'), ('sent_for_review', 'Отправлено на рецензию'), ('needs_revision', 'Требуется доработка'), ('re_review', 'Повторная рецензия'), ('accepted', 'Принято к публикации'), ('rejected', 'Отклонено'), ('published', 'Опубликовано')], default='draft', max_length=255),
        ),
    ]
