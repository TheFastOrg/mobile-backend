from src.app.dtos.business import (
    SearchBusinessRequest,
    SearchBusinessResponse,
    SearchBusinessLocationModel,
    LocationModel, AddressModel, WorkingHourModel,
)
from src.core.entities.business.business import Business
from src.core.entities.business.queries import BusinessSearchQuery


class BusinessMapper:
    @staticmethod
    def to_core_query(query: SearchBusinessRequest) -> BusinessSearchQuery:
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
        )

        if isinstance(query.location, SearchBusinessLocationModel):
            return_query.latitude = query.location.latitude
            return_query.longitude = query.location.longitude
            return_query.radiusInKM = query.location.radiusInKM

        return return_query

    @staticmethod
    def to_search_response(business: Business) -> SearchBusinessResponse:
        return SearchBusinessResponse(
            id=business.business_id.value,
            name=business.names.default_name(),
            number_of_reviews=business.number_of_reviews,
            overall_rating=business.overall_rating,
            location=LocationModel(
                latitude=business.location.latitude,
                longitude=business.location.longitude,
            ),
            address=AddressModel(
                city=business.address.city,
                address_line1=business.address.address_line1,
                address_line2=business.address.address_line2
            ),
            tags=business.tags,
            working_hours=[
                WorkingHourModel(day=item.day,
                                 opening_time=item.opening_time,
                                 closing_time=item.closing_time)
                for item
                in business.working_days]
        )
