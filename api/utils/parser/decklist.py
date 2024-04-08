from api.utils.parser.section import Section


class Decklist:
    def __init__(
        self,
        sections: list[Section],
        is_commander_deck: bool,
        has_companion: bool,
        maindeck_card_count: int,
        non_land_card_count: int,
        non_land_cmcs_count: float,
        cheap_card_draw_spell_count: int,
        cheap_mana_ramp_spell_count: int,
        non_mythic_land_spell_mdfc_count: int,
        mythic_land_spell_mdfc_count: int,
        average_cmc: float,
        recommended_number_of_lands: int,
    ):
        self._sections = sections
        self._is_commander_deck = is_commander_deck
        self._has_companion = has_companion
        self._maindeck_card_count = maindeck_card_count
        self._non_land_card_count = non_land_card_count
        self._non_land_cmcs_count = non_land_cmcs_count
        self._cheap_card_draw_spell_count = cheap_card_draw_spell_count
        self._cheap_mana_ramp_spell_count = cheap_mana_ramp_spell_count
        self._non_mythic_land_spell_mdfc_count = (
            non_mythic_land_spell_mdfc_count
        )
        self._mythic_land_spell_mdfc_count = mythic_land_spell_mdfc_count
        self._average_cmc = average_cmc
        self._recommended_number_of_lands = recommended_number_of_lands

    @property
    def sections(self):
        return self._sections

    @property
    def is_commander_deck(self):
        return self._is_commander_deck

    @property
    def has_companion(self):
        return self._has_companion

    @property
    def maindeck_card_count(self):
        return self._maindeck_card_count

    @property
    def non_land_card_count(self):
        return self._non_land_card_count

    @property
    def non_land_cmcs_count(self):
        return self._non_land_cmcs_count

    @property
    def cheap_card_draw_spell_count(self):
        return self._cheap_card_draw_spell_count

    @property
    def cheap_mana_ramp_spell_count(self):
        return self._cheap_mana_ramp_spell_count

    @property
    def non_mythic_land_spell_mdfc_count(self):
        return self._non_mythic_land_spell_mdfc_count

    @property
    def mythic_land_spell_mdfc_count(self):
        return self._mythic_land_spell_mdfc_count

    @property
    def average_cmc(self):
        return self._average_cmc

    @property
    def recommended_number_of_lands(self):
        return self._recommended_number_of_lands
