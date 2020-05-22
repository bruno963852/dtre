import math
from io import BytesIO
from typing import Tuple

import requests
from PIL import Image, ImageDraw, ImageFont
from os import path, makedirs


class TokenImageProcessor:
    IMAGE_CACHE_DIR = 'cache/'
    DEFAULT_TOKEN_FRAME_FILE = 'play_mat/default_token_frame.png'
    FRAME_FILE_SUFFIX = '_frame.png'

    def __init__(self, name: str, position: Tuple[int, int], url: str, square_size: int, server_id: str,
                 frame_url: str = DEFAULT_TOKEN_FRAME_FILE):
        self._position = position
        self._name = name
        self._url = url
        self._server_id = server_id
        self._square_size = square_size
        self._frame_url = frame_url
        self._changed_frame = False

    def set_frame(self, url):
        self._get_frame(True)
        self.get_token_image(True)

    def _get_frame(self, overwrite: bool = False) -> Image:
        frame_image_path = self.IMAGE_CACHE_DIR + self._server_id + self._name + self.FRAME_FILE_SUFFIX
        if not overwrite and path.exists(frame_image_path):
            return Image.open(frame_image_path)
        if self._frame_url.startswith('http'):
            response = requests.get(self._frame_url)
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGBA':
                img = img.convert(mode='RGBA')
            return img
        else:
            img = Image.open(self.DEFAULT_TOKEN_FRAME_FILE)
            img = img.resize((self._square_size, self._square_size), resample=Image.LANCZOS, reducing_gap=3.0)
            img.save(frame_image_path, quality=85, optimize=True)
            return img

    def get_token_image(self, overwrite=False) -> Image:
        cache_token_path = self.IMAGE_CACHE_DIR + self._server_id + '/' + self._name + '.png'
        if path.exists(cache_token_path) and not overwrite:
            return Image.open(cache_token_path)
        response = requests.get(self._url)
        source = Image.open(BytesIO(response.content))
        source = source.convert(mode='RGBA')
        source = source.resize((self._square_size, self._square_size), resample=Image.LANCZOS, reducing_gap=3.0)
        background = Image.new(source.mode, (self._square_size, self._square_size), (0, 0, 0, 0))
        mask = Image.new('L', (self._square_size, self._square_size), 0)
        draw = ImageDraw.Draw(mask)
        offset = math.ceil(2 * self._square_size / 45)
        draw.ellipse((offset, offset, self._square_size - offset, self._square_size - offset), fill=255)
        img = Image.composite(source, background, mask)
        frame = self._get_frame()
        img.alpha_composite(frame)
        img.save(cache_token_path, quality=85, optimize=True)
        return img
