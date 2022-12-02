# from django.test import TestCase
# from home.models import Usuario

# # Create your tests here.


# class UsuarioTestCase(TestCase):

#     @classmethod
#     def setUp(self):
#         Usuario.objects.create(
#             username = 'user_test',
#             nombre = 'test_name',
#             ap_paterno = 'test_ap_paterno',
#             ap_materno = 'test_ap_materno',
#             rut = '19384928',
#             dv = '8',
#             correo = 'test@example.com',
#             telefono = '82839482',
#         )

#     def test_username_label(self):
#         user = Usuario.objects.get(username='user_test')
#         field_label = user._meta.get_field('username').verbose_name
#         self.assertEqual(field_label, 'username')


