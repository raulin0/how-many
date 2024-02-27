from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DecklistCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity}x {self.card}'


class Commander(models.Model):
    commanders_cards = models.ManyToManyField(DecklistCard)

    def __str__(self):
        return ', '.join(str(card) for card in self.commanders_cards.all())


class Companion(models.Model):
    companion_card = models.ForeignKey(DecklistCard, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.companion_card)


class Maindeck(models.Model):
    maindeck_cards = models.ManyToManyField(DecklistCard)

    def __str__(self):
        return ', '.join(str(card) for card in self.maindeck_cards.all())


class Sideboard(models.Model):
    sideboard_cards = models.ManyToManyField(DecklistCard)

    def __str__(self):
        return ', '.join(str(card) for card in self.sideboard_cards.all())


class Decklist(models.Model):
    commanders = models.ForeignKey(Commander, on_delete=models.CASCADE)
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE)
    maindeck = models.ForeignKey(Maindeck, on_delete=models.CASCADE)
    sideboard = models.ForeignKey(Sideboard, on_delete=models.CASCADE)

    def __str__(self):
        return f'Commander: {self.commanders}, Companion: {self.companion}, Maindeck: {self.maindeck}, Sideboard: {self.sideboard}'
