from django.contrib import admin

from api.models import CardDeckModel, CardModel, DeckModel


@admin.register(CardModel)
class CardModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'mana_cost',
        'cmc',
        'type_line',
        'rarity',
        'oracle_text',
        'is_land',
        'is_cheap_card_draw_spell',
        'is_cheap_mana_ramp_spell',
        'is_land_spell_mdfc',
    )
    list_display_links = ('id', 'name')
    search_fields = (
        'name',
        'mana_cost',
        'type_line',
        'oracle_text',
    )
    list_filter = (
        'cmc',
        'rarity',
        'is_land',
        'is_cheap_card_draw_spell',
        'is_cheap_mana_ramp_spell',
        'is_land_spell_mdfc',
    )
    ordering = ('name',)
    list_per_page = 20


@admin.register(DeckModel)
class DeckModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'is_commander_deck',
        'has_companion',
        'maindeck_card_count',
        'non_land_card_count',
        'non_land_cmcs_count',
        'cheap_card_draw_spell_count',
        'cheap_mana_ramp_spell_count',
        'non_mythic_land_spell_mdfc_count',
        'mythic_land_spell_mdfc_count',
        'average_cmc',
        'recommended_number_of_lands',
    )
    list_display_links = ('id', 'created_at')
    search_fields = (
        'created_at',
        'maindeck_card_count',
        'non_land_card_count',
        'non_land_cmcs_count',
        'cheap_card_draw_spell_count',
        'cheap_mana_ramp_spell_count',
        'non_mythic_land_spell_mdfc_count',
        'mythic_land_spell_mdfc_count',
        'average_cmc',
        'recommended_number_of_lands',
    )
    list_filter = ('is_commander_deck', 'has_companion')
    ordering = ('created_at',)
    list_per_page = 20


@admin.register(CardDeckModel)
class DeckCardModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'deck', 'card', 'quantity', 'section')
    list_display_links = ('id',)
    search_fields = ('card__name',)
    list_filter = ('section',)
    ordering = ('id',)
    list_per_page = 40
