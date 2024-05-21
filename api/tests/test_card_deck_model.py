from django.contrib.auth.models import Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import CardDeckModel, CardModel, DeckModel


class CardDeckModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        permissions = Permission.objects.filter(
            codename__in=[
                'add_carddeckmodel',
                'change_carddeckmodel',
                'delete_carddeckmodel',
            ]
        )
        self.user.user_permissions.add(*permissions)
        self.client.force_authenticate(user=self.user)

        self.card_data = {
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

        self.card = CardModel.objects.create(**self.card_data)
        self.deck = DeckModel.objects.create(**self.deck_data)

        self.card_deck_data = {
            'section': 'companion',
            'quantity': 1,
            'card': self.card,
            'deck': self.deck,
        }

        self.card_deck = CardDeckModel.objects.create(**self.card_deck_data)

        self.url_list = reverse('card_decks-list')
        self.url_detail = reverse(
            'card_decks-detail', kwargs={'pk': self.card_deck.pk}
        )

    def test_get_request_to_return_all_card_decks_successfully(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['deck'], self.card_deck.deck.id
        )

    def test_post_request_to_create_card_deck_successfully(self):
        card_data = {
            'name': 'Fatal Push',
            'layout': 'normal',
            'mana_cost': '{B}',
            'cmc': 1.0,
            'type_line': 'Instant',
            'rarity': 'uncommon',
            'oracle_text': 'Destroy target creature if it has mana value 2 or less.\nRevolt — Destroy that creature if it has mana value 4 or less instead if a permanent you controlled left the battlefield this turn.',
            'is_land': False,
            'is_cheap_card_draw_spell': False,
            'is_cheap_mana_ramp_spell': False,
            'is_land_spell_mdfc': False,
        }

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

        card = CardModel.objects.create(**card_data)
        deck = DeckModel.objects.create(**deck_data)

        card_deck_data = {
            'section': 'deck',
            'quantity': 3,
            'card': card.id,
            'deck': deck.id,
        }

        response = self.client.post(self.url_list, data=card_deck_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_request_to_fully_update_card_deck_successfully(self):
        updated_data = {
            'section': 'sideboard',
            'quantity': 2,
            'card': self.card.id,
            'deck': self.deck.id,
        }
        response = self.client.put(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_request_to_partial_update_card_deck_successfully(self):
        updated_data = {'section': 'commander'}
        response = self.client.patch(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request_to_delete_card_deck_successfully(self):
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
