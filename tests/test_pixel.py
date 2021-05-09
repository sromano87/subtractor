# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import pathlib

import pytest  # type: ignore

from subtractor.pixel import shape_of_png

FIXTURE_ROOT = pathlib.Path("tests", "fixtures")
DEFAULT_FILE_NAME = "empty.png"
SINGLE_FILE_FOLDER = pathlib.Path(FIXTURE_ROOT, "single_file")
SINGLE_FILE_PATH_EMPTY_PNG = pathlib.Path(SINGLE_FILE_FOLDER, DEFAULT_FILE_NAME)

REF_OBS_ROOT = pathlib.Path(FIXTURE_ROOT, "ref_obs")
REF_CHILD_FOLDER = pathlib.Path(REF_OBS_ROOT, "ref")
OBS_CHILD_FOLDER = pathlib.Path(REF_OBS_ROOT, "obs")
RGB_RED_NAME = "ff0000_2x2.png"
REF_CHILD_RGB_RED_PNG = pathlib.Path(REF_CHILD_FOLDER, RGB_RED_NAME)


def test_shape_of_png_ok_test_single_fixture_rgb_file():
    ok, width, height, info = shape_of_png(REF_CHILD_RGB_RED_PNG)
    assert ok is True
    assert width == 2 and height == 2
    facts = {
        'alpha': False,
        'background': (1,),
        'bitdepth': 1,
        'gamma': 0.45455,
        'greyscale': False,
        'interlace': 0,
        'palette': [(255, 0, 0), (255, 255, 255)],
        'planes': 1,
        'size': (2, 2)
    }
    assert info == facts


def test_shape_of_png_nok_test_single_fixture_non_png_file():
    ok, width, height, info = shape_of_png(SINGLE_FILE_PATH_EMPTY_PNG)
    assert ok is False
    assert width is None and height is None
    assert info["error"].lower() == "formaterror: png file has invalid signature."


def test_shape_of_png_nok_non_existing_file():
    file_not_there = pathlib.Path("no", "file", "here")
    assert not file_not_there.exists(), f"WARNING: The path {file_not_there} SHOULD not exist, but does."
    ok, width, height, info = shape_of_png(file_not_there)
    assert ok is False
    assert width is None and height is None
    assert info["error"].lower() == f"[errno 2] no such file or directory: '{str(file_not_there).lower()}'"
