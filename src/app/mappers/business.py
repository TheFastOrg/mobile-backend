from src.app.dtos.business.address_model import AddressModel
from src.app.dtos.business.location_model import LocationModel
from src.app.dtos.business.search_business_location_model import (
    SearchBusinessLocationModel,
)
from src.app.dtos.business.search_business_request import SearchBusinessRequest
from src.app.dtos.business.search_business_response import SearchBusinessResponse
from src.app.dtos.business.wokring_hour_model import WorkingHourModel
from src.core.entities.business.business import Business
from src.core.entities.business.enums import SupportedLanguage
from src.core.entities.business.queries import BusinessSearchQuery


class BusinessMapper:
    @staticmethod
    def to_core_query(
        query: SearchBusinessRequest, language: SupportedLanguage
    ) -> BusinessSearchQuery:
        return_query = BusinessSearchQuery(
            type=query.type,
            name=query.name,
            categoryName=query.categoryName,
            categories=query.categories,
            tags=query.tags,
            features=query.features,
            openedNow=query.openedNow,
            page_size=query.page_size,
            page_number=query.page_number,
            language=language,
            sortBy=query.sortBy,
        )

        if isinstance(query.location, SearchBusinessLocationModel):
            return_query.latitude = query.location.latitude
            return_query.longitude = query.location.longitude
            return_query.radiusInKM = query.location.radiusInKM

        return return_query

    @staticmethod
    def to_search_response(
        business: Business, language: SupportedLanguage
    ) -> SearchBusinessResponse:
        result = SearchBusinessResponse(
            id=business.business_id.value,
            name=business.names.name(language),
            number_of_reviews=business.number_of_reviews,
            overall_rating=business.overall_rating,
            location=LocationModel(
                latitude=business.location.latitude,
                longitude=business.location.longitude,
            ),
            tags=business.tags,
            working_hours=[
                WorkingHourModel(
                    day=item.day,
                    opening_time=item.opening_time,
                    closing_time=item.closing_time,
                )
                for item in business.working_days
            ],
        )
        if business.address:
            result.address = AddressModel(
                city=business.address.city,
                address_line1=business.address.address_line1,
                address_line2=business.address.address_line2,
            )
        return result
