import pytest
from radon.iot import serializers, models


def test_WisolValidation_get_wisol_or_error(mocker):
    mock_get = mocker.patch.object(models.Wisol.objects, 'get', side_effect=models.Wisol.DoesNotExist)
    ser = serializers.WisolValidation()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.get_wisol_or_error('412344')
    mock_get.assert_called_with(serie='412344')


def test_WisolValidation_validate_wisol_disponible(mocker):
    mock_wisol = mocker.MagicMock(spec=models.Wisol)
    mock_wisol.activo = False
    get_wisol_or_error = mocker.patch.object(serializers.WisolValidation, 'get_wisol_or_error', return_value=mock_wisol)
    ser = serializers.WisolValidation()
    serie = 'foo_serie'
    assert ser.validate_wisol(serie) == serie
    get_wisol_or_error.assert_called_with(serie)


def test_WisolValidation_validate_wisol_ocupado(mocker):
    mock_wisol = mocker.MagicMock(spec=models.Wisol)
    mock_wisol.activo = True
    get_wisol_or_error = mocker.patch.object(serializers.WisolValidation, 'get_wisol_or_error', return_value=mock_wisol)
    ser = serializers.WisolValidation()
    serie = 'foo_serie'
    error_message = 'El chip Wisol ya tiene un dispositivo asignado'
    with pytest.raises(serializers.serializers.ValidationError) as err:
        ser.validate_wisol(serie)
    assert error_message in str(err.value)
    get_wisol_or_error.assert_called_with(serie)


def test_DeviceTypeSerializer_Meta():
    ser = serializers.DeviceTypeSerializer()
    assert ser.Meta.fields == ['pk', 'key', 'name']
    assert ser.Meta.model == models.DeviceType


def test_WisolSerializer_Meta():
    ser = serializers.WisolSerializer()
    assert ser.Meta.fields == ['pk', 'serie', 'pac', 'deviceTypeId', 'prototype', ]
    assert ser.Meta.model == models.Wisol
