# # your_app/signals.py
# from django.apps import AppConfig
# from django.db.models.signals import post_save, post_delete
# from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

# from .models import PetModel

# post_save.connect(post_save_subscription, sender=PetModel,
#                   dispatch_uid="your_model_post_save")
# post_delete.connect(post_delete_subscription, sender=PetModel,
#                     dispatch_uid="your_model_post_delete")
