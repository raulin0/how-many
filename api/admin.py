from django.contrib import admin

from api.models import (
    Card,
    Commander,
    Companion,
    Decklist,
    DecklistCard,
    Maindeck,
    Sideboard,
)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(DecklistCard)
class DecklistCardAdmin(admin.ModelAdmin):
    list_display = ['card', 'quantity']


@admin.register(Commander)
class CommanderAdmin(admin.ModelAdmin):
    filter_horizontal = ['commanders_cards']


@admin.register(Companion)
class CompanionAdmin(admin.ModelAdmin):
    list_display = ['companion_card']


@admin.register(Maindeck)
class MaindeckAdmin(admin.ModelAdmin):
    filter_horizontal = ['maindeck_cards']


@admin.register(Sideboard)
class SideboardAdmin(admin.ModelAdmin):
    filter_horizontal = ['sideboard_cards']


@admin.register(Decklist)
class DecklistAdmin(admin.ModelAdmin):
    list_display = ['commanders', 'companion', 'maindeck', 'sideboard']
