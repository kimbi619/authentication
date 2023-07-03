from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed    

from .models import User



# class TokenPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         """
#         Get the token for the user and mark the last login date of the user
#         """
#         from django.utils import timezone
#         _obj = user
#         _obj.last_login = timezone.now()
#         _obj.save()
#         return RefreshToken.for_user(user)

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         if self.user is None:
#             raise AuthenticationFailed('Invalid email or password. Please try again.')

#         email = getattr(self.user, User.USERNAME_FIELD)

#         if not self.user.is_active:
#             raise AuthenticationFailed('Account is not activated. Please check your mails.')

#         if not email:
#             raise AuthenticationFailed('Please enter your email address.')

#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)
#         data["user"] = LoginSerializer(self.user).data
#         return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=256, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=256, min_length=6, write_only=True)
    class Meta:
        model = User
        # fields = ['email', 'password', 'groups']
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=5)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):

        return super().validate(attrs)



# relativeLink = reverse('password_reset_confirm')
# absurl = 'http://'+current_site+relativeLink
# email_body = f'To Reset password for {user.username} user the link below'
# data = {
#     'email_body': email_body,
#     'to_email': user.email,
#     'email_subject': 'Reset password',
    
# }