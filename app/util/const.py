class Const:
    class DbMode:
        CREATE = 0
        UPDATE = 1
        DELETE = 1

    class LIMIT:
        TRANSCRIPT = 10

    class DelFlg:
        DELETE = True
        NOT_DELETE = False

    class SpecialChar:
        UNDERSCORE = "_"
        SPACE = " "

    class ResponseMessage:
        SUCCESS = "Successfully"

    class ResponseCode:
        SUCCESS = 200
        ERROR_VALIDATE = 400
        DUPLICATE = 409

    class LOG_LEVEL:
        ACCESS = "ACCESS"
        VALIDATE = "VALIDATE"
        EXCEPTION = "EXCEPTION"
        VIDEO_NOT_AVAILABLE = "Video not available or you have no right to access. Please contact admin"
        ATTACHMENT_NOT_AVAILABLE = "Attachment not available or you have no right to access. Please contact admin"
        CHANNEL_NOT_AVAILABLE = "Channel not available or you have no right to access. Please contact admin"
        INFO = "INFO"
        CHANNEL_NOT_PERMISSSION = "You cannot have permission"

    class NOTI_TYPE:
        VIDEO_READY = 1
        VIEWER = 2
        COMMENT = 3
        LIKE = 4
        MENTION = 9

        PARTICIPANT_VIDEO_READY = 5
        PARTICIPANT_VIEWER = 6
        PARTICIPANT_COMMENT = 7
        PARTICIPANT_LIKE = 8

    class GOOOGLE_CREDENTIAL:
        CLIENT_ID = '594601702974-dlqulqgb80rhjop07hir9e20vk3cm9k1.apps.googleusercontent.com'
        CLIENT_SECRET = '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'
        AUTH_CODE = 'authorization_code'
        REFS_TOKEN = 'refresh_token'
        URL_TOKEN = 'https://oauth2.googleapis.com/token'
        URL_REVOKE_TOKEN = 'https://oauth2.googleapis.com/revoke'

        def URL_GET_FILE(fileId):
            return 'https://www.googleapis.com/drive/v2/files/' + fileId

        def URL_READ_FILE(fileId):
            return 'https://www.googleapis.com/drive/v3/files/' + fileId + '?alt=media&source=downloadUrl'

        def google_api_headers(access_token):
            return {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json'}

    class ZOOM_CREDENTIAL:
        CLIENT_ID = 'Bje3QTwvQi68Gjnw2YiymA'
        CLIENT_SECRET = 'L6aQ3W5NWPs4tGZrtFUBgrkwZDDUfCTH'
        REDIRECT_URI = 'http://localhost:8081'
        AUTHORIZE = 'https://zoom.us/oauth/authorize'
        TOKEN_URL = 'https://zoom.us/oauth/token'
        REVOKE_URL = 'https://zoom.us/oauth/revoke'
        API_URL = 'https://api.zoom.us/v2'

    class INTEGRATION:
        NONE = '0'
        GOOGLE_MEET = '1'
        MS_TEAMS = '2'
        ZOOM = '3'

    class JWT_CONFIG:
        SECRET_KEY = "AVPyTXUZntKOR1DxIlr4"
        REFRESH_KEY= "PoyDIG8Ck0TcdpveH9Ba"
        REFRESH_EXPIRES_TIME_D = 2
        SECRET_KEY_TIME_M = 15
        