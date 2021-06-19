# Generated by Django 3.1.7 on 2021-06-19 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20210619_0740'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sale_number',
        ),
        migrations.RemoveField(
            model_name='product',
            name='special_offer',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='category.category'),
        ),
    ]