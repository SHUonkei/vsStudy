class AuthenticationError(Exception):
    """アプリケーション内で利用する基底のエラークラス"""

    msg = ""
    status_code = 500


class BadLoginReuquestError(AuthenticationError):
    msg = "userNameとpasswordの指定は必須です"
    status_code = 400


class LoginFailureError(AuthenticationError):
    msg = "userNameまたはpasswordが誤っています"
    status_code = 401