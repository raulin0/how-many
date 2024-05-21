import unittest
from unittest.mock import MagicMock, patch

from django.test import TestCase

from api.utils.manager import DecklistDataManager
from api.utils.parser.card import Card
from api.utils.parser.parser import DecklistParser


class TestDecklistDataManager(TestCase):
    def setUp(self):
        decklist_text = """Deck
1 Archfiend of the Dross
3 Blightstep Pathway
4 Blood Crypt
2 Fatal Push
4 Bloodtithe Harvester
1 Duress
3 Dusk Legion Zealot
4 Fable of the Mirror-Breaker
4 Mutavault
1 Go for the Throat
1 Heartless Act
2 Hive of the Eye Tyrant
2 Swamp
4 Sulfurous Springs
2 Preacher of the Schism
4 Sorin, Imperious Bloodlord
2 Thoughtseize
1 Mountain
1 Takenuma, Abandoned Mire
1 Thoughtseize
4 Vein Ripper
2 Archfiend of the Dross
4 Blackcleave Cliffs
2 Fatal Push
1 Thoughtseize

Sideboard
1 Duress
1 Gix's Command
1 Grafdigger's Cage
2 Liliana of the Veil
2 Damping Sphere
2 Path of Peril
1 Quakebringer
1 Duress
4 Leyline of the Void
"""
        decklist = DecklistParser(decklist_text)
        self.manager = DecklistDataManager(decklist)

        self.section_card = Card(
            name='Thoughtseize',
            quantity=4,
            layout='',
            mana_cost='',
            cmc=0.0,
            type_line='',
            rarity='',
            oracle_text='',
            is_land=False,
            is_cheap_card_draw_spell=False,
            is_cheap_mana_ramp_spell=False,
            is_land_spell_mdfc=False,
        )

        self.fetched_card_data = {
            'name': 'Thoughtseize',
            'layout': 'normal',
            'mana_cost': '{B}',
            'cmc': 1.0,
            'type_line': 'Sorcery',
            'rarity': 'rare',
            'oracle_text': 'Target player reveals their hand. You choose a nonland card from it. That player discards that card. You lose 2 life.',
            'is_land': False,
            'is_cheap_card_draw_spell': False,
            'is_cheap_mana_ramp_spell': False,
            'is_land_spell_mdfc': False,
        }

    @patch('api.utils.manager.CardModel.objects.filter')
    @patch('api.utils.manager.DecklistDataManager._get_database_card_data')
    def test__get_or_fetch_card_data_call__get_database_card_data(
        self, mock_get_database_card_data, mock_filter
    ):
        """Test that the database is queried when fetching card data."""
        mock_filter.return_value.first.return_value = MagicMock()

        self.manager._get_or_fetch_card_data(self.section_card)

        mock_get_database_card_data.assert_called_once_with(
            self.section_card, mock_filter.return_value.first.return_value
        )

    @patch('api.utils.manager.CardModel.objects.filter')
    @patch('api.utils.manager.DecklistDataManager._get_scryfall_card_data')
    def test__get_or_fetch_card_data_call__get_scryfall_card_data(
        self, mock_get_scryfall_card_data, mock_filter
    ):
        """Test that Scryfall is queried when card data is not found in the database."""
        mock_filter.return_value.first.return_value = None

        self.manager._get_or_fetch_card_data(self.section_card)
        mock_get_scryfall_card_data.assert_called_once_with(self.section_card)

    def test__get_database_card_data_get_card_properties(self):
        """Test that card properties are correctly set from database data."""
        database_card = MagicMock()
        database_card.name = 'Thoughtseize'
        database_card.layout = 'normal'
        database_card.mana_cost = '{B}'
        database_card.cmc = 1.0
        database_card.type_line = 'Sorcery'
        database_card.rarity = 'rare'
        database_card.oracle_text = 'Target player reveals their hand. You choose a nonland card from it. That player discards that card. You lose 2 life.'
        database_card.is_land = False
        database_card.is_cheap_card_draw_spell = False
        database_card.is_cheap_mana_ramp_spell = False
        database_card.is_land_spell_mdfc = False

        self.manager._get_database_card_data(self.section_card, database_card)

        self.assertEqual(self.section_card.name, database_card.name)
        self.assertEqual(self.section_card.layout, database_card.layout)
        self.assertEqual(self.section_card.mana_cost, database_card.mana_cost)
        self.assertEqual(self.section_card.cmc, database_card.cmc)
        self.assertEqual(self.section_card.type_line, database_card.type_line)
        self.assertEqual(self.section_card.rarity, database_card.rarity)
        self.assertEqual(
            self.section_card.oracle_text, database_card.oracle_text
        )
        self.assertEqual(self.section_card.is_land, database_card.is_land)
        self.assertEqual(
            self.section_card.is_cheap_card_draw_spell,
            database_card.is_cheap_card_draw_spell,
        )
        self.assertEqual(
            self.section_card.is_cheap_mana_ramp_spell,
            database_card.is_cheap_mana_ramp_spell,
        )
        self.assertEqual(
            self.section_card.is_land_spell_mdfc,
            database_card.is_land_spell_mdfc,
        )

    @patch('api.utils.manager.DecklistDataManager._is_land_spell_mdfc')
    @patch('api.utils.manager.DecklistDataManager._is_cheap_mana_ramp_spell')
    @patch('api.utils.manager.DecklistDataManager._is_cheap_card_draw_spell')
    @patch('api.utils.manager.DecklistDataManager._is_land')
    @patch('api.utils.manager.DecklistDataManager._get_oracle_text')
    @patch('api.utils.manager.DecklistDataManager._get_rarity')
    @patch('api.utils.manager.DecklistDataManager._get_type_line')
    @patch('api.utils.manager.DecklistDataManager._get_cmc')
    @patch('api.utils.manager.DecklistDataManager._get_mana_cost')
    @patch('api.utils.manager.DecklistDataManager._get_layout')
    @patch('api.utils.manager.DecklistDataManager._get_name')
    @patch('api.utils.manager.DecklistDataManager._fetch_card_data')
    def test__get_scryfall_card_data_get_card_properties(
        self,
        mock_fetch_card_data,
        mock_get_name,
        mock_get_layout,
        mock_get_mana_cost,
        mock_get_cmc,
        mock_get_type_line,
        mock_get_rarity,
        mock_get_oracle_text,
        mock_is_land,
        mock_is_cheap_card_draw_spell,
        mock_is_cheap_mana_ramp_spell,
        mock_is_land_spell_mdfc,
    ):
        """Test that card properties are correctly set from Scryfall data."""
        mock_fetch_card_data.return_value = self.fetched_card_data
        mock_get_name.return_value = mock_fetch_card_data.return_value['name']
        mock_get_layout.return_value = mock_fetch_card_data.return_value[
            'layout'
        ]
        mock_get_mana_cost.return_value = mock_fetch_card_data.return_value[
            'mana_cost'
        ]
        mock_get_cmc.return_value = mock_fetch_card_data.return_value['cmc']
        mock_get_type_line.return_value = mock_fetch_card_data.return_value[
            'type_line'
        ]
        mock_get_rarity.return_value = mock_fetch_card_data.return_value[
            'rarity'
        ]
        mock_get_oracle_text.return_value = mock_fetch_card_data.return_value[
            'oracle_text'
        ]
        mock_is_land.return_value = mock_fetch_card_data.return_value[
            'is_land'
        ]
        mock_is_cheap_card_draw_spell.return_value = (
            mock_fetch_card_data.return_value['is_cheap_card_draw_spell']
        )
        mock_is_cheap_mana_ramp_spell.return_value = (
            mock_fetch_card_data.return_value['is_cheap_mana_ramp_spell']
        )
        mock_is_land_spell_mdfc.return_value = (
            mock_fetch_card_data.return_value['is_land_spell_mdfc']
        )

        self.manager._get_scryfall_card_data(self.section_card)

        mock_fetch_card_data.assert_called_once_with(self.section_card.name)
        mock_get_name.assert_called_once_with(
            mock_fetch_card_data.return_value
        )
        mock_get_layout.assert_called_once_with(
            mock_fetch_card_data.return_value
        )
        mock_get_mana_cost.assert_called_once_with(
            self.section_card.layout, mock_fetch_card_data.return_value
        )
        mock_get_cmc.assert_called_once_with(mock_fetch_card_data.return_value)
        mock_get_type_line.assert_called_once_with(
            mock_fetch_card_data.return_value
        )
        mock_get_rarity.assert_called_once_with(
            mock_fetch_card_data.return_value
        )
        mock_get_oracle_text.assert_called_once_with(
            self.section_card.layout, mock_fetch_card_data.return_value
        )

        section_card_type_line_lower = self.section_card.type_line.lower()
        section_card_layout_lower = self.section_card.layout.lower()
        mock_is_land.assert_called_once_with(
            section_card_type_line_lower,
            section_card_layout_lower,
            mock_fetch_card_data.return_value,
        )
        section_card_oracle_text_lower = self.section_card.oracle_text.lower()
        mock_is_cheap_card_draw_spell.assert_called_once_with(
            self.section_card.cmc,
            section_card_oracle_text_lower,
            section_card_type_line_lower,
            self.section_card.is_land,
        )
        mock_is_cheap_mana_ramp_spell.assert_called_once_with(
            self.section_card.cmc,
            section_card_type_line_lower,
            section_card_oracle_text_lower,
            self.section_card.is_land,
            self.section_card.is_cheap_card_draw_spell,
        )
        mock_is_land_spell_mdfc.assert_called_once_with(
            self.section_card.is_land,
            section_card_layout_lower,
            self.fetched_card_data,
        )

        self.assertEqual(self.section_card.name, mock_get_name.return_value)
        self.assertEqual(
            self.section_card.layout, mock_get_layout.return_value
        )
        self.assertEqual(
            self.section_card.mana_cost, mock_get_mana_cost.return_value
        )
        self.assertEqual(self.section_card.cmc, mock_get_cmc.return_value)
        self.assertEqual(
            self.section_card.type_line, mock_get_type_line.return_value
        )
        self.assertEqual(
            self.section_card.rarity, mock_get_rarity.return_value
        )
        self.assertEqual(
            self.section_card.oracle_text, mock_get_oracle_text.return_value
        )
        self.assertEqual(self.section_card.is_land, mock_is_land.return_value)
        self.assertEqual(
            self.section_card.is_cheap_card_draw_spell,
            mock_is_cheap_card_draw_spell.return_value,
        )
        self.assertEqual(
            self.section_card.is_cheap_mana_ramp_spell,
            mock_is_cheap_mana_ramp_spell.return_value,
        )
        self.assertEqual(
            self.section_card.is_land_spell_mdfc,
            mock_is_land_spell_mdfc.return_value,
        )

    @patch('api.utils.manager.requests.get')
    def test__fetch_card_data_success(self, mock_get):
        """Test that card data is fetched successfully."""
        mock_get.return_value.json.return_value = self.fetched_card_data

        card_data = self.manager._fetch_card_data('Thoughtseize')

        self.assertEqual(card_data, mock_get.return_value.json.return_value)


if __name__ == '__main__':
    unittest.main()
