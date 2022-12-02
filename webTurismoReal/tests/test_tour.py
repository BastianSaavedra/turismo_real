import pytest

from home.models import Tour

@pytest.mark.django_db
def test_tour_creation():
    tour = Tour.objects.create(
        tipoTour = '1',
        nombreTour = "El Baratie",
        horario_in = '00:00',
        horario_fin = '00:00',
        costo = 1234,
        comuna = 'Valdivia',
        status = '1'
    )
    assert tour.status == '1'
