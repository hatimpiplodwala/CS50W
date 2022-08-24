from django.contrib import admin

from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("user_id", "title", "startingbid", "currentprice", "category")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("user_id", "item", "amount")
    
    @admin.display(empty_value='???')
    def item(self, obj):
        return obj.item_id.title
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_id", "item", "comment")
    
    @admin.display(empty_value='???')
    def item(self, obj):
        return obj.item_id.title
    
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("user_id", "item", "winning_bid")
    
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