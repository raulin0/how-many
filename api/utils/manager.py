import re

import requests

from api.models import CardModel
from api.utils.parser.card import Card
from api.utils.parser.decklist import Decklist
from how_many.settings import SCRYFALL_API_URL


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
                decklist_section_name_lower = decklist_section.name.lower()
                if decklist_section_name_lower == 'deck':
                    self._get_maindeck_cards_count(section_card)
                    self._get_non_land_card_and_non_land_cmcs_count(
                        section_card
                    )
                    self._get_cheap_card_draw_spell_count(section_card)
                    self._get_cheap_mana_ramp_spell_count(section_card)
                    self._get_non_mythic_and_mythic_land_spell_mdfc_count(
                        section_card
                    )

            self._get_is_commander_deck(decklist_section_name_lower)
            self._get_has_companion(decklist_section_name_lower)

        self._get_average_cmc()
        self._get_recommended_number_of_lands()

    def _get_or_fetch_card_data(self, section_card: Card):
        card = CardModel.objects.filter(name=section_card.name).first()
        if card:
            self._get_database_card_data(section_card, card)

        else:
            self._get_scryfall_card_data(section_card)

    def _get_database_card_data(self, section_card: Card, card: CardModel):
        section_card._name = card.name
        section_card._layout = card.layout
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
            section_card._name = self._get_name(fetched_card_data)
            section_card._layout = self._get_layout(fetched_card_data)
            section_card._mana_cost = self._get_mana_cost(
                section_card.layout, fetched_card_data
            )
            section_card._cmc = self._get_cmc(fetched_card_data)
            section_card._type_line = self._get_type_line(fetched_card_data)
            section_card._rarity = self._get_rarity(fetched_card_data)
            section_card._oracle_text = self._get_oracle_text(
                section_card.layout, fetched_card_data
            )
            section_card_type_line_lower = section_card.type_line.lower()
            section_card_layout_lower = section_card.layout.lower()
            section_card._is_land = self._is_land(
                section_card_type_line_lower,
                section_card_layout_lower,
                fetched_card_data,
            )
            section_card_oracle_text_lower = section_card.oracle_text.lower()
            section_card._is_cheap_card_draw_spell = (
                self._is_cheap_card_draw_spell(
                    section_card.cmc,
                    section_card_oracle_text_lower,
                    section_card_type_line_lower,
                    section_card.is_land,
                )
            )
            section_card._is_cheap_mana_ramp_spell = (
                self._is_cheap_mana_ramp_spell(
                    section_card.cmc,
                    section_card_type_line_lower,
                    section_card_oracle_text_lower,
                    section_card.is_land,
                    section_card.is_cheap_card_draw_spell,
                )
            )
            section_card._is_land_spell_mdfc = self._is_land_spell_mdfc(
                section_card.is_land,
                section_card_layout_lower,
                fetched_card_data,
            )

    def _fetch_card_data(self, section_card_name: str):
        scryfall_api_request_url = f'{SCRYFALL_API_URL}{section_card_name}'
        
        try:
            response = requests.get(scryfall_api_request_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def _get_name(self, fetched_card_data: dict):
        return fetched_card_data.get('name', '')

    def _get_layout(self, fetched_card_data: dict):
        return fetched_card_data.get('layout', '')

    def _get_mana_cost(
        self, section_card_layout: str, fetched_card_data: dict
    ):
        if 'normal' not in section_card_layout:
            front_mana_cost = fetched_card_data.get('card_faces', [{}])[0].get(
                'mana_cost', ''
            )
            back_mana_cost = fetched_card_data.get('card_faces', [{}])[1].get(
                'mana_cost', ''
            )
            card_mana_Cost = f'{front_mana_cost} // {back_mana_cost}'

            return (
                card_mana_Cost
                if front_mana_cost and back_mana_cost
                else front_mana_cost or back_mana_cost
            )

        return fetched_card_data.get('mana_cost', '')

    def _get_cmc(self, fetched_card_data: dict):
        return fetched_card_data.get('cmc', 0.0)

    def _get_type_line(self, fetched_card_data: dict):
        return fetched_card_data.get('type_line', '')

    def _get_rarity(self, fetched_card_data: dict):
        return fetched_card_data.get('rarity', '')

    def _get_oracle_text(
        self, section_card_layout: str, fetched_card_data: dict
    ):
        if 'normal' not in section_card_layout:
            front_oracle_text = fetched_card_data.get('card_faces', [{}])[
                0
            ].get('oracle_text', '')
            back_oracle_text = fetched_card_data.get('card_faces', [{}])[
                1
            ].get('oracle_text', '')
            card_oracle_text = f'{front_oracle_text} // {back_oracle_text}'

            return (
                card_oracle_text
                if front_oracle_text and back_oracle_text
                else front_oracle_text or back_oracle_text
            )

        return fetched_card_data.get('oracle_text', '')

    def _is_land(
        self,
        section_card_type_line_lower: str,
        section_card_layout_lower: str,
        fetched_card_data: dict,
    ):
        if 'modal_dfc' in section_card_layout_lower:
            section_card_front_type_line = fetched_card_data.get(
                'card_faces', [{}]
            )[0].get('type_line', '')

            section_card_front_type_line_lower = (
                section_card_front_type_line.lower()
            )
            if 'land' in section_card_front_type_line_lower:

                return True

        elif 'land' in section_card_type_line_lower:

            return True

        return False

    def _is_cheap_card_draw_spell(
        self,
        section_card_cmc: float,
        section_card_oracle_text_lower: str,
        section_card_type_line_lower: str,
        section_card_is_land: bool,
    ):
        if section_card_is_land:

            return False

        if not section_card_oracle_text_lower:

            return False

        cycling_cost_match = re.search(
            r'cycling \{[1wburg]\}', section_card_oracle_text_lower
        )
        if cycling_cost_match:

            return True

        if section_card_cmc <= 2.0:
            if 'draw' in section_card_oracle_text_lower:
                draw_cost_match = re.search(
                    r'\{\d+\}', section_card_oracle_text_lower
                )
                if draw_cost_match:

                    return False

                attack_block_draw_condition_match = re.search(
                    r'\battack|attacks|block|blocks\b',
                    section_card_oracle_text_lower,
                )
                if attack_block_draw_condition_match:

                    return False

                if 'creature' in section_card_type_line_lower:
                    etb_draw_condition_match = re.search(
                        r'\bwhen.*enter|enters\b',
                        section_card_oracle_text_lower,
                    )
                    if etb_draw_condition_match:

                        return True

                return True

            draw_equivalent_terms_match = re.search(
                r'\blook.*library.*put.*your hand\b',
                section_card_oracle_text_lower,
            )
            if draw_equivalent_terms_match:
                draw_equivalent_cost_match = re.search(
                    r'\{\d+\}', section_card_oracle_text_lower
                )
                if draw_equivalent_cost_match:

                    return False

                return True

        return False

    def _is_cheap_mana_ramp_spell(
        self,
        section_card_cmc: float,
        section_card_type_line_lower: str,
        section_card_oracle_text_lower: str,
        section_card_is_land: bool,
        section_card_is_cheap_card_draw_spell: bool,
    ):
        if section_card_is_land:

            return False

        if not section_card_oracle_text_lower:

            return False

        if section_card_is_cheap_card_draw_spell:

            return False

        if section_card_cmc <= 2.0:
            if 'add ' in section_card_oracle_text_lower:
                not_add_mana_term_match = re.search(
                    r'\badd its ability|add a lore counter\b',
                    section_card_oracle_text_lower,
                )
                if not_add_mana_term_match:

                    return False

                if 'creature' in section_card_type_line_lower:
                    if 'die' in section_card_oracle_text_lower:

                        return False

                    return True

                return True

            untap_land_term_match = re.search(
                r'\buntap target.*land|snow land|forest|swamp|mountain|island|plains\b',
                section_card_oracle_text_lower,
            )
            if untap_land_term_match:

                return True

            mana_ramp_equivalent_terms_match = re.search(
                r'\bsearch.*your library.*land\b',
                section_card_oracle_text_lower,
            )
            if mana_ramp_equivalent_terms_match:
                if 'sacrifice' in section_card_oracle_text_lower:

                    return False

                return True

            enchanted_land_ramp_term_match = re.search(
                r'\benchanted.*land|snow land|forest|swamp|mountain|island|plains\b',
                section_card_oracle_text_lower,
            )
            if enchanted_land_ramp_term_match:
                if 'adds an additional' in section_card_oracle_text_lower:

                    return True

            put_onto_battlefield_terms_match = re.search(
                r'\bput.*creature card with.*from your hand onto the battlefield\b',
                section_card_oracle_text_lower,
            )
            if put_onto_battlefield_terms_match:

                return True

        return False

    def _is_land_spell_mdfc(
        self,
        section_card_is_land: bool,
        section_card_layout_lower: str,
        fetched_card_data: dict,
    ):
        if section_card_is_land:

            return False

        if 'modal_dfc' in section_card_layout_lower:
            section_card_back_type_line = fetched_card_data.get(
                'card_faces', [{}]
            )[1].get('type_line', '')
            section_card_back_type_line_lower = (
                section_card_back_type_line.lower()
            )
            if 'land' in section_card_back_type_line_lower:

                return True

        return False

    def _get_maindeck_cards_count(self, section_card: Card):
        section_card_quantity = section_card.quantity
        self._decklist._maindeck_card_count += section_card_quantity

    def _get_non_land_card_and_non_land_cmcs_count(self, section_card: Card):
        section_card_is_land = section_card.is_land
        section_card_quantity = section_card.quantity
        section_card_cmc = section_card.cmc
        if not section_card_is_land:
            self._decklist._non_land_card_count += section_card_quantity
            self._decklist._non_land_cmcs_count += (
                section_card_quantity * section_card_cmc
            )

    def _get_cheap_card_draw_spell_count(self, section_card: Card):
        section_card_is_cheap_card_draw_spell = (
            section_card.is_cheap_card_draw_spell
        )
        section_card_quantity = section_card.quantity
        if section_card_is_cheap_card_draw_spell:
            self._decklist._cheap_card_draw_spell_count += (
                section_card_quantity
            )

    def _get_cheap_mana_ramp_spell_count(self, section_card: Card):
        section_card_is_cheap_mana_ramp_spell = (
            section_card.is_cheap_mana_ramp_spell
        )
        section_card_quantity = section_card.quantity
        if section_card_is_cheap_mana_ramp_spell:
            self._decklist._cheap_mana_ramp_spell_count += (
                section_card_quantity
            )

    def _get_non_mythic_and_mythic_land_spell_mdfc_count(
        self, section_card: Card
    ):
        section_card_is_land_spell_mdfc = section_card.is_land_spell_mdfc
        section_card_rarity_lower = section_card.rarity.lower()
        section_card_quantity = section_card.quantity
        if section_card_is_land_spell_mdfc:
            if section_card_rarity_lower in ['common', 'uncommon', 'rare']:
                self._decklist._non_mythic_land_spell_mdfc_count += (
                    section_card_quantity
                )
            elif section_card_rarity_lower == 'mythic':
                self._decklist._mythic_land_spell_mdfc_count += (
                    section_card_quantity
                )

    def _get_is_commander_deck(self, decklist_section_name_lower: str):
        if decklist_section_name_lower == 'commander':
            self._decklist._is_commander_deck = True

    def _get_has_companion(self, decklist_section_name_lower: str):
        if decklist_section_name_lower == 'companion':
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
