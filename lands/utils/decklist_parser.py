import re


class DecklistParser:
    """
    A class for parsing a decklist and extracting card information.

    Attributes:
        _decklist (str): The raw decklist to be parsed.
        _parsed_decklist (dict): A dictionary to store the parsed decklist data.
    """

    def __init__(self, decklist):
        """
        Initializes the DecklistParser instance.

        Args:
            decklist (str): The raw decklist to be parsed.
        """
        self._decklist = decklist.lower().strip()
        self._parsed_decklist = {'companion': {}, 'deck': {}, 'sideboard': {}}

    @property
    def parsed_decklist(self):
        """
        Property method to access the parsed decklist.

        Returns:
            dict: A dictionary containing the parsed decklist data.
        """
        return self._parsed_decklist

    def parse_decklist(self):
        """
        Parses the decklist and extracts card information.

        Returns:
            dict: A dictionary containing the parsed decklist data.
        """
        lines = self._decklist.split('\r\n')

        if self._is_valid_decklist(lines):
            card_pattern = (
                r'^\s*(?P<quantity>\d+)\s+(?P<card_name>[\w\s\'\,\-]+)'
            )
            set_pattern = r'\((?P<set_code>\w+)\)\s+(?P<card_set_id>\d+)'

            current_section = None

            for line in lines:
                if line.startswith('companion'):
                    current_section = line.strip()
                elif line.startswith('deck'):
                    current_section = line.strip()
                elif line.startswith('sideboard'):
                    current_section = line.strip()
                else:
                    match = re.search(card_pattern, line)
                    if match:
                        quantity = int(match.group('quantity'))
                        card_name = match.group('card_name').strip()
                        set_info = re.search(set_pattern, line)

                        if set_info:
                            set_code = set_info.group('set_code')
                            card_set_id = set_info.group('card_set_id')
                        else:
                            set_code = None
                            card_set_id = None

                        self._parsed_decklist[current_section].setdefault(
                            card_name, []
                        )
                        self._parsed_decklist[current_section][
                            card_name
                        ].append(
                            {
                                'quantity': quantity,
                                'set_code': set_code,
                                'card_set_id': card_set_id,
                            }
                        )

            return self._parsed_decklist

        else:
            raise KeyError(
                'Invalid entry. Enter a valid decklist by explicitly entering each section that your decklist has. Example: Companion ... Deck ... Sideboard ...'
            )

    def _is_valid_decklist(self, decklist):
        if self._is_valid_decklist_start(decklist):
            if self._is_valid_decklist_end(decklist):
                return True
        return False

    def _is_valid_decklist_start(self, decklist):
        if 'companion' in decklist[0]:
            if 'deck' in decklist[3]:
                return True

        elif 'deck' in decklist[0]:
            return True

    def _is_valid_decklist_end(self, decklist):
        deck_index = decklist.index('deck')
        sublist_after_deck = decklist[deck_index + 1 :]
        sublist_after_deck_len = len(sublist_after_deck)
        if '' in sublist_after_deck:
            if 'sideboard' in sublist_after_deck:
                if (
                    sublist_after_deck.index('')
                    == sublist_after_deck.index('sideboard') - 1
                ):
                    return True

            elif sublist_after_deck.index('') + 1 == sublist_after_deck_len:
                return True

        elif 'sideboard' not in sublist_after_deck:
            return True
