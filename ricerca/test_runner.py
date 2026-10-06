# from django.test.runner import DiscoverRunner
# from django.apps import apps


# class ManagedModelTestRunner(DiscoverRunner):
#     """Durante i test forza managed=True, così le tabelle vengono create."""

#     def setup_test_environment(self, *args, **kwargs):
#         super().setup_test_environment(*args, **kwargs)
#         self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
#         for m in self.unmanaged_models:
#             m._meta.managed = True

#     def teardown_test_environment(self, *args, **kwargs):
#         super().teardown_test_environment(*args, **kwargs)
#         for m in self.unmanaged_models:
#             m._meta.managed = False
