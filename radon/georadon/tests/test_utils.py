import os
from pathlib import Path
import pytest
from radon.georadon.utils import get_path_for_shape


def test_get_path_for_production_shape(mocker):
    mocker.patch.object(
        Path, 'exists', side_effect=[False, True])
    shape_path = get_path_for_shape('aguascalientes_jm')
    assert shape_path == '/data/aguascalientes_jm.shp'


def test_get_path_for_local_shape(mocker):
    mocker.patch.object(
        Path, 'exists', side_effect=[True, False])
    shape_path = get_path_for_shape('aguascalientes_jm')
    assert shape_path == os.path.abspath(os.path.join('docker/production/django/data/aguascalientes_jm.shp'))


def test_no_path_shape():
    with pytest.raises(FileNotFoundError):
        get_path_for_shape('nonexistentshape')
