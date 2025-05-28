from rest_framework import serializers

from account_app.models import User
from exam_app.models import Exam


class ExamCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
        )

class ExamSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.only("phone_number", "full_name").filter(is_active=True, is_staff=True),
    )

    class Meta:
        model = Exam
        exclude = (
            "is_deleted",
            "deleted_at"
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
