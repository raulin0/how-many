from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.filters import (
    CardDeckModelFilter,
    CardDecksFilter,
    CardModelFilter,
    DeckCardsFilter,
    DeckModelFilter,
)
from api.models import CardDeckModel, CardModel, DeckModel
from api.serializers import (
    CardDeckModelSerializer,
    CardModelSerializer,
    DeckModelSerializer,
    ListCardDecksSerializer,
    ListDeckCardsSerializer,
)
from api.utils.manager import DecklistDataManager
from api.utils.parser.card import Card
from api.utils.parser.decklist import Decklist
from api.utils.parser.parser import DecklistParser
from api.utils.parser.section import Section


class CardModelViewSet(viewsets.ModelViewSet):
    queryset = CardModel.objects.all().order_by('id')
    serializer_class = CardModelSerializer
    ordering_fields = ['name']
    filterset_class = CardModelFilter

    @action(detail=True, methods=['get'])
    def decks(self, request, pk=None):
        self.queryset = CardDeckModel.objects.filter(card_id=self.kwargs['pk'])
        self.filterset_class = CardDecksFilter

        filterset = self.filter_queryset(self.queryset)
        serializer = ListCardDecksSerializer(filterset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeckModelViewSet(viewsets.ModelViewSet):
    queryset = DeckModel.objects.all().order_by('id')
    serializer_class = DeckModelSerializer
    ordering_fields = ['created_at']
    filterset_class = DeckModelFilter

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def process(self, request):
        try:
            decklist_text = self._extract_decklist_text(request)
            parsed_decklist = self._parse_decklist(decklist_text)
            processed_decklist = self._manage_decklist_data(parsed_decklist)
            response = self._save_deck_data(processed_decklist)

            return response

        except ValueError as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def _extract_decklist_text(self, request):
        decklist_text = request.data['decklist_text']
        if not decklist_text:
            raise ParseError('Decklist text is empty')

        return decklist_text

    def _parse_decklist(self, decklist_text: str):
        parser = DecklistParser(decklist_text)

        return parser._parse_deck()

    def _manage_decklist_data(self, parsed_decklist: Decklist):
        manager = DecklistDataManager(parsed_decklist)
        manager.process_decklist()

        return manager.decklist

    def _save_deck_data(self, processed_decklist: Decklist):
        deck_serializer, deck_instance = self._save_deck_info(
            processed_decklist
        )

        for section in processed_decklist.sections:
            for section_card in section.cards:

                existing_card = self._get_existing_card(section_card)

                if existing_card:
                    card_instance = existing_card
                else:
                    card_instance = self._save_card_info(section_card)

                self._save_card_deck_info(
                    deck_instance, card_instance, section_card, section
                )

        return Response(deck_serializer.data, status=status.HTTP_201_CREATED)

    def _save_deck_info(self, processed_decklist: Decklist):
        deck_serializer = self.serializer_class(
            data={
                'is_commander_deck': processed_decklist.is_commander_deck,
                'has_companion': processed_decklist.has_companion,
                'maindeck_card_count': processed_decklist.maindeck_card_count,
                'non_land_card_count': processed_decklist.non_land_card_count,
                'non_land_cmcs_count': processed_decklist.non_land_cmcs_count,
                'cheap_card_draw_spell_count': processed_decklist.cheap_card_draw_spell_count,
                'cheap_mana_ramp_spell_count': processed_decklist.cheap_mana_ramp_spell_count,
                'non_mythic_land_spell_mdfc_count': processed_decklist.non_mythic_land_spell_mdfc_count,
                'mythic_land_spell_mdfc_count': processed_decklist.mythic_land_spell_mdfc_count,
                'average_cmc': processed_decklist.average_cmc,
                'recommended_number_of_lands': processed_decklist.recommended_number_of_lands,
            }
        )

        deck_serializer.is_valid(raise_exception=True)
        deck_instance = deck_serializer.save()

        return deck_serializer, deck_instance

    def _get_existing_card(self, section_card: Card):
        existing_card = CardModel.objects.filter(
            name=section_card.name
        ).first()

        return existing_card

    def _save_card_info(self, section_card: Card):
        card_serializer = CardModelSerializer(
            data={
                'name': section_card.name,
                'layout': section_card.layout,
                'mana_cost': section_card.mana_cost,
                'cmc': section_card.cmc,
                'type_line': section_card.type_line,
                'rarity': section_card.rarity,
                'oracle_text': section_card.oracle_text,
                'is_land': section_card.is_land,
                'is_cheap_card_draw_spell': section_card.is_cheap_card_draw_spell,
                'is_cheap_mana_ramp_spell': section_card.is_cheap_mana_ramp_spell,
                'is_land_spell_mdfc': section_card.is_land_spell_mdfc,
            }
        )
        card_serializer.is_valid(raise_exception=True)
        card_instance = card_serializer.save()

        return card_instance

    def _save_card_deck_info(
        self,
        deck_instance: list,
        card_instance: CardModel | list,
        section_card: Card,
        section: Section,
    ):
        deck_card_serializer = CardDeckModelSerializer(
            data={
                'section': section.name,
                'quantity': section_card.quantity,
                'card': card_instance.pk,
                'deck': deck_instance.pk,
            }
        )
        deck_card_serializer.is_valid(raise_exception=True)
        deck_card_serializer.save()

    @action(detail=True, methods=['get'])
    def cards(self, request, pk=None):
        self.queryset = CardDeckModel.objects.filter(deck_id=self.kwargs['pk'])
        self.filterset_class = DeckCardsFilter

        filterset = self.filter_queryset(self.queryset)
        serializer = ListDeckCardsSerializer(filterset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CardDeckModelViewSet(viewsets.ModelViewSet):
    queryset = CardDeckModel.objects.all().order_by('id')
    serializer_class = CardDeckModelSerializer
    ordering_fields = ['id']
    filterset_class = CardDeckModelFilter
