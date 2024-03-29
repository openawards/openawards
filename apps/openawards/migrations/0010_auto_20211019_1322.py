# Generated by Django 2.1.2 on 2021-10-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openawards', '0009_auto_20191001_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='authorship',
            field=models.CharField(choices=[('Y', 'Yes, I am the author, have permission, or the license authorizes this.'), ('N', "No, I don't own these rights, but I still want to upload this work, knowing that it might betransferred to another person or removed from the awards if there's a claim."), ('M', "I don't know if I'm allowed or not to enroll this work to the awards, but I still want to upload this work, knowing that it might be transferred to another person or removed from the awards if there's a claim.")], max_length=1),
        ),
    ]
