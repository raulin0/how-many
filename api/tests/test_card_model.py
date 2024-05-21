from django.contrib.auth.models import Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import CardModel


class CardModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        permissions = Permission.objects.filter(
            codename__in=[
                'add_cardmodel',
                'change_cardmodel',
                'delete_cardmodel',
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

        self.card = CardModel.objects.create(**self.card_data)

        self.url_list = reverse('cards-list')
        self.url_detail = reverse('cards-detail', kwargs={'pk': self.card.pk})

    def test_get_request_to_return_all_cards_returns_status_code_200(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.card.name)

    def test_post_request_to_create_card_returns_status_code_201(self):
        card_data = {
            'name': 'Cauldron Familiar',
            'layout': 'normal',
            'mana_cost': '{B}',
            'cmc': 1.0,
            'type_line': 'Creature — Cat',
            'rarity': 'common',
            'oracle_text': 'When Cauldron Familiar enters the battlefield, each opponent loses 1 life and you gain 1 life.\nSacrifice a Food: Return Cauldron Familiar from your graveyard to the battlefield.',
            'is_land': False,
            'is_cheap_card_draw_spell': False,
            'is_cheap_mana_ramp_spell': False,
            'is_land_spell_mdfc': False,
        }
        response = self.client.post(self.url_list, data=card_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_request_to_fully_update_card_returns_status_code_200(self):
        updated_data = {
            'name': 'Put Cauldron Familiar',
            'layout': 'normal',
            'mana_cost': '{B}',
            'cmc': 1.0,
            'type_line': 'Creature — Cat',
            'rarity': 'common',
            'oracle_text': 'When Cauldron Familiar enters the battlefield, each opponent loses 1 life and you gain 1 life.\nSacrifice a Food: Return Cauldron Familiar from your graveyard to the battlefield.',
            'is_land': False,
            'is_cheap_card_draw_spell': False,
            'is_cheap_mana_ramp_spell': False,
            'is_land_spell_mdfc': False,
        }
        response = self.client.put(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_request_to_partial_update_card_returns_status_code_200(
        self,
    ):
        updated_data = {'name': 'Patch Cauldron Familiar'}
        response = self.client.patch(self.url_detail, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request_to_delete_card_returns_status_code_204(self):
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_decks_action_returns_all_decks_in_which_the_card_is_present_returns_status_code_200(
        self,
    ):
        response = self.client.get(
            reverse('cards-decks', kwargs={'pk': self.card.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
