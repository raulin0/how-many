import re

import requests

from api.models import CardModel
from api.utils.parser.card import Card
from api.utils.parser.decklist import Decklist


class DecklistDataManager:
    def __init__(self, decklist: Decklist):
        self._decklist = decklist

    @property
    def decklist(self):
        return self._decklist

    def process_decklist(self):
        for decklist_section in self.decklist.sections:
            for section_card in decklist_section.cards:
                self._get_or_fetch_card_data(section_card)
                if decklist_section.name == 'deck':
                    self._get_maindeck_cards_count(section_card)
                    self._get_non_land_card_and_non_land_cmcs_count(
                        section_card
                    )
                    self._get_cheap_card_draw_spell_count(section_card)
                    self._get_cheap_mana_ramp_spell_count(section_card)
                    self._get_non_mythic_and_mythic_land_spell_mdfc_count(
                        section_card
                    )

            self._get_is_commander_deck(decklist_section.name)
            self._get_has_companion(decklist_section.name)

        self._get_average_cmc()
        self._get_recommended_number_of_lands()

    def _get_or_fetch_card_data(self, section_card: Card):
        card = CardModel.objects.filter(name=section_card.name).first()
        if card:
            self._get_database_card_data(section_card, card)

        else:
            self._get_scryfall_card_data(section_card)

    def _get_database_card_data(self, section_card: Card, card: CardModel):
        section_card._mana_cost = card.mana_cost
        section_card._cmc = card.cmc
        section_card._type_line = card.type_line
        section_card._rarity = card.rarity
        section_card._oracle_text = card.oracle_text
        section_card._is_land = card.is_land
        section_card._is_cheap_card_draw_spell = card.is_cheap_card_draw_spell
        section_card._is_cheap_mana_ramp_spell = card.is_cheap_mana_ramp_spell
        section_card._is_land_spell_mdfc = card.is_land_spell_mdfc

    def _get_scryfall_card_data(self, section_card: Card):
        fetched_card_data = self._fetch_card_data(section_card.name)
        if fetched_card_data:
            section_card._mana_cost = fetched_card_data.get(
                'mana_cost', ''
            ).lower()
            section_card._cmc = fetched_card_data.get('cmc', 0.0)
            section_card._type_line = fetched_card_data.get(
                'type_line', ''
            ).lower()
            section_card._rarity = fetched_card_data.get('rarity', '').lower()
            section_card._oracle_text = fetched_card_data.get(
                'oracle_text', ''
            ).lower()
            section_card._is_land = self._is_land(
                section_card, fetched_card_data
            )
            section_card._is_cheap_card_draw_spell = (
                self._is_cheap_card_draw_spell(section_card)
            )
            section_card._is_cheap_mana_ramp_spell = (
                self._is_cheap_mana_ramp_spell(section_card)
            )
            section_card._is_land_spell_mdfc = self._is_land_spell_mdfc(
                section_card, fetched_card_data
            )

    def _fetch_card_data(self, section_card_name: str):
        scryfall_api_url = (
            f'https://api.scryfall.com/cards/named?exact={section_card_name}'
        )
        response = requests.get(scryfall_api_url)
        response.raise_for_status()

        return response.json()

    def _is_land(self, section_card: Card, card_data: dict):
        if self._has_land_in_front_or_back_type_line(section_card, card_data):

            return True

        return False

    def _has_land_in_front_or_back_type_line(
        self, section_card: Card, card_data: dict
    ):
        type_line = section_card.type_line
        card_layout = card_data.get('layout', '').lower()

        if 'land' in type_line or (
            'modal_dfc' in card_layout
            and 'land'
            in card_data.get('card_faces', [{}])[0]
            .get('type_line', '')
            .lower()
        ):
            return True

    def _is_cheap_card_draw_spell(self, section_card: Card):
        cmc = section_card.cmc
        type_line = section_card.type_line
        oracle_text = section_card.oracle_text
        is_land = section_card.is_land

        if is_land:

            return False

        if not oracle_text:

            return False

        cycling_cost_match = re.search(r'cycling \{[1wburg]\}', oracle_text)
        if cycling_cost_match:

            return True

        if cmc <= 2.0:
            if 'draw' in oracle_text:
                draw_cost_match = re.search(r'\{\d+\}', oracle_text)
                if draw_cost_match:

                    return False

                attack_block_draw_condition_match = re.search(
                    r'\battack|attacks|block|blocks\b', oracle_text
                )
                if attack_block_draw_condition_match:

                    return False

                if 'creature' in type_line:
                    etb_draw_condition_match = re.search(
                        r'\bwhen.*enter|enters\b', oracle_text
                    )
                    if etb_draw_condition_match:

                        return True

                return True

            draw_equivalent_terms_match = re.search(
                r'\blook.*library.*put.*your hand\b', oracle_text
            )
            if draw_equivalent_terms_match:
                draw_equivalent_cost_match = re.search(r'\{\d+\}', oracle_text)
                if draw_equivalent_cost_match:

                    return False

                return True

        return False

    def _is_cheap_mana_ramp_spell(self, section_card: Card):
        cmc = section_card.cmc
        type_line = section_card.type_line
        oracle_text = section_card.oracle_text
        is_land = section_card.is_land
        is_cheap_card_draw_spell = section_card.is_cheap_card_draw_spell

        if is_land:

            return False

        if not oracle_text:

            return False

        if is_cheap_card_draw_spell:

            return False

        if cmc <= 2.0:
            if 'add ' in oracle_text:
                not_add_mana_term_match = re.search(
                    r'\badd its ability|add a lore counter\b', oracle_text
                )
                if not_add_mana_term_match:

                    return False

                if 'creature' in type_line:
                    if 'die' in oracle_text:

                        return False

                    return True

                return True

            untap_land_term_match = re.search(
                r'\buntap target.*land|snow land|forest|swamp|mountain|island|plains\b',
                oracle_text,
            )
            if untap_land_term_match:

                return True

            mana_ramp_equivalent_terms_match = re.search(
                r'\bsearch.*your library.*land\b', oracle_text
            )
            if mana_ramp_equivalent_terms_match:
                if 'sacrifice' in oracle_text:

                    return False

                return True

            enchanted_land_ramp_term_match = re.search(
                r'\benchanted.*land|snow land|forest|swamp|mountain|island|plains\b',
                oracle_text,
            )
            if enchanted_land_ramp_term_match:
                if 'adds an additional' in oracle_text:

                    return True

            put_onto_battlefield_terms_match = re.search(
                r'\bput.*creature card with.*from your hand onto the battlefield\b',
                oracle_text,
            )
            if put_onto_battlefield_terms_match:

                return True

        return False

    def _is_land_spell_mdfc(self, section_card: Card, card_data: dict):
        is_land = section_card.is_land
        card_layout = card_data.get('layout', '').lower()

        if is_land:

            return False

        if 'modal_dfc' in card_layout and (
            'land'
            in card_data.get('card_faces', [{}])[1]
            .get('type_line', '')
            .lower()
        ):

            return True

        return False

    def _get_maindeck_cards_count(self, maindeck_card: Card):
        self._decklist._maindeck_card_count += maindeck_card.quantity

    def _get_non_land_card_and_non_land_cmcs_count(self, maindeck_card: Card):
        if not maindeck_card.is_land:
            self._decklist._non_land_card_count += maindeck_card.quantity
            self._decklist._non_land_cmcs_count += (
                maindeck_card.quantity * maindeck_card.cmc
            )

    def _get_cheap_card_draw_spell_count(self, maindeck_card: Card):
        if maindeck_card.is_cheap_card_draw_spell:
            self._decklist._cheap_card_draw_spell_count += (
                maindeck_card.quantity
            )

    def _get_cheap_mana_ramp_spell_count(self, maindeck_card: Card):
        if maindeck_card.is_cheap_mana_ramp_spell:
            self._decklist._cheap_mana_ramp_spell_count += (
                maindeck_card.quantity
            )

    def _get_non_mythic_and_mythic_land_spell_mdfc_count(
        self, maindeck_card: Card
    ):
        if maindeck_card.is_land_spell_mdfc:
            if maindeck_card.rarity in ['common', 'uncommon', 'rare']:
                self._decklist._non_mythic_land_spell_mdfc_count += (
                    maindeck_card.quantity
                )
            elif maindeck_card.rarity == 'mythic':
                self._decklist._mythic_land_spell_mdfc_count += (
                    maindeck_card.quantity
                )

    def _get_is_commander_deck(self, decklist_section_name: str):
        if decklist_section_name == 'commander':
            self._decklist._is_commander_deck = True

    def _get_has_companion(self, decklist_section_name: str):
        if decklist_section_name == 'companion':
            self._decklist._has_companion = True

    def _get_average_cmc(self):
        if self.decklist.non_land_card_count != 0:
            self._decklist._average_cmc = (
                self.decklist.non_land_cmcs_count
                / self.decklist.non_land_card_count
            )

    def _get_recommended_number_of_lands(self):
        commander_free_mulligan_draw_reduction = 0.0
        if self.decklist.is_commander_deck:
            commander_free_mulligan_draw_reduction = 1.35
        if self.decklist.maindeck_card_count >= 80:
            self._decklist._has_companion = True

        recommended_number_of_lands = (
            self.decklist.maindeck_card_count
            / 60
            * (
                19.59
                + (
                    (1.90 * self.decklist.average_cmc)
                    + (0.27 * self.decklist.has_companion)
                )
            )
        ) - (
            0.28
            * (
                self.decklist.cheap_card_draw_spell_count
                + self.decklist.cheap_mana_ramp_spell_count
            )
            - commander_free_mulligan_draw_reduction
        )
        recommended_number_of_lands = recommended_number_of_lands - (
            (0.38 * self.decklist.non_mythic_land_spell_mdfc_count)
            + (0.74 * self.decklist.mythic_land_spell_mdfc_count)
        )

        self._decklist._recommended_number_of_lands = round(
            recommended_number_of_lands
        )
