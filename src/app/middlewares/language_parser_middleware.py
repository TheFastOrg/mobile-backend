import re

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LanguageParserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        language = request.headers.get("Accept-Language")
        language_code = 'en'
        if language:
            language_match = re.search(r"(\w{2})(?:-\w{2})?", language)
            if language_match:
                matched_language = language_match.group(1)
                if matched_language == "ar":
                    language_code = "ar"
        request.scope["language"] = language_code
        return await call_next(request)
