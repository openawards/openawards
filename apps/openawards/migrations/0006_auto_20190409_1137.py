# Generated by Django 2.1.2 on 2019-04-09 09:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('openawards', '0005_auto_20190408_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36),
        ),
    ]
