import math

from lands.utils.card_data_fetcher import CardDataFetcher


class Analyzer:
    """
    A class for analyzing a parsed decklist and extracting various statistics.

    Attributes:
        _parsed_decklist (dict): A dictionary containing the parsed decklist data.
        _card_count (int): Total count of cards in the deck.
        _non_land_count (int): Count of non-land cards in the deck.
        _non_land_cmcs_count (int): Total converted mana cost of non-land cards.
        _cheap_card_draw_count (int): Count of cards that provide cheap card draw.
        _cheap_card_draw_list (list): List of cards that provide cheap card draw.
        _cheap_card_scry_count (int): Count of cards that provide cheap scrying.
        _cheap_card_scry_list (list): List of cards that provide cheap scrying.
        _cheap_mana_ramp_count (int): Count of cards that provide cheap mana ramp.
        _cheap_mana_ramp_list (list): List of cards that provide cheap mana ramp.
        _non_mythic_land_spell_mdfc_count (int): Count of non-mythic land/spell modal double-faced cards.
        _non_mythic_land_spell_mdfc_list (list): List of non-mythic land/spell modal double-faced cards.
        _mythic_land_spell_mdfc_count (int): Count of mythic land/spell modal double-faced cards.
        _mythic_land_spell_mdfc_list (list): List of mythic land/spell modal double-faced cards.
        _average_cmc (float): Average converted mana cost of non-land cards.
        _recommended_number_of_lands (float): Recommended number of lands based on analysis.

    Methods:
        analyze_decklist(): Analyzes the parsed decklist and populates statistics attributes.
    """

    def __init__(self, parsed_decklist):
        """
        Initializes the Analyzer instance.

        Args:
            parsed_decklist (dict): A dictionary containing the parsed decklist data.
        """
        self._parsed_decklist = parsed_decklist
        self._card_count = 0
        self._non_land_count = 0
        self._non_land_cmcs_count = 0
        self._cheap_card_draw_count = 0
        self._cheap_card_draw_list = []
        self._cheap_card_scry_count = 0
        self._cheap_card_scry_list = []
        self._cheap_mana_ramp_count = 0
        self._cheap_mana_ramp_list = []
        self._non_mythic_land_spell_mdfc_count = 0
        self._non_mythic_land_spell_mdfc_list = []
        self._mythic_land_spell_mdfc_count = 0
        self._mythic_land_spell_mdfc_list = []
        self._average_cmc = 0.0
        self._recommended_number_of_lands = 0.0

    @property
    def card_count(self):
        """
        int: The total count of cards in the deck.
        """
        return self._card_count

    @property
    def non_land_count(self):
        """
        int: The count of non-land cards in the deck.
        """
        return self._non_land_count

    @property
    def non_land_cmcs_count(self):
        """
        int: The total converted mana cost of non-land cards in the deck.
        """
        return self._non_land_cmcs_count

    @property
    def cheap_card_draw_count(self):
        """
        int: The count of cards that provide cheap card draw.
        """
        return self._cheap_card_draw_count

    @property
    def cheap_card_draw_list(self):
        """
        list: A list of cards that provide cheap card draw.
        """
        return self._cheap_card_draw_list

    @property
    def cheap_card_scry_count(self):
        """
        int: The count of cards that provide cheap scrying.
        """
        return self._cheap_card_scry_count

    @property
    def cheap_card_scry_list(self):
        """
        list: A list of cards that provide cheap scrying.
        """
        return self._cheap_card_scry_list

    @property
    def cheap_mana_ramp_count(self):
        """
        int: The count of cards that provide cheap mana ramp.
        """
        return self._cheap_mana_ramp_count

    @property
    def cheap_mana_ramp_list(self):
        """
        list: A list of cards that provide cheap mana ramp.
        """
        return self._cheap_mana_ramp_list

    @property
    def non_mythic_land_spell_mdfc_count(self):
        """
        int: The count of non-mythic land/spell modal double-faced cards in the deck.
        """
        return self._non_mythic_land_spell_mdfc_count

    @property
    def non_mythic_land_spell_mdfc_list(self):
        """
        list: A list of non-mythic land/spell modal double-faced cards in the deck.
        """
        return self._non_mythic_land_spell_mdfc_list

    @property
    def mythic_land_spell_mdfc_count(self):
        """
        int: The count of mythic land/spell modal double-faced cards in the deck.
        """
        return self._mythic_land_spell_mdfc_count

    @property
    def mythic_land_spell_mdfc_list(self):
        """
        list: A list of mythic land/spell modal double-faced cards in the deck.
        """
        return self._mythic_land_spell_mdfc_list

    @property
    def average_cmc(self):
        """
        float: The average converted mana cost of non-land cards in the deck.
        """
        return self._average_cmc

    @property
    def recommended_number_of_lands(self):
        """
        float: The recommended number of lands based on the analysis.
        """
        return self._recommended_number_of_lands

    def analyze_decklist(self):
        """
        Analyzes the parsed decklist and populates various statistics attributes.
        """
        fetcher = CardDataFetcher()

        # Count the number of cards in the companion and maindeck
        companion = len(self._parsed_decklist['companion'])
        maindeck = self._parsed_decklist['deck']

        # Iterate through maindeck cards and analyze each card
        for card, card_info_list in maindeck.items():
            total_quantity = sum(
                card_info['quantity'] for card_info in card_info_list
            )
            self._card_count += total_quantity
            card_quantity = total_quantity
            try:
                card_data = fetcher.get_card_data(card)
                self._analyze_card(card, card_data, card_quantity)
            except AttributeError:
                raise AttributeError(f'Card data not found for {card}.')

        # Calculate average converted mana cost and recommended number of lands
        if self.non_land_cmcs_count > 0 and self.non_land_count > 0:
            self._average_cmc = self.non_land_cmcs_count / self.non_land_count
        else:
            raise ValueError(
                'Invalid decklist. Non-land cards count or non-land cmcs count must be greater than 0.'
            )
        self._calculate_number_of_lands(companion)

    def _analyze_card(self, card, card_data, card_quantity):
        """
        Analyzes a single card in the decklist and updates relevant statistics.

        Args:
            card (str): The name of the card being analyzed.
            card_data (dict): Card data fetched using CardDataFetcher.
            card_quantity (int): The quantity of the card in the deck.
        """
        type_line = card_data.get('type_line', '').lower()
        layout = card_data.get('layout', '').lower()

        # Determine if the card is a non-land card, possibly with a land/spell modal double-faced layout
        if 'land' not in type_line or (
            'modal_dfc' in layout
            and not (
                'land'
                in card_data.get('card_faces', [{}])[0]
                .get('type_line', '')
                .lower()
            )
        ):
            self._non_land_count += card_quantity
            cmc = card_data.get('cmc', 0)
            self._non_land_cmcs_count += card_quantity * cmc

            # Check if the card provides land/spell modal double-faced card
            if self._is_land_spell_mdfc(layout, card_data):
                # Determine if the land/spell modal double-faced card is mythic or non-mythic
                rarity = card_data.get('rarity', '').lower()
                if 'mythic' in rarity:
                    self._mythic_land_spell_mdfc_list.append(card)
                    self._mythic_land_spell_mdfc_count += card_quantity
                else:
                    self._non_mythic_land_spell_mdfc_list.append(card)
                    self._non_mythic_land_spell_mdfc_count += card_quantity

            # Check if the card provides cheap card draw
            oracle_text = card_data.get('oracle_text', '').lower()
            if self._is_cheap_card_draw(oracle_text, cmc, type_line):
                self._cheap_card_draw_list.append(card)
                self._cheap_card_draw_count += card_quantity

            # Check if the card provides cheap mana ramp
            if self._is_cheap_mana_ramp(oracle_text, cmc, type_line, card):
                self._cheap_mana_ramp_list.append(card)
                self._cheap_mana_ramp_count += card_quantity

            # Check if the card provides cheap scrying
            if self._is_cheap_card_scry(oracle_text, cmc, type_line, card):
                self._cheap_card_scry_list.append(card)
                self._cheap_card_scry_count += card_quantity

    def _is_land_spell_mdfc(self, layout, card_data):
        """
        Checks if a card provides land/spell modal double-faced card based on its attributes.

        Args:
            layout (str): The layout of the card.
            cmc (float): The converted mana cost of the card.
            type_line (str): The type line of the card.

        Returns:
            bool: True if the card provides land/spell modal double-faced card, False otherwise.
        """
        if (
            'modal_dfc' in layout
            and 'land'
            in card_data.get('card_faces', [{}])[1]
            .get('type_line', '')
            .lower()
        ):
            return True

        return False

    def _is_cheap_card_draw(self, oracle_text, cmc, type_line):
        """
        Checks if a card provides cheap card draw based on its attributes.

        Args:
            oracle_text (str): The oracle text of the card.
            cmc (float): The converted mana cost of the card.
            type_line (str): The type line of the card.

        Returns:
            bool: True if the card provides cheap card draw, False otherwise.
        """
        # Check for simple card draw effects
        if oracle_text:
            if cmc <= 2.0:
                if 'draw' in oracle_text:
                    if not (
                        '{4}' in oracle_text
                        or 'blood token' in oracle_text
                        or 'investigate' in oracle_text
                    ):
                        if 'creature' in type_line:
                            if (
                                'when' in oracle_text
                                and 'enters' in oracle_text
                            ):
                                return True
                        else:
                            return True

                # Check for "look at the top of your library" effects
                elif not ('creature' in type_line):
                    if (
                        'look' in oracle_text
                        and 'library' in oracle_text
                        and 'put' in oracle_text
                        and 'your hand' in oracle_text
                    ):
                        if not ('pay' in oracle_text):
                            return True

            # Check for cycling abilities
            if (
                r'cycling {1}' in oracle_text
                or r'cycling {w}' in oracle_text
                or r'cycling {b}' in oracle_text
                or r'cycling {u}' in oracle_text
                or r'cycling {r}' in oracle_text
                or r'cycling {g}' in oracle_text
            ):
                return True

        return False

    def _is_cheap_mana_ramp(self, oracle_text, cmc, type_line, card):
        """
        Checks if a card provides cheap mana ramp based on its attributes.

        Args:
            oracle_text (str): The oracle text of the card.
            cmc (float): The converted mana cost of the card.
            type_line (str): The type line of the card.
            card (str): The name of the card being analyzed.

        Returns:
            bool: True if the card provides cheap mana ramp, False otherwise.
        """
        # Check for mana ramp effects
        if oracle_text:
            if cmc <= 2.0:
                if not (card in self.cheap_card_draw_list):
                    if 'add ' in oracle_text:
                        if not ('add its ability' in oracle_text) or not (
                            'add a lore counter' in oracle_text
                        ):
                            if 'creature' in type_line:
                                if not ('dies' in oracle_text):
                                    return True
                            else:
                                return True

                    # Check for land search effects
                    elif (
                        'search' in oracle_text
                        and 'your library' in oracle_text
                        and 'land' in oracle_text
                    ):
                        if not ('sacrifice' in oracle_text):
                            return True

                    # Check for mana enhancement through tapping enchanted land
                    elif (
                        'enchanted land is tapped' in oracle_text
                        and 'adds and additional' in oracle_text
                    ):
                        return True

                    # Check for putting creatures into play from hand
                    elif (
                        'put' in oracle_text
                        and 'creature card with' in oracle_text
                        and 'from your hand onto the battlefield'
                        in oracle_text
                    ):
                        return True

        return False

    def _is_cheap_card_scry(self, oracle_text, cmc, type_line, card):
        """
        Checks if a card provides cheap scrying based on its attributes.

        Args:
            oracle_text (str): The oracle text of the card.
            cmc (float): The converted mana cost of the card.
            type_line (str): The type line of the card.
            card (str): The name of the card being analyzed.

        Returns:
            bool: True if the card provides cheap scrying, False otherwise.
        """
        # Check for scry effects
        if oracle_text:
            if cmc <= 2.0:
                if not (card in self.cheap_card_draw_list):
                    if 'scry ' in oracle_text:
                        if 'creature' in type_line:
                            if (
                                'when' in oracle_text
                                and 'enters' in oracle_text
                            ):
                                return True
                        else:
                            return True

        return False

    def _calculate_number_of_lands(self, companion):
        """
        Calculates the recommended number of lands based on deck size and companion.

        Args:
            companion (int): The number of companion cards in the deck.

        Raises:
            ValueError: If the deck size is not 60, 80, or 99 cards.
        """
        if self._card_count == 60:
            self._lands_60_cards(companion)
        elif self._card_count == 80:
            self._lands_80_cards()
        elif self._card_count == 99:
            self._lands_99_cards()
        else:
            raise ValueError(
                'Invalid decklist. Deck size must be 60, 80, or 99 cards.'
            )

    def _lands_60_cards(self, companion):
        """
        Calculates the recommended number of lands for a 60-card deck.

        Args:
            companion (int): The number of companion cards in the deck.
        """
        self._recommended_number_of_lands = (
            19.59
            + (1.90 * self.average_cmc)
            - (
                0.28
                * (self.cheap_card_draw_count + self.cheap_mana_ramp_count)
            )
            + (0.27 * companion)
        )
        self._recommended_number_of_lands = (
            self._recommended_number_of_lands
            - (
                (0.38 * self.non_mythic_land_spell_mdfc_count)
                + (0.74 * self.mythic_land_spell_mdfc_count)
            )
        )

        if self.cheap_card_scry_count >= 4:
            self._recommended_number_of_lands = math.floor(
                self._recommended_number_of_lands
            )
        else:
            self._recommended_number_of_lands = round(
                self._recommended_number_of_lands
            )

    def _lands_80_cards(self):
        """
        Calculates the recommended number of lands for an 80-card deck.
        """
        self._recommended_number_of_lands = (
            80 / 60 * (19.59 + (1.90 * self.average_cmc) + 0.27)
        ) - (0.28 * (self.cheap_card_draw_count + self.cheap_mana_ramp_count))
        self._recommended_number_of_lands -= (
            0.38 * self.non_mythic_land_spell_mdfc_count
        ) + (0.74 * self.mythic_land_spell_mdfc_count)

        self._recommended_number_of_lands = round(
            self._recommended_number_of_lands
        )

    def _lands_99_cards(self):
        """
        Calculates the recommended number of lands for a 99-card deck.
        """
        self._recommended_number_of_lands = (
            (99 / 60 * (19.59 + (1.90 * self.average_cmc) + 0.27))
            - (
                0.28
                * (self.cheap_card_draw_count + self.cheap_mana_ramp_count)
            )
            - 1.35
        )
        self._recommended_number_of_lands -= (
            0.38 * self.non_mythic_land_spell_mdfc_count
        ) + (0.74 * self.mythic_land_spell_mdfc_count)
        self._recommended_number_of_lands = round(
            self._recommended_number_of_lands
        )
