from django.contrib import admin

from .models import Auctions, User, Comments, Bids

# Register your models here.

admin.site.register(Auctions)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Bids)