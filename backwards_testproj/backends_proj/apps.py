from django.apps import AppConfig

# 放置app的名字，尽量不要修改

class BackendsProjConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backends_proj"
