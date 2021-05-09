# -*- coding: utf-8 -*-
# pylint: disable=c-extension-no-member,expression-not-assigned,line-too-long,logging-fstring-interpolation
"""Juggle with pixels."""
import pathlib

from PIL import Image
from pixelmatch.contrib import PIL

from pixelmatch import pixelmatch
import png

OPTIONS = {"threshold": 0.05}


def shape_of_png(path):
    """MVP like initial shape reader for PNG from path."""
    try:
        with path.open("rb") as handle:
            a_png = png.Reader(file=handle)
            width, height, _, info = a_png.read()  # Ignore the rows iterator
            return True, width, height, info
    except Exception as err:  # pylint: disable=too-broad-exception
        return False, None, None, {"error": str(err).replace("\n", "$NL$")}


def read_img(path):
    """HACK A DID ACK"""
    return Image.open(path)


def pil_to_flatten_data(img):
    """
    Convert data from [(R1, G1, B1, A1), (R2, G2, B2, A2)] to [R1, G1, B1, A1, R2, G2, B2, A2]
    """
    return [x for p in img.convert("RGBA").getdata() for x in p]


def diff_img(ref, obs, sub):
    """Read from ref and obs, calculate the subtraction, output at sub and return the mismatch pixel count."""
    img_a = Image.open(ref)
    img_b = Image.open(obs)
    width, height = img_a.size
    img_diff = Image.new("RGBA", (width, height))
    mismatch = PIL.pixelmatch(img_a, img_b, **OPTIONS)

    img_diff.save(sub)
    return mismatch
