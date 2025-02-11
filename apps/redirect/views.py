from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from apps.redirect.models import RedirectRule
from apps.redirect.serializers import RedirectIdentifierSerializer, RedirectRuleSerializer


class PublicRedirectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RedirectRule.objects.filter(is_private=False)
    serializer_class = RedirectRuleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "redirect_identifier"

    def retrieve(self, request: Request, redirect_identifier: str | None = None) -> HttpResponseRedirect:
        rule = get_object_or_404(self.get_queryset(), redirect_identifier=redirect_identifier)
        return HttpResponseRedirect(rule.redirect_url)


class PrivateRedirectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RedirectRule.objects.all()
    serializer_class = RedirectRuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "redirect_identifier"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, is_private=True)

    def retrieve(self, request: Request, redirect_identifier: str | None = None) -> HttpResponseRedirect:
        rule = get_object_or_404(self.get_queryset(), redirect_identifier=redirect_identifier)
        return HttpResponseRedirect(rule.redirect_url)


class UrlViewSet(viewsets.GenericViewSet):
    serializer_class = RedirectRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            redirect_rule = serializer.save()
            response_serializer = RedirectIdentifierSerializer(redirect_rule)
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request: Request, redirect_identifier: str | None = None) -> Response:
        redirect_rule = get_object_or_404(RedirectRule, redirect_identifier=redirect_identifier)

        if redirect_rule.owner != request.user:
            return Response({"error": "You do not have permission to update this redirect."}, HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(redirect_rule, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            redirect_rule = serializer.save()
            response_serializer = RedirectIdentifierSerializer(redirect_rule)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, redirect_identifier: str | None = None) -> Response:
        redirect_rule = get_object_or_404(RedirectRule, redirect_identifier=redirect_identifier)

        if redirect_rule.owner != request.user:
            return Response({"error": "You do not have permission to delete this redirect."}, HTTP_403_FORBIDDEN)

        redirect_rule.delete()
        return Response({"message": "Redirect deleted successfully."}, HTTP_204_NO_CONTENT)
