from src.core.entities.business.exceptions import BusinessNotFoundError
from src.core.entities.business.value_types import BusinessId


class TestBusiness:
    def test_get_by_id_should_raise_error(self, container):
        service = container.business_service()
        try:
            service.get_by_id(BusinessId())
        except BusinessNotFoundError:
            assert True
            return
        assert False
