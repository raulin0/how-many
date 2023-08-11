from django.shortcuts import render

from lands.utils.analyzer import Analyzer
from lands.utils.decklist_parser import DecklistParser


def index(request):
    """
    Handles the index page view, including form submission and result rendering.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with rendered content.
    """
    if request.method == 'POST':
        # Get the decklist from the form data
        decklist = request.POST.get('decklist')
        if not decklist.strip():
            # If decklist is empty, render the index page
            return render(request, 'lands/index.html')

        # Parse the decklist and analyze it
        try:
            parser = DecklistParser(decklist)
            parser.parse_decklist()
            analyzer = Analyzer(parser.parsed_decklist)
            analyzer.analyze_decklist()

            # Extract data from the analyzer and parser
            companion_count = len(parser.parsed_decklist['companion'])
            companion = ', '.join(parser.parsed_decklist['companion'].keys())
            card_count = analyzer.card_count
            non_land_count = analyzer.non_land_count
            non_land_cmcs_count = analyzer.non_land_cmcs_count
            cheap_card_draw_count = analyzer.cheap_card_draw_count
            cheap_card_draw_list = ', '.join(analyzer.cheap_card_draw_list)
            cheap_card_scry_count = analyzer.cheap_card_scry_count
            cheap_card_scry_list = ', '.join(analyzer.cheap_card_scry_list)
            cheap_mana_ramp_count = analyzer.cheap_mana_ramp_count
            cheap_mana_ramp_list = ', '.join(analyzer.cheap_mana_ramp_list)
            non_mythic_mdfc_count = analyzer.non_mythic_mdfc_count
            non_mythic_mdfc_list = ', '.join(analyzer.non_mythic_mdfc_list)
            mythic_mdfc_count = analyzer.mythic_mdfc_count
            mythic_mdfc_list = ', '.join(analyzer.mythic_mdfc_list)
            average_cmc = f'{analyzer.average_cmc:.1f}'
            recommended_number_of_lands = analyzer.recommended_number_of_lands

            # Render the index page with result data
            return render(
                request,
                'lands/index.html',
                {
                    'result': {
                        'companion_count': companion_count,
                        'companion': companion,
                        'card_count': card_count,
                        'non_land_count': non_land_count,
                        'non_land_cmcs_count': non_land_cmcs_count,
                        'cheap_card_draw_count': cheap_card_draw_count,
                        'cheap_card_draw_list': cheap_card_draw_list,
                        'cheap_card_scry_count': cheap_card_scry_count,
                        'cheap_card_scry_list': cheap_card_scry_list,
                        'cheap_mana_ramp_count': cheap_mana_ramp_count,
                        'cheap_mana_ramp_list': cheap_mana_ramp_list,
                        'non_mythic_mdfc_count': non_mythic_mdfc_count,
                        'non_mythic_mdfc_list': non_mythic_mdfc_list,
                        'mythic_mdfc_count': mythic_mdfc_count,
                        'mythic_mdfc_list': mythic_mdfc_list,
                        'average_cmc': average_cmc,
                        'recommended_number_of_lands': recommended_number_of_lands,
                    }
                },
            )
        except (ValueError, AttributeError, KeyError) as e:
            # Handle errors and render the index page with an error message
            if isinstance(e, ValueError):
                error_message = e
            elif isinstance(e, AttributeError):
                error_message = e
            elif isinstance(e, KeyError):
                error_message = 'Invalid entry. You must explicitly enter each section that your deck list has. Example: Companion ... Deck ... Sideboard ...'

            return render(
                request, 'lands/index.html', {'error_message': error_message}
            )
    else:
        return render(request, 'lands/index.html')


def about(request):
    """
    Handles the about page view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with rendered content.
    """
    return render(request, 'lands/about.html')


def privacy(request):
    """
    Handles the privacy page view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with rendered content.
    """
    return render(request, 'lands/privacy.html')
