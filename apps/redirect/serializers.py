from django.contrib.auth.models import User
from rest_framework import serializers

from apps.redirect.models import RedirectRule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RedirectRuleSerializer(serializers.Serializer):
    owner = UserSerializer(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    redirect_url = serializers.URLField()
    is_private = serializers.BooleanField()
    redirect_identifier = serializers.CharField(max_length=16, read_only=True)

    def create(self, validated_data) -> RedirectRule:
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return RedirectRule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RedirectIdentifierSerializer(serializers.Serializer):
    redirect_identifier = serializers.CharField(read_only=True)
