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
        lines = self._decklist.split('\n')

        card_pattern = r'^\s*(?P<quantity>\d+)\s+(?P<card_name>[\w\s\'\,\-]+)'
        set_pattern = r'\((?P<set_code>\w+)\)\s+(?P<set_number>\d+)'

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
                        set_number = set_info.group('set_number')
                    else:
                        set_code = None
                        set_number = None
                    
                    self._parsed_decklist[current_section].setdefault(card_name, [])
                    self._parsed_decklist[current_section][card_name].append({
                        'quantity': quantity,
                        'set_code': set_code,
                        'set_number': set_number,
                    })

        return self._parsed_decklist
