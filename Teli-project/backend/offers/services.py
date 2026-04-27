from django.utils import timezone
from .models import DailyOffer, SpecialOffer


class OfferService:
    @staticmethod
    def list_all_offers():
        return list(DailyOffer.objects.all()) + list(SpecialOffer.objects.all())

    @staticmethod
    def list_active_offers():
        today = timezone.now().date()
        daily = DailyOffer.objects.filter(is_active=True, day=today)
        special = SpecialOffer.objects.filter(is_active=True, start_date__lte=today, end_date__gte=today)
        offers = list(daily) + list(special)
        return offers

    @staticmethod
    def list_daily_offers():
        return DailyOffer.objects.all()

    @staticmethod
    def list_special_offers():
        return SpecialOffer.objects.all()
