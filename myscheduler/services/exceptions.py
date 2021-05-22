class FailureToRetrieveActivity(Exception):
    def __init__(self, message: str = "There was a failure to retrieve an activity!"):
        super().__init__(message)


class FailureToRetrieveCPFValidation(Exception):
    def __init__(self, message: str = "Failure to retrieve the CPF validation status!"):
        super().__init__(message)
