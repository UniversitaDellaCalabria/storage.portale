from django.apps import AppConfig


class AdvancedTrainingConfig(AppConfig):
    name = "advanced_training"
    verbose_name = "Advanced Training"
    
    def ready(self):
        import advanced_training.management.signals  