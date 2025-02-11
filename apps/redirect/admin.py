from django.contrib import admin

from apps.redirect.models import RedirectRule


class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "redirect_url",
        "is_private",
        "redirect_identifier",
        "created",
        "modified",
    )
    ordering = ("created",)


admin.site.register(RedirectRule, RedirectRuleAdmin)
