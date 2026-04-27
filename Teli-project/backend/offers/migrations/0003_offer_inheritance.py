from django.conf import settings
from django.db import migrations, models


def migrate_offer_data(apps, schema_editor):
    Offer = apps.get_model('offers', 'Offer')
    DailyOffer = apps.get_model('offers', 'DailyOffer')
    SpecialOffer = apps.get_model('offers', 'SpecialOffer')

    for offer in Offer.objects.all():
        if offer.daily_offer_id:
            try:
                daily = DailyOffer.objects.get(pk=offer.daily_offer_id)
            except DailyOffer.DoesNotExist:
                continue
            daily.code = offer.code
            daily.price = offer.price
            daily.configurator_id = offer.configurator_id
            daily.is_active = offer.is_active
            daily.save()
        elif offer.special_offer_id:
            try:
                special = SpecialOffer.objects.get(pk=offer.special_offer_id)
            except SpecialOffer.DoesNotExist:
                continue
            special.code = offer.code
            special.price = offer.price
            special.configurator_id = offer.configurator_id
            special.is_active = offer.is_active
            special.save()


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_offer_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyoffer',
            name='code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='dailyoffer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='dailyoffer',
            name='configurator',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dailyoffer',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='specialoffer',
            name='code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='specialoffer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='specialoffer',
            name='configurator',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='specialoffer',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.RunPython(migrate_offer_data, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='dailyoffer',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='dailyoffer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dailyoffer',
            name='configurator',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dailyoffer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='configurator',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
    ]
