
import os

import pytest

from mock import patch

from rio_toa import toa_utils
from remotepixel import l8_ovr

landsat_scene_c1 = 'LC08_L1TP_016037_20170813_20170814_01_RT'
landsat_bucket = os.path.join(os.path.dirname(__file__), 'fixtures', 'landsat-pds')

landsat_path = os.path.join(landsat_bucket, 'c1', 'L8', '016', '037', landsat_scene_c1, landsat_scene_c1)
with open('{}_MTL.txt'.format(landsat_path), 'r') as f:
    landsat_meta = toa_utils._parse_mtl_txt(f.read())


def test_worker_valid():
    """
    Should work as expected (read data, proccess to TOA and rescale to int)
    """

    assert l8_ovr.worker(4, landsat_path, landsat_meta.get('L1_METADATA_FILE'), 512, False).shape == (512, 512)


def test_worker_validNdvi():
    """
    Should work as expected (read data and proccess to TOA)
    """

    assert l8_ovr.worker(4, landsat_path, landsat_meta.get('L1_METADATA_FILE'), 512, True).shape == (512, 512)


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_valid(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read r,g,b bands and create JPEG image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create(landsat_scene_c1, bands=[4, 3, 2])


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_validPNG(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read r,g,b bands and create PNG image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create(landsat_scene_c1, bands=[4, 3, 2], img_format='png')


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_validSmall(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read bands and create 128x128 image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create(landsat_scene_c1, ovrSize=128)


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_invalidFormat(landsat_get_mtl, monkeypatch):
    """
    Should raise invalid format
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    with pytest.raises(UserWarning):
        l8_ovr.create(landsat_scene_c1, img_format='tif')


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_ndvi_valid(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read nir and red bands and create JPEG image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create_ndvi(landsat_scene_c1)


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_ndvi_validPNG(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read nir and red bands and create PNG image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create_ndvi(landsat_scene_c1, img_format='png')


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_ndvi_validSmall(landsat_get_mtl, monkeypatch):
    """
    Should work as expected (read bands and create 128x128 image)
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    assert l8_ovr.create_ndvi(landsat_scene_c1, ovrSize=128)


@patch('remotepixel.utils.landsat_get_mtl')
def test_create_ndvi_invalidFormat(landsat_get_mtl, monkeypatch):
    """
    Should raise invalid format
    """

    monkeypatch.setattr(l8_ovr, 'LANDSAT_BUCKET', landsat_bucket)
    landsat_get_mtl.return_value = landsat_meta

    with pytest.raises(UserWarning):
        l8_ovr.create_ndvi(landsat_scene_c1, img_format='tif')
