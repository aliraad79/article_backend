# Generated by Django 5.0.6 on 2024-06-12 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_article_text_vote_created_at_vote_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='vote',
            new_name='score',
        ),
    ]
