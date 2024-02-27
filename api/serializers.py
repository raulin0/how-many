from rest_framework import serializers

from api.models import (
    Card,
    Commander,
    Companion,
    Decklist,
    DecklistCard,
    Maindeck,
    Sideboard,
)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class DecklistCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecklistCard
        fields = '__all__'


class CommanderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commander
        fields = '__all__'


class CompanionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companion
        fields = '__all__'


class MaindeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maindeck
        fields = '__all__'


class SideboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sideboard
        fields = '__all__'


class DecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decklist
        fields = '__all__'
