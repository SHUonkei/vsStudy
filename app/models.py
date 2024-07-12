#login機能のための定義
#UserMixin、ログイン・ログアウトで必要なライブラリをインポート
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#パスワードをハッシュ化するライブラリをインポート
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin):
    def __init__(self, player_id: str, name:str) -> None:
        """user_idにはユーザーを一意に特定できる値を指定し、その他の項目は任意で設定する

        Args:
            user_id (str): ユーザーを一意に特定できる値
        """
        self.user_id = player_id
        self.user_name = name

    def get_id(self):
        """このメソッドは必要に応じて定義する必要があり、デフォルトではself.idの値が返されるので、
        self.id以外の値を返したい場合はget_idのメソッドを上書きする
        self.get_idで返す値はユーザーを一意に特定できる値を返すこと
        仮に単一の項目では一意の値とならない場合は複数項目をTuple(ハッシュ化可能な値)で返すと良い
        """
        return self.user_id

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