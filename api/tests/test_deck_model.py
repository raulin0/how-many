from django.contrib.auth.models import Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import DeckModel


class DeckModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        permissions = Permission.objects.filter(
            codename__in=[
                'add_deckmodel',
                'change_deckmodel',
                'delete_deckmodel',
            ]
        )
        self.user.user_permissions.add(*permissions)
        self.client.force_authenticate(user=self.user)

        self.deck_data = {
            'is_commander_deck': False,
            'has_companion': True,
            'maindeck_card_count': 60,
            'non_land_card_count': 38,
            'non_land_cmcs_count': 63.0,
            'cheap_card_draw_spell_count': 4,
            'cheap_mana_ramp_spell_count': 0,
            'non_mythic_land_spell_mdfc_count': 0,
            'mythic_land_spell_mdfc_count': 0,
            'average_cmc': 1.6578947368421053,
            'recommended_number_of_lands': 22,
        }

        self.deck = DeckModel.objects.create(**self.deck_data)

        self.url_list = reverse('decks-list')
        self.url_detail = reverse('decks-detail', kwargs={'pk': self.deck.pk})

    def test_get_request_to_return_all_decks_returns_status_code_200(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['average_cmc'],
            self.deck.average_cmc,
        )

    def test_post_request_to_create_deck_returns_status_code_201(self):
        deck_data = {
            'is_commander_deck': False,
            'has_companion': False,
            'maindeck_card_count': 60,
            'non_land_card_count': 41,
            'non_land_cmcs_count': 104.0,
            'cheap_card_draw_spell_count': 16,
            'cheap_mana_ramp_spell_count': 0,
            'non_mythic_land_spell_mdfc_count': 0,
            'mythic_land_spell_mdfc_count': 0,
            'average_cmc': 2.5365853658536586,
            'recommended_number_of_lands': 20,
        }
        response = self.client.post(self.url_list, data=deck_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_request_to_fully_update_deck_returns_status_code_200(self):
        updated_data = {
            'is_commander_deck': False,
            'has_companion': True,
            'maindeck_card_count': 60,
            'non_land_card_count': 41,
            'non_land_cmcs_count': 104.0,
            'cheap_card_draw_spell_count': 16,
            'cheap_mana_ramp_spell_count': 0,
            'non_mythic_land_spell_mdfc_count': 0,
            'mythic_land_spell_mdfc_count': 0,
            'average_cmc': 2.5365853658536586,
            'recommended_number_of_lands': 20,
        }
        response = self.client.put(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_request_to_partial_update_deck_returns_status_code_200(
        self,
    ):
        updated_data = {'recommended_number_of_lands': 22}
        response = self.client.patch(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request_to_delete_deck_returns_status_code_204(self):
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cards_action_returns_all_cards_belonging_to_the_deck_returns_status_code_200(
        self,
    ):
        response = self.client.get(
            reverse('decks-cards', kwargs={'pk': self.deck.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_process_action_with_decklist_without_cards_set_codes_and_numbers_returns_status_code_201(
        self,
    ):
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
        response = self.client.post(
            reverse('decks-process'), data={'decklist_text': decklist_text}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_process_action_with_decklist_with_cards_set_codes_and_numbers_returns_status_code_201(
        self,
    ):
        decklist_text = """Deck
1 Archfiend of the Dross (ONE) 82
3 Blightstep Pathway (KHM) 252
4 Blood Crypt (RNA) 245
2 Fatal Push (KLR) 84
4 Bloodtithe Harvester (VOW) 232
1 Duress (M19) 94
3 Dusk Legion Zealot (RIX) 70
4 Fable of the Mirror-Breaker (NEO) 141
4 Mutavault (M14) 228
1 Go for the Throat (BRO) 102
1 Heartless Act (IKO) 91
2 Hive of the Eye Tyrant (AFR) 258
2 Swamp (KTK) 254
4 Sulfurous Springs (DMU) 256
2 Preacher of the Schism (LCI) 113
4 Sorin, Imperious Bloodlord (M20) 115
2 Thoughtseize (AKR) 127
1 Mountain (KTK) 256
1 Takenuma, Abandoned Mire (NEO) 278
1 Thoughtseize (AKR) 127
4 Vein Ripper (MKM) 110
2 Archfiend of the Dross (ONE) 82
4 Blackcleave Cliffs (ONE) 248
2 Fatal Push (KLR) 84
1 Thoughtseize (AKR) 127

Sideboard
1 Duress (M19) 94
1 Gix's Command (BRO) 97
1 Grafdigger's Cage (M20) 227
2 Liliana of the Veil (DMU) 97
2 Damping Sphere (DAR) 213
1 Duress (M19) 94
2 Path of Peril (VOW) 124
1 Quakebringer (KHM) 145
4 Leyline of the Void (M20) 107
"""
        response = self.client.post(
            reverse('decks-process'), data={'decklist_text': decklist_text}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_process_action_with_empty_decklist_returns_status_code_400(self):
        decklist_text = ''
        response = self.client.post(
            reverse('decks-process'), data={'decklist_text': decklist_text}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_action_without_sections_names_returns_status_code_400(
        self,
    ):
        decklist_text = """1 Archfiend of the Dross (ONE) 82
3 Blightstep Pathway (KHM) 252
4 Blood Crypt (RNA) 245
2 Fatal Push (KLR) 84
4 Bloodtithe Harvester (VOW) 232
1 Duress (M19) 94
3 Dusk Legion Zealot (RIX) 70
4 Fable of the Mirror-Breaker (NEO) 141
4 Mutavault (M14) 228
1 Go for the Throat (BRO) 102
1 Heartless Act (IKO) 91
2 Hive of the Eye Tyrant (AFR) 258
2 Swamp (KTK) 254
4 Sulfurous Springs (DMU) 256
2 Preacher of the Schism (LCI) 113
4 Sorin, Imperious Bloodlord (M20) 115
2 Thoughtseize (AKR) 127
1 Mountain (KTK) 256
1 Takenuma, Abandoned Mire (NEO) 278
1 Thoughtseize (AKR) 127
4 Vein Ripper (MKM) 110
2 Archfiend of the Dross (ONE) 82
4 Blackcleave Cliffs (ONE) 248
2 Fatal Push (KLR) 84
1 Thoughtseize (AKR) 127

1 Duress (M19) 94
1 Gix's Command (BRO) 97
1 Grafdigger's Cage (M20) 227
2 Liliana of the Veil (DMU) 97
2 Damping Sphere (DAR) 213
1 Duress (M19) 94
2 Path of Peril (VOW) 124
1 Quakebringer (KHM) 145
4 Leyline of the Void (M20) 107
"""
        response = self.client.post(
            reverse('decks-process'), data={'decklist_text': decklist_text}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
