from django.contrib.auth import authenticate
from rest_framework import serializers

from apis.v1.account.exceptions import CustomValidationError
from apis.v1.account.token import get_tokens_for_user
from account_app.models import User, Student, Otp


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("phone_number", "password", "full_name", "email", "token", "user_type")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_token(self, user):
        return get_tokens_for_user(user)

    def get_user_type(self, user):
        return user.user_type

    def to_representation(self, instance):
        # get super data
        data = super().to_representation(instance)

        return {
            "token": data.get("token"),
            "success": True,
            "role": data.get("user_type"),
        }


class TokenSerializer(serializers.Serializer):
    """
    show response token after successfully login and signup
    """
    refresh = serializers.CharField()
    access = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    """
    for use response login  serializer
    """
    success = serializers.BooleanField()
    token = TokenSerializer()
    is_staff = serializers.BooleanField()
    role = serializers.CharField()


class CreateResponseSerializer(serializers.Serializer):
    """
    for use response signup serializer
    """
    success = serializers.BooleanField()
    token = TokenSerializer()
    role = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    """
    used serializer UserLoginView
    """
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # get phone and password
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        # authenticate user request, phone, password
        user = authenticate(
            request=self.context.get('request'),
            phone_number=phone_number,
            password=password,
        )

        # invalid phone and password
        if not user:
            raise CustomValidationError(
                {
                    "message": "phone and password is invalid",
                    "success": False
                }
            )

        # create jwt token
        token = get_tokens_for_user(user)
        attrs['token'] = token
        attrs['tole'] = user.user_type
        attrs['is_staff'] = user.is_staff
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "nation_code",
            "phone_number",
            "user_type"
        )
        read_only_fields = (
            "user_type",
            "email",
            "phone_number",
        )


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = (
            "id",
            "user",
            "student_number",
            "student_image",
            "grade",
            "parent_phone"
        )
        read_only_fields = (
            "student_number",
        )

    def update(self, instance, validated_data):
        # get user data
        user_data = validated_data.pop('user', None)

        # update student field
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update user data
        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise CustomValidationError(
                {
                    "message": "phone number is invalid",
                    "success": False
                }
            )
        return value

    def create(self, validated_data):
        # get obj request
        request = self.context.get('request')

        return Otp.objects.create(
            phone_number=validated_data['phone_number'],
            device_ip=request.META.get('REMOTE_ADDR', "X_FORWARDED_FOR"),
        )

    def to_representation(self, instance):
        return {
            "message": "code sned"
        }


class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "رمزهای عبور وارد شده یکسان نیستند."})
        return data