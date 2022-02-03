from django.conf import settings


def subs_prices(request):
    return {'BRONZE_PRICE': settings.STRIPE_PRICE_ID_BRONZE}
