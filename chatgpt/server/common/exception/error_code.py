#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ERROR_CODE:
    """Error code
    """
    DEFAULT = 10000

    # Authentication related errors 100001 ~ 110000
    class AUTH:
        # Not logged in
        NO_LOGIN = 100001
        # Unauthorized, keep unique when combined with 403 status code
        FORBIDDEN = 100002

    # Resource related 120000 ~ 130000
    class RESOURCE:
        # No resource found
        NO_RESOURCE = 120001
        # No resource found
        NOT_FOUND = 120002
        # Response header parameter error
        RES_HEADERS_PARAMS_ERROR = 120003

    # User input data related 130000 ~ 140000
    class USER_DATA:
        # Invalid field, incorrect parameters
        FIELD_VALID_ERROR = 130001

    # Service related 140000 ~ 150000
    class SERVER:
        # Model error
        MODEL_ERROR = 140001
        # Parameter error
        PARAMS_ERROR = 140002
        # Third-party request error
        REQUEST_ERROR = 140003
        # Operation error
        OPERATION_ERROR = 140004
        # es insertion error
        ES_INDEX_ERROR = 140005
        # Cutting function
        FUNCTION_ERROR = 140006
        # Data operation exception
        DB_ERROR = 140007
        # prompt tokens too long
        PROMPT_TOKENS_LENGTH = 140008
        # ai return does not contain code
        AI_RESPONSE_NO_CODE = 140009

        # gpt exception
        GPT_ERROR = 170002

        # Required parameter missing exception
        REQUIRE_PARAMS_MISSING_ERROR = 180002

        # Retry exception
        RETRY_ERROR = 180003

        # Parameter type error exception
        PARAMS_TYPE_ERROR = 180005

        # Manual case step error
        MANUAL_CASE_ERROR = 180006
