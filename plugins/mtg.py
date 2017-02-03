import re

from YAuB.plugins import Plugin


class MtgPlugin(Plugin):

    def __init__(self):
        self.name = 'MtgPlugin'
        self.description = 'Plugin for displaying Magic: the Gathering decks'

        self.header_includes = [
            '<script src="https://deckbox.org/assets/external/tooltip.js"></script>',
            '<script src="https://deckbox.org/assets/external/decks.js"></script>'
        ]
        self.footer_includes = [
            "<script>Deckbox.utils.DeckParser.initializeMyfreeforum('mtg');</script>"
        ]
        self.replace = [
            ('[deck-view]', '<table class="table table-bordered"><tr>'),
            ('[col-titles]', '<td><b>'),
            ('[/col-titles]', '</b></td></tr><tr>'),
            ('[deck]', '<td><span class="postbody">[deck]'),
            ('[/deck]', '[/deck]</span></td>'),
            ('[/deck-view]', '</tr></table>'),
            ('[card]', '<span class="postbody">[card]'),
            ('[/card]', '[/card]</span>'),
        ]

        self.regex = [
            (None, None)
        ]

    def transmute(self, data):
        matches = re.findall(r"(?<=\[deck\]\n)(.*?)(?=\[\/deck\])", data, re.DOTALL)
        for match in matches:
            # Replace markdown added chars with html for deckbox api
            orig = match
            match = match.replace('<p>', '')
            match = match.replace('</p>', '')
            match = match.replace('\n', '<br />')
            self.replace.append((orig, match))

        matches = re.findall(r"(?<=\[col-titles\])(?:.*?)(?:.*?)(?=\[/col-titles\])", data, re.DOTALL)
        for match in matches:
            orig = match
            match = match.replace('|', '</b></td><td><b>')
            self.replace.append((orig, match))


def plug():
    plug = MtgPlugin()
    return plug
