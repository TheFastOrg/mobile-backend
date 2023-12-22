class BusinessError(Exception):
    def __init__(self, message="Business error occurred"):
        self.message = message
        super().__init__(self.message)


class OpeningTimeError(BusinessError):
    def __init__(self, message="Opening time should be before closing time"):
        super().__init__(message)


class WorkingDayOverlapError(BusinessError):
    def __init__(
        self, message="Working days should not have overlapping days or times"
    ):
        super().__init__(message)
