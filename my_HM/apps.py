from django.apps import AppConfig




class MyHmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_HM"

    def ready(self):
        import my_HM.signals