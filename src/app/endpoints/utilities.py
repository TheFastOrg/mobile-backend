from starlette.requests import Request

from src.core.entities.business.enums import SupportedLanguage


def language_parser(request: Request) -> SupportedLanguage:
    default_language_code = SupportedLanguage.EN

    language_header = request.headers.get("Accept-Language")
    if not language_header:
        return default_language_code

    language_code = language_header[:2]
    if language_code == "ar":
        return SupportedLanguage.AR

    return default_language_code
