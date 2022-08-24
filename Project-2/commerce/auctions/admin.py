from django.contrib import admin

from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user_id", "startingbid", "currentprice", "category")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("item", "user_id", "amount")
    
    @admin.display(empty_value='???')
    def item(self, obj):
        return obj.item_id.title
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "user_id", "comment")
    
    @admin.display(empty_value='???')
    def item(self, obj):
        return obj.item_id.title
    
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("item", "user_id", "winning_bid")
    
    @admin.display(empty_value='???')
    def item(self, obj):
        return obj.item_id.title
    
    @admin.display(empty_value='???')
    def winning_bid(self, obj):
        return obj.item_id.currentprice
    
# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Winner, WinnerAdmin)