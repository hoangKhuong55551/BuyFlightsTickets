from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrIdAuthBackend(ModelBackend):
    """
    Cho phép xác thực tài khoản (bao gồm cả Django Admin) bằng:
    - Email
    - Mã định danh riêng (member_id: SKB-XXXXXXXX)
    - Username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        if not username or not password:
            return None

        identifier = username.strip()

        # Tìm user theo email, mã ID (profile__member_id), hoặc username
        user = User.objects.filter(
            Q(email__iexact=identifier) |
            Q(profile__member_id__iexact=identifier) |
            Q(username__iexact=identifier)
        ).first()

        if user and user.check_password(password):
            return user
        return None
