from django.shortcuts import render, redirect

from utils.analyzer import Analyzer
from utils.decklist_parser import DecklistParser


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
        form = request.POST
        decklist = form.get('decklist', '').strip()

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
            non_mythic_land_spell_mdfc_count = (
                analyzer.non_mythic_land_spell_mdfc_count
            )
            non_mythic_land_spell_mdfc_list = ', '.join(
                analyzer.non_mythic_land_spell_mdfc_list
            )
            mythic_land_spell_mdfc_count = (
                analyzer.mythic_land_spell_mdfc_count
            )
            mythic_land_spell_mdfc_list = ', '.join(
                analyzer.mythic_land_spell_mdfc_list
            )
            average_cmc = f'{analyzer.average_cmc:.1f}'
            recommended_number_of_lands = analyzer.recommended_number_of_lands

            # Store the result data in the session to be accessed after the redirect
            request.session['result_data'] = {
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
                        'non_mythic_land_spell_mdfc_count': non_mythic_land_spell_mdfc_count,
                        'non_mythic_land_spell_mdfc_list': non_mythic_land_spell_mdfc_list,
                        'mythic_land_spell_mdfc_count': mythic_land_spell_mdfc_count,
                        'mythic_land_spell_mdfc_list': mythic_land_spell_mdfc_list,
                        'average_cmc': average_cmc,
                        'recommended_number_of_lands': recommended_number_of_lands,
                    }

            # Redirect to a new URL to prevent form resubmission
            return redirect('result_page')
        except (ValueError, AttributeError, KeyError) as e:
            # Handle errors
            error_message = e
            return render(request, 'lands/index.html', {'error_message': error_message})
    else:
        # Clear any previous result data or error message from the session
        request.session.pop('result_data', None)
        return render(request, 'lands/index.html')


def result_page(request):
    result_data = request.session.get('result_data')

    if result_data:
        # Clear the stored result data from the session
        request.session.pop('result_data', None)
        return render(request, 'lands/index.html', {'result': result_data})
    else:
        # If accessed directly without proper redirection, go back to the index page
        return redirect('index')

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
