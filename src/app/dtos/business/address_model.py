from src.app.dtos.base_dto import BaseDTO


class AddressModel(BaseDTO):
    address_line1: str
    address_line2: str
    city: str
