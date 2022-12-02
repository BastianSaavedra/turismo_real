import pytest

from home.models import Usuario


# Test creacion Usuario Cliente
@pytest.mark.django_db
def test_user_creation():
    user = Usuario.objects.create_user(
        username = 'user_test',
        nombre = 'test_name',
        ap_paterno = 'test_ap_paterno',
        ap_materno = 'test_ap_materno',
        rut = '19384928',
        dv = '8',
        correo = 'test@example.com',
        telefono = '82839482',
    )
    # assert user.username == 'user_test'
    assert user.usuario_cliente

# Test creacion Usuario SuperAdministrador
@pytest.mark.django_db
def test_supert_administrador_creation():
    user = Usuario.objects.create_superuser(
        username = 'test_superuser',
        nombre = 'test_superuser_name',
        ap_paterno = 'test_superuser_ap_paterno',
        ap_materno = 'test_superuser_ap_materno',
        rut = '19384928',
        dv = '8',
        correo = 'test@example.com',
        telefono = '82839482',
        password = 'test_adminuser'
    )
    assert user.usuario_superAdministrador

# Test creacion Usuario Admin
@pytest.mark.django_db
def test_admin_creation():
    user = Usuario.objects.create(
        username = 'user_test',
        nombre = 'test_name',
        ap_paterno = 'test_ap_paterno',
        ap_materno = 'test_ap_materno',
        rut = '19384928',
        dv = '8',
        correo = 'test@example.com',
        telefono = '82839482',
        usuario_admin = True,
        usuario_cliente = False
    )
    assert user.usuario_admin

# Test creacion Usuario Funcionario
@pytest.mark.django_db
def test_funcionario_creation():
    user = Usuario.objects.create(
        username = 'user_test',
        nombre = 'test_name',
        ap_paterno = 'test_ap_paterno',
        ap_materno = 'test_ap_materno',
        rut = '19384928',
        dv = '8',
        correo = 'test@example.com',
        telefono = '82839482',
        usuario_admin = False,
        usuario_cliente = False,
        usuario_funcionario = True
    )
    assert user.usuario_funcionario


# Test creacion de Usuario con atributos de SuperAdministrador
@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):
        Usuario.objects.create_user(
            password = '12345',
            usuario_superAdministrador = True,
        )



    
