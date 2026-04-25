from django.contrib import admin
from .models import DailyOffer, SpecialOffer, Offer

admin.site.register(DailyOffer)
admin.site.register(SpecialOffer)
admin.site.register(Offer)  