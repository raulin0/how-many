import unittest

from api.utils.parser.parser import DecklistParser


class TestDecklistParser(unittest.TestCase):
    def test__parse_deck_separates_the_decklist_sections(self):
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
        parser = DecklistParser(decklist_text)
        decklist = parser._parse_deck()

        self.assertEqual(len(decklist.sections), 2)

    def test__extract_section_the_section_name_from_the_content(self):
        section_text = """Deck
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
"""
        parser = DecklistParser('')
        section = parser._extract_section(section_text)

        self.assertEqual(section.name, 'deck')
        self.assertEqual(len(section.cards), 21)

    def test__parse_card_without_set_code_and_number_separates_the_card_quantity_from_the_name(
        self,
    ):
        line = '4 Vein Ripper'
        parser = DecklistParser('')
        card = parser._parse_card(line)

        self.assertEqual(card.quantity, 4)
        self.assertEqual(card.name, 'Vein Ripper')

    def test__parse_card_with_set_code_and_number_separates_the_card_quantity_from_the_name(
        self,
    ):
        line = '4 Vein Ripper (MKM) 110'
        parser = DecklistParser('')
        card = parser._parse_card(line)

        self.assertEqual(card.quantity, 4)
        self.assertEqual(card.name, 'Vein Ripper')


if __name__ == '__main__':
    unittest.main()
