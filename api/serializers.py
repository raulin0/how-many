from rest_framework import serializers

from api.models import CardDeckModel, CardModel, DeckModel


class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = '__all__'


class DeckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckModel
        fields = '__all__'


class CardDeckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDeckModel
        fields = '__all__'


class ListCardDecksSerializer(serializers.ModelSerializer):
    deck = serializers.ReadOnlyField(source='deck.id')

    class Meta:
        model = CardDeckModel
        fields = ['deck']


class ListDeckCardsSerializer(serializers.ModelSerializer):
    card_name = serializers.ReadOnlyField(source='card.name')

    class Meta:
        model = CardDeckModel
        fields = ['section', 'quantity', 'card_name']
