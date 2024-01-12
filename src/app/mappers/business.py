from src.app.dtos.business import (
    SearchBusinessRequest,
    LocationRequest,
    SearchBusinessResponse,
)
from src.core.entities.business.business import Business
from src.core.entities.business.queries import BusinessSearchQuery


class BusinessMapper:
    @staticmethod
    def to_core_query(query: SearchBusinessRequest) -> BusinessSearchQuery:
        returnQuery = BusinessSearchQuery(
            type=query.type,
            name=query.name,
            categoryName=query.categoryName,
            categories=query.categories,
            tags=query.tags,
            features=query.features,
            openedNow=query.openedNow,
            page_size=query.page_size,
            page_number=query.page_number,
        )

        if isinstance(query.location, LocationRequest):
            returnQuery.latitude = query.location.latitude
            returnQuery.longitude = query.location.longitude
            returnQuery.radiusInKM = query.location.radiusInKM

        return returnQuery

    @staticmethod
    def to_search_response(business: Business) -> SearchBusinessResponse:
        return SearchBusinessResponse(
            id=business.business_id.value, name=business.names.default_name()
        )
