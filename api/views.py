from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from api.filters import DecklistFilter
from api.models import (
    Card,
    Commander,
    Companion,
    Decklist,
    DecklistCard,
    Maindeck,
    Sideboard,
)
from api.serializers import (
    CardSerializer,
    CommanderSerializer,
    CompanionSerializer,
    DecklistCardSerializer,
    DecklistSerializer,
    MaindeckSerializer,
    SideboardSerializer,
)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['name']
    search_fields = ['name']


class DecklistCardViewSet(viewsets.ModelViewSet):
    queryset = DecklistCard.objects.all()
    serializer_class = DecklistCardSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['quantity']
    search_fields = ['card__name']


class CommanderViewSet(viewsets.ModelViewSet):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['commanders_cards__card__name']
    search_fields = ['commanders_cards__card__name']


class CompanionViewSet(viewsets.ModelViewSet):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['companion_cards__card__name']
    search_fields = ['companion_cards__card__name']


class MaindeckViewSet(viewsets.ModelViewSet):
    queryset = Maindeck.objects.all()
    serializer_class = MaindeckSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['maindeck_cards__card__name']
    search_fields = ['maindeck_cards__card__name']


class SideboardViewSet(viewsets.ModelViewSet):
    queryset = Sideboard.objects.all()
    serializer_class = SideboardSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['sideboard_cards__card__name']
    search_fields = ['sideboard_cards__card__name']


class DecklistViewSet(viewsets.ModelViewSet):
    queryset = Decklist.objects.all()
    serializer_class = DecklistSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['decklist_cards__card__name']
    search_fields = ['decklist_cards__card__name']
    filterset_class = DecklistFilter
