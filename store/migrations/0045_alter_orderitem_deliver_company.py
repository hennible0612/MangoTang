# Generated by Django 3.2.12 on 2022-03-25 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_alter_productreview_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='deliver_company',
            field=models.CharField(blank=True, choices=[('04', 'CJ대한통운'), ('05', '한진택배'), ('08', '롯데택배'), ('06', '로젠택배'), ('01', '우체국택배'), ('46', 'CU편의점택배'), ('24', 'GS Postbox 택배\t')], max_length=200, null=True),
        ),
    ]