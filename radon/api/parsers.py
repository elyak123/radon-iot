from rest_framework.parsers import BaseParser


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain; charset=UTF-8'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
