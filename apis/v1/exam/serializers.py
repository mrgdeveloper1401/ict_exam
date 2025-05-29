from django.utils import timezone
from rest_framework import serializers

from account_app.models import User
from apis.v1.account.exceptions import CustomValidationError
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
            "deleted_at",
            "created_at",
            "updated_at",
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
        return data

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("text", "id")


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

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

        # filter exam
        exam = Exam.objects.filter(
            id=exam_pk
        ).only("title")

        # check exam attempts if not exits rais validation error
        if not exam:
            raise serializers.ValidationError(
                detail={"message": "No exam attempts for this exam."},
                code="not-found"
            )
        # else:
        # Checking the exam entry time
        #     if exam.last().exam_start_time > timezone.now():
        #         raise CustomValidationError(
        #             {
        #                 "message": "The exam hasn't started yet.",
        #                 "success": False
        #             }
        #         )

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


class SimpleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("text",)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        exclude = (
            "is_deleted",
            "deleted_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # edit representation question
        data['question'] = SimpleQuestionSerializer(instance.question).data
        return data


class CreateFieldUserAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.select_related("exam").only(
            "exam__title"
        )
    )


class CreateUserAnswerSerializer(serializers.Serializer):
    data = CreateFieldUserAnswerSerializer(many=True)

    def create(self, validated_data):
        data = validated_data.pop("data")

        if not data:
            raise CustomValidationError({
                "message": "you must send data",
                "success": False
            })

        request = self.context.get("request")
        user = request.user

        # پیدا کردن امتحان
        first_question = data[0]["question"]
        exam = first_question.exam

        # تلاش کاربر برای امتحان
        exam_attempt = ExamAttempt.objects.filter(
            user=user,
            exam=exam,
        ).first()

        if not exam_attempt:
            raise CustomValidationError({
                "message": "شما ابتدا باید در آزمون ثبت‌نام کنید.",
                "success": False
            })

        correct_count = 0
        total_count = len(data)
        created_answers = []

        for item in data:
            question = item["question"]
            answer_value = item["answer"]

            # بررسی وجود گزینه صحیح برای سوال
            try:
                selected_option = question.options.get(id=int(answer_value))
            except Option.DoesNotExist:
                selected_option = None

            # بررسی صحت پاسخ
            is_correct = selected_option.is_correct if selected_option else False
            if is_correct:
                correct_count += 1

            # ذخیره پاسخ
            user_answer = UserAnswer(
                question=question,
                option=selected_option,
                answer=answer_value,
            )
            created_answers.append(user_answer)

        # ذخیره‌ی انبوه پاسخ‌ها
        UserAnswer.objects.bulk_create(created_answers)

        #  نمره
        score = round((correct_count / total_count) * 100, 2)

        # save score user
        exam_attempt.score = score
        exam_attempt.end_time = timezone.now()
        exam_attempt.save()

        return {
            "score": score,
            "correct_answers": correct_count,
            "total_questions": total_count
        }
