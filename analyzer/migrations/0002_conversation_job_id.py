# Generated by Django 4.0 on 2021-12-12 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='job_id',
            field=models.CharField(default=54, max_length=255),
            preserve_default=False,
        ),
    ]
