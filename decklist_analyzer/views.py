from django.shortcuts import redirect, render

from decklist_analyzer.utils.analyzer import Analyzer
from decklist_analyzer.utils.decklist_parser import DecklistParser


def index(request):
    """
    Handles the index page view, including decklist parsing and analysis.

    This view function handles both GET and POST requests. For GET requests, it checks
    if there is any stored result data or error message in the session, and renders the
    appropriate template accordingly. For POST requests, it retrieves the decklist from
    the form data, parses and analyzes it using the DecklistParser and Analyzer classes.
    If the parsing and analysis are successful, it collects various data such as card
    counts, companion information, card draw counts, etc., and stores this data in the
    session. Then, it redirects back to the index page to display the analyzed data.
    If there's an error during parsing or analysis, it catches the exceptions, stores
    an error message in the session, and redirects back to the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object that redirects to the index page with
        analyzed data, or with an error message if the parsing/analysis fails.
    """
    if request.method == 'POST':
        form = request.POST
        decklist = form.get('decklist', '').strip()

        request.session['preloaded_decklist'] = decklist

        try:
            parser = DecklistParser(decklist)
            parser.parse_decklist()
            analyzer = Analyzer(parser.parsed_decklist)
            analyzer.analyze_decklist()

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

            return redirect('index')

        except (ValueError, AttributeError, KeyError) as e:
            request.session['error_message'] = str(e).replace("'", '')

            return redirect('index')
    else:

        if 'result_data' in request.session:
            preloaded_decklist = request.session['preloaded_decklist']
            request.session.pop('preloaded_decklist', None)
            result_data = request.session['result_data']
            request.session.pop('result_data', None)
            return render(
                request,
                'decklist_analyzer/index.html',
                {'result': result_data, 'preloaded_decklist' : preloaded_decklist},
            )

        elif 'error_message' in request.session:
            preloaded_decklist = request.session['preloaded_decklist']
            request.session.pop('preloaded_decklist', None)
            error_message = request.session['error_message']
            request.session.pop('error_message', None)
            return render(
                request,
                'decklist_analyzer/index.html',
                {'error_message': error_message, 'preloaded_decklist' : preloaded_decklist},
            )


        request.session['preloaded_decklist'] = '''
Companion
1 Jegantha, the Wellspring

Deck
2 Sulfurous Springs
3 Blackcleave Cliffs
1 Mountain
1 Swamp
4 Blood Crypt
4 Fatal Push
1 Ramunap Ruins
4 Thoughtseize
4 Mayhem Devil
3 Cauldron Familiar
3 Claim the Firstborn
4 Witch's Oven
1 Kroxa, Titan of Death's Hunger
4 Blightstep Pathway
4 Deadly Dispute
2 Den of the Bugbear
2 Hive of the Eye Tyrant
4 Bloodtithe Harvester
4 Fable of the Mirror-Breaker
1 Takenuma, Abandoned Mire
1 Sokenzan, Crucible of Defiance
3 Unlucky Witness

Sideboard
1 Kolaghan's Command
2 Rending Volley
1 Jegantha, the Wellspring
2 Unlicensed Hearse
2 Duress
2 Furnace Reins
2 Damping Sphere
1 Abrade
2 Ob Nixilis, the Adversary 
        '''

        preloaded_decklist = request.session['preloaded_decklist']
        request.session.pop('preloaded_decklist', None)
        return render(request, 'decklist_analyzer/index.html', {'preloaded_decklist' : preloaded_decklist})
