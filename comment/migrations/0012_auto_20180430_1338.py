# Generated by Django 2.0 on 2018-04-30 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180421_2013'),
        ('comment', '0011_auto_20180423_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='History_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.User')),
                ('viewed_question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='comment.Question')),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='root_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root', to='comment.Comment'),
        ),
    ]