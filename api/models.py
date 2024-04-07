from django.db import models


class CardModel(models.Model):
    RARITY_CHOICES = [
        ('common', 'common'),
        ('uncommon', 'uncommon'),
        ('rare', 'rare'),
        ('mythic', 'mythic'),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    mana_cost = models.CharField(max_length=20, blank=True)
    cmc = models.FloatField()
    type_line = models.CharField(max_length=100)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    oracle_text = models.TextField(blank=True)
    is_land = models.BooleanField()
    is_cheap_card_draw_spell = models.BooleanField()
    is_cheap_mana_ramp_spell = models.BooleanField()
    is_land_spell_mdfc = models.BooleanField()

    class Meta:
        verbose_name = 'Card'

    def __str__(self):
        return self.name


class DeckModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_commander_deck = models.BooleanField()
    has_companion = models.BooleanField()
    maindeck_card_count = models.IntegerField()
    non_land_card_count = models.IntegerField()
    non_land_cmcs_count = models.FloatField()
    cheap_card_draw_spell_count = models.IntegerField()
    cheap_mana_ramp_spell_count = models.IntegerField()
    non_mythic_land_spell_mdfc_count = models.IntegerField()
    mythic_land_spell_mdfc_count = models.IntegerField()
    average_cmc = models.FloatField()
    recommended_number_of_lands = models.IntegerField()

    class Meta:
        verbose_name = 'Deck'

    def __str__(self):
        return f'Deck created at {self.created_at}'


class CardDeckModel(models.Model):
    SECTION_CHOICES = [
        ('commander', 'commander'),
        ('companion', 'companion'),
        ('deck', 'deck'),
        ('sideboard', 'sideboard'),
    ]

    section = models.CharField(
        max_length=20, choices=SECTION_CHOICES, blank=False, null=False
    )
    quantity = models.IntegerField(blank=False, null=False, default=1)
    card = models.ForeignKey(
        CardModel, on_delete=models.CASCADE, related_name='decks'
    )
    deck = models.ForeignKey(
        DeckModel, on_delete=models.CASCADE, related_name='cards'
    )

    class Meta:
        verbose_name = 'Card-Deck Association'

    def __str__(self):
        return f'{self.quantity}x {self.card.name} in {self.deck} ({self.section})'
