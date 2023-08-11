import requests


class CardDataFetcher:
    """
    A class for fetching card data from the Scryfall API and caching it.
    ...
    """

    def __init__(self):
        """
        Initializes the CardDataFetcher instance with an empty card cache.
        """
        self._card_cache = {}

    def get_card_data(self, card):
        """
        Fetches card data from the Scryfall API for the specified card.

        Args:
            card (str): The name of the card to fetch data for.

        Returns:
            dict: A dictionary containing the card data from the API response.
                  Returns None if the request fails.
        """
        if card in self._card_cache:
            return self._card_cache[card]

        try:
            response = requests.get(
                f'https://api.scryfall.com/cards/named?exact={card}'
            )
            response.raise_for_status()
            card_data = response.json()
            self._card_cache[card] = card_data
            return card_data
        except requests.exceptions.RequestException:
            return None
