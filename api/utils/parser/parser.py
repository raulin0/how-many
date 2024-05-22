import re

from api.utils.parser.card import Card
from api.utils.parser.decklist import Decklist
from api.utils.parser.section import Section


class DecklistParser:
    """
    Parser to transform a decklist text into a Decklist object.

    Attributes:
        _decklist_text (str): The raw decklist text.
    """

    def __init__(self, decklist_text: str):
        """
        Initializes a new instance of the DecklistParser class.

        Parameters:
            decklist_text (str): The raw decklist text.
        """
        self._decklist_text = decklist_text

    @property
    def decklist_text(self):
        """
        str: Returns the raw decklist text.
        """
        return self._decklist_text

    def _parse_deck(self):
        """
        Parses the decklist text and creates a Decklist object.

        Returns:
            Decklist: The Decklist object generated from the text.
        """
        sections_list = re.split(
            r'\r?\n\r?\n(?=\w)', self.decklist_text.strip()
        )
        decklist = Decklist(
            sections=[],
            is_commander_deck=False,
            has_companion=False,
            maindeck_card_count=0,
            non_land_card_count=0,
            non_land_cmcs_count=0.0,
            cheap_card_draw_spell_count=0,
            cheap_mana_ramp_spell_count=0,
            non_mythic_land_spell_mdfc_count=0,
            mythic_land_spell_mdfc_count=0,
            average_cmc=0.0,
            recommended_number_of_lands=0,
        )
        for section_text in sections_list:
            section = self._extract_section(section_text)
            decklist._sections.append(section)

        return decklist

    def _extract_section(self, section_text: str):
        """
        Extracts a section from the decklist text.

        Parameters:
            section_text (str): The raw section text.

        Returns:
            Section: The extracted section.

        Raises:
            ValueError: If the section name is unrecognized.
        """
        section_lines_list = re.split(r'\r?\n(?=\w)', section_text.strip())
        section = Section(name='', cards=[])
        section_name_lower = section_lines_list[0].strip().lower()
        if section_name_lower in [
            'commander',
            'companion',
            'deck',
            'sideboard',
        ]:
            section._name = section_name_lower
        else:
            raise ValueError(
                f'Unrecognized section name: {section_name_lower}. Each section must start with the name of the corresponding section (commander, companion, deck or sideboard).'
            )
        section_lines_list = section_lines_list[1:]
        for line in section_lines_list:
            line_lower = line.strip().lower()
            card = self._parse_card(line_lower)

            existing_card = next(
                (
                    existing_card
                    for existing_card in section._cards
                    if existing_card.name == card.name
                ),
                None,
            )
            if existing_card:
                existing_card._quantity += card.quantity
            else:
                section._cards.append(card)

        return section

    def _parse_card(self, line: str):
        """
        Parses a line of text and creates a Card object.

        Parameters:
            line (str): The line of text representing a card.

        Returns:
            Card: The Card object generated from the text.

        Raises:
            ValueError: If the card line format is invalid.
        """
        card_pattern = r'^(\d+)\s+(.*?)(?:\s+\(\w+\)\s+\d+)?$'
        card_pattern_match = re.match(card_pattern, line)

        if card_pattern_match:
            quantity = int(card_pattern_match.group(1))
            name = card_pattern_match.group(2)
            card = Card(
                name=name,
                quantity=quantity,
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

            return card

        else:
            raise ValueError(f'Invalid card format: {line}')
