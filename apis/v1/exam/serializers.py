from rest_framework import serializers

from account_app.models import User
from exam_app.models import Exam, Question, ExamAttempt, Option, UserAnswer


class ExamCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
        )

class ExamSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        exclude = (
            "is_deleted",
            "deleted_at"
        )

    def create(self, validated_data):
        request = self.context.get("request")
        return Exam.objects.create(
            creator_id=request.user.id,
            **validated_data
        )

    def to_representation(self, instance):
        # get super data
        data = super().to_representation(instance)
        data['creator'] = ExamCreatorSerializer(instance.creator).data

        # get obj request
        request = self.context.get("request")

        # pop property for not admin user
        if not request.user.is_staff:
            data.pop("is_active", None)
            data.pop("is_active", None)
        return data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = (
            "is_deleted",
            "deleted_at"
        )
        read_only_fields = ("exam",)

    def create(self, validated_data):
        exam_pk = self.context.get("exam_pk")
        return Question.objects.create(
            exam_id=exam_pk,
            **validated_data
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if not request.user.is_staff:
            data.pop("is_active", None)
            data.pop("created_at", None)
            data.pop("updated_at", None)
        return data


class ExamAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        exclude = ("is_deleted", "deleted_at")
        read_only_fields = ("exam", "user", "score", "ip_address", "result_color")

    def to_representation(self, instance):
        # super class
        data = super().to_representation(instance)
        # get obj request
        request = self.context.get("request")

        # check user
        if not request.user.is_staff:
            data.pop("created_at", None)
            data.pop("updated_at", None)
            data.pop("user", None)
        return data

    def get_fields(self):
        # super
        field = super().get_fields()

        # get user
        user = self.context.get("request").user

        #check user
        if not user.is_staff:
            field.pop("user", None)
        return field

    def validate(self, attr):
        # get exam pk from urls
        exam_pk = self.context.get('exam_pk')

        # get user id
        user_id = self.context.get('request').user.id

        # filter exam_attempts
        exam_attempts = Exam.objects.filter(
            id=exam_pk
        ).only("title")

        # check exam attempts
        if not exam_attempts:
            raise serializers.ValidationError(
                detail={"message": "No exam attempts for this exam."},
                code="not-found"
            )

        # validate unique_together
        if ExamAttempt.objects.filter(
            exam_id=exam_pk,
            user_id=user_id
        ).exists():
            raise serializers.ValidationError(
                detail={"message": "Exam attempt already exists for this exam."},
                code="already-exists"
            )

        return attr

    def create(self, validated_data):
        # get exam pk from urls
        exam_pk = self.context.get('exam_pk')

        # get user id from obj request
        request = self.context.get('request')
        user_id = request.user.id
        return ExamAttempt.objects.create(
            exam_id=exam_pk,
            user_id=user_id,
            ip_address=request.META.get('REMOTE_ADDR', "X_FORWARDED_FOR")
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = (
            "is_deleted",
            "deleted_at",
            "is_correct"
        )


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        exclude = (
            "is_deleted",
            "deleted_at",
        )
