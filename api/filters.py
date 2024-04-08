import django_filters

from api.models import CardDeckModel, CardModel, DeckModel


class CardModelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='Name'
    )
    mana_cost = django_filters.CharFilter(
        field_name='mana_cost', lookup_expr='iexact', label='Mana Cost'
    )
    mana_cost_icontains = django_filters.CharFilter(
        field_name='mana_cost',
        lookup_expr='icontains',
        label='Mana Cost (contains)',
    )
    cmc = django_filters.NumberFilter(
        field_name='cmc', lookup_expr='exact', label='CMC'
    )
    cmc_gte = django_filters.NumberFilter(
        field_name='cmc',
        lookup_expr='gte',
        label='CMC Greater Than or Equal To',
    )
    cmc_lte = django_filters.NumberFilter(
        field_name='cmc', lookup_expr='lte', label='CMC Less Than or Equal To'
    )
    type_line = django_filters.CharFilter(
        field_name='type_line', lookup_expr='icontains', label='Type Line'
    )
    rarity = django_filters.ChoiceFilter(
        field_name='rarity',
        lookup_expr='iexact',
        label='Rarity',
        choices=CardModel.RARITY_CHOICES,
    )
    oracle_text = django_filters.CharFilter(
        field_name='oracle_text', lookup_expr='icontains', label='Oracle Text'
    )
    is_land = django_filters.BooleanFilter(
        field_name='is_land', label='Is Land'
    )
    is_cheap_card_draw_spell = django_filters.BooleanFilter(
        field_name='is_cheap_card_draw_spell', label='Is Cheap Card Draw Spell'
    )
    is_cheap_mana_ramp_spell = django_filters.BooleanFilter(
        field_name='is_cheap_mana_ramp_spell', label='Is Cheap Mana Ramp Spell'
    )
    is_land_spell_mdfc = django_filters.BooleanFilter(
        field_name='is_land_spell_mdfc', label='Is Land Spell MDFC'
    )

    class Meta:
        model = CardModel
        fields = [
            'name',
            'mana_cost',
            'mana_cost_icontains',
            'cmc',
            'cmc_gte',
            'cmc_lte',
            'type_line',
            'rarity',
            'oracle_text',
            'is_land',
            'is_cheap_card_draw_spell',
            'is_cheap_mana_ramp_spell',
            'is_land_spell_mdfc',
        ]


class DeckModelFilter(django_filters.FilterSet):
    created_at_date = django_filters.DateFilter(
        field_name='created_at_date', label='Created At Date'
    )
    created_at_datetime = django_filters.DateTimeFilter(
        field_name='created_at_datetime', label='Created At Datetime'
    )
    created_at_date_range = django_filters.DateFromToRangeFilter(
        field_name='created_at_date_range', label='Created At Date Range'
    )
    created_at_datetime_range = django_filters.DateTimeFromToRangeFilter(
        field_name='created_at_datetime_range',
        label='Created At Datetime Range',
    )
    is_commander_deck = django_filters.BooleanFilter(
        field_name='is_commander_deck', label='Is Commander Deck'
    )
    has_companion = django_filters.BooleanFilter(
        field_name='has_companion', label='Has Companion'
    )
    maindeck_card_count = django_filters.NumberFilter(
        field_name='maindeck_card_count',
        lookup_expr='exact',
        label='Maindeck Card Count',
    )
    non_land_card_count = django_filters.NumberFilter(
        field_name='non_land_card_count',
        lookup_expr='exact',
        label='Non-Land Card Count',
    )
    non_land_cmcs_count = django_filters.NumberFilter(
        field_name='non_land_cmcs_count',
        lookup_expr='exact',
        label='Non-Land CMCs Count',
    )
    cheap_card_draw_spell_count = django_filters.NumberFilter(
        field_name='cheap_card_draw_spell_count',
        lookup_expr='exact',
        label='Cheap Card Draw Spell Count',
    )
    cheap_mana_ramp_spell_count = django_filters.NumberFilter(
        field_name='cheap_mana_ramp_spell_count',
        lookup_expr='exact',
        label='Cheap Mana Ramp Spell Count',
    )
    non_mythic_land_spell_mdfc_count = django_filters.NumberFilter(
        field_name='non_mythic_land_spell_mdfc_count',
        lookup_expr='exact',
        label='Non-Mythic Land Spell MDFC Count',
    )
    mythic_land_spell_mdfc_count = django_filters.NumberFilter(
        field_name='mythic_land_spell_mdfc_count',
        lookup_expr='exact',
        label='Mythic Land Spell MDFC Count',
    )
    average_cmc = django_filters.NumberFilter(
        field_name='average_cmc', lookup_expr='exact', label='Average CMC'
    )
    recommended_number_of_lands = django_filters.NumberFilter(
        field_name='recommended_number_of_lands',
        lookup_expr='exact',
        label='Recommended Number of Lands',
    )

    class Meta:
        model = DeckModel
        fields = [
            'created_at_date',
            'created_at_datetime',
            'created_at_date_range',
            'created_at_datetime_range',
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
        ]


class CardDecksFilter(django_filters.FilterSet):
    created_at_date = django_filters.DateFilter(
        field_name='deck__created_at_date', label='Created At Date'
    )
    created_at_datetime = django_filters.DateTimeFilter(
        field_name='deck__created_at_datetime', label='Created At Datetime'
    )
    created_at_date_range = django_filters.DateFromToRangeFilter(
        field_name='deck__created_at_date_range', label='Created At Date Range'
    )
    created_at_datetime_range = django_filters.DateTimeFromToRangeFilter(
        field_name='deck__created_at_datetime_range',
        label='Created At Datetime Range',
    )
    is_commander_deck = django_filters.BooleanFilter(
        field_name='deck__is_commander_deck', label='Is Commander Deck'
    )
    has_companion = django_filters.BooleanFilter(
        field_name='deck__has_companion', label='Has Companion'
    )
    maindeck_card_count = django_filters.NumberFilter(
        field_name='deck__maindeck_card_count',
        lookup_expr='exact',
        label='Maindeck Card Count',
    )
    non_land_card_count = django_filters.NumberFilter(
        field_name='deck__non_land_card_count',
        lookup_expr='exact',
        label='Non-Land Card Count',
    )
    non_land_cmcs_count = django_filters.NumberFilter(
        field_name='deck__non_land_cmcs_count',
        lookup_expr='exact',
        label='Non-Land CMCs Count',
    )
    cheap_card_draw_spell_count = django_filters.NumberFilter(
        field_name='deck__cheap_card_draw_spell_count',
        lookup_expr='exact',
        label='Cheap Card Draw Spell Count',
    )
    cheap_mana_ramp_spell_count = django_filters.NumberFilter(
        field_name='deck__cheap_mana_ramp_spell_count',
        lookup_expr='exact',
        label='Cheap Mana Ramp Spell Count',
    )
    non_mythic_land_spell_mdfc_count = django_filters.NumberFilter(
        field_name='deck__non_mythic_land_spell_mdfc_count',
        lookup_expr='exact',
        label='Non-Mythic Land Spell MDFC Count',
    )
    mythic_land_spell_mdfc_count = django_filters.NumberFilter(
        field_name='deck__mythic_land_spell_mdfc_count',
        lookup_expr='exact',
        label='Mythic Land Spell MDFC Count',
    )
    average_cmc = django_filters.NumberFilter(
        field_name='deck__average_cmc',
        lookup_expr='exact',
        label='Average CMC',
    )
    recommended_number_of_lands = django_filters.NumberFilter(
        field_name='deck__recommended_number_of_lands',
        lookup_expr='exact',
        label='Recommended Number of Lands',
    )

    class Meta:
        model = CardDeckModel
        fields = [
            'created_at_date',
            'created_at_datetime',
            'created_at_date_range',
            'created_at_datetime_range',
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
        ]


class DeckCardsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='card__name', lookup_expr='icontains', label='Name'
    )
    mana_cost = django_filters.CharFilter(
        field_name='card__mana_cost', lookup_expr='iexact', label='Mana Cost'
    )
    mana_cost_icontains = django_filters.CharFilter(
        field_name='card__mana_cost',
        lookup_expr='icontains',
        label='Mana Cost (contains)',
    )
    cmc = django_filters.NumberFilter(
        field_name='card__cmc', lookup_expr='exact', label='CMC'
    )
    cmc_gte = django_filters.NumberFilter(
        field_name='card__cmc',
        lookup_expr='gte',
        label='CMC Greater Than or Equal To',
    )
    cmc_lte = django_filters.NumberFilter(
        field_name='card__cmc',
        lookup_expr='lte',
        label='CMC Less Than or Equal To',
    )
    type_line = django_filters.CharFilter(
        field_name='card__type_line',
        lookup_expr='icontains',
        label='Type Line',
    )
    rarity = django_filters.ChoiceFilter(
        field_name='card__rarity',
        lookup_expr='iexact',
        label='Rarity',
        choices=CardModel.RARITY_CHOICES,
    )
    oracle_text = django_filters.CharFilter(
        field_name='card__oracle_text',
        lookup_expr='icontains',
        label='Oracle Text',
    )
    is_land = django_filters.BooleanFilter(
        field_name='card__is_land', label='Is Land'
    )
    is_cheap_card_draw_spell = django_filters.BooleanFilter(
        field_name='card__is_cheap_card_draw_spell',
        label='Is Cheap Card Draw Spell',
    )
    is_cheap_mana_ramp_spell = django_filters.BooleanFilter(
        field_name='card__is_cheap_mana_ramp_spell',
        label='Is Cheap Mana Ramp Spell',
    )
    is_land_spell_mdfc = django_filters.BooleanFilter(
        field_name='card__is_land_spell_mdfc', label='Is Land Spell MDFC'
    )
    quantity = django_filters.NumberFilter(
        field_name='quantity', lookup_expr='exact', label='Quantity'
    )
    section = django_filters.ChoiceFilter(
        field_name='section',
        lookup_expr='iexact',
        label='Section',
        choices=CardDeckModel.SECTION_CHOICES,
    )

    class Meta:
        model = CardDeckModel
        fields = [
            'name',
            'mana_cost',
            'mana_cost_icontains',
            'cmc',
            'cmc_gte',
            'cmc_lte',
            'type_line',
            'rarity',
            'oracle_text',
            'is_land',
            'is_cheap_card_draw_spell',
            'is_cheap_mana_ramp_spell',
            'is_land_spell_mdfc',
            'quantity',
            'section',
        ]


class DeckCardModelFilter(django_filters.FilterSet):
    card_name = django_filters.CharFilter(
        field_name='card__name', lookup_expr='icontains', label='Card name'
    )
    section = django_filters.ChoiceFilter(
        field_name='section',
        lookup_expr='iexact',
        choices=CardDeckModel.SECTION_CHOICES,
    )

    class Meta:
        model = CardDeckModel
        fields = [
            'card_name',
            'section',
        ]
