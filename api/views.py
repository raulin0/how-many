from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.filters import (
    CardDecksFilter,
    CardModelFilter,
    DeckCardModelFilter,
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
from api.utils.parser.decklist import Decklist
from api.utils.parser.parser import DecklistParser


class CardModelViewSet(viewsets.ModelViewSet):
    queryset = CardModel.objects.all()
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
    queryset = DeckModel.objects.all()
    serializer_class = DeckModelSerializer
    ordering_fields = ['created_at']
    filterset_class = DeckModelFilter

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def process(self, request):
        decklist_text = self._extract_decklist_text(request)
        parsed_decklist = self._parse_decklist(decklist_text)
        processed_decklist = self._manage_decklist_data(parsed_decklist)
        response = self._save_deck_data(processed_decklist)

        return response

    def _extract_decklist_text(self, request):
        decklist_text = request.body.decode('utf-8')
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
        try:
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

            for section in processed_decklist.sections:
                for section_card in section.cards:

                    existing_card = CardModel.objects.filter(
                        name=section_card.name
                    ).first()
                    if existing_card:
                        card_instance = existing_card

                    else:
                        card_serializer = CardModelSerializer(
                            data={
                                'name': section_card.name,
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

                    deck_card_serializer = CardDeckModelSerializer(
                        data={
                            'deck': deck_instance.pk,
                            'card': card_instance.pk,
                            'quantity': section_card.quantity,
                            'section': section.name,
                        }
                    )
                    deck_card_serializer.is_valid(raise_exception=True)
                    deck_card_serializer.save()

            return Response(
                deck_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def cards(self, request, pk=None):
        self.queryset = CardDeckModel.objects.filter(deck_id=self.kwargs['pk'])
        self.filterset_class = DeckCardsFilter

        filterset = self.filter_queryset(self.queryset)
        serializer = ListDeckCardsSerializer(filterset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CardDeckModelViewSet(viewsets.ModelViewSet):
    queryset = CardDeckModel.objects.all()
    serializer_class = CardDeckModelSerializer
    ordering_fields = ['id']
    filterset_class = DeckCardModelFilter
