# Generated by Django 4.1.3 on 2022-11-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_alter_room_amenities_alter_room_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='country',
            field=models.CharField(choices=[('default', '나라 선택하기'), ('한국', '한국'), ('미국', '미국'), ('일본', '일본')], default='default', max_length=100),
        ),
    ]