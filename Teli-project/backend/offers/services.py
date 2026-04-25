from django.db.models import Q
from django.utils import timezone
from .models import DailyOffer, SpecialOffer, Offer


class OfferService:
    @staticmethod
    def list_all_offers():
        return Offer.objects.all()

    @staticmethod
    def list_active_offers():
        today = timezone.now().date()
        offers = Offer.objects.filter(is_active=True).filter(
            (Q(daily_offer__day=today)) |
            (Q(special_offer__start_date__lte=today, special_offer__end_date__gte=today))
        ).distinct()
        return offers

    @staticmethod
    def list_daily_offers():
        return DailyOffer.objects.all()

    @staticmethod
    def list_special_offers():
        return SpecialOffer.objects.all()
