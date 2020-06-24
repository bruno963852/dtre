import math
from abc import ABC
from io import BytesIO
from typing import Tuple

import requests
from PIL import Image, ImageDraw, ImageFont, ImageColor
from os import path

from src.image.image_processor import IMAGE_CACHE_DIR, ImageProcessor

DEFAULT_TOKEN_FRAME_FILE = 'image/files/default_token_frame.png'
FRAME_FILE_SUFFIX = '_frame.png'


class TokenImageProcessor(ImageProcessor, ABC):

    def __init__(self, name: str, position: Tuple[int, int], image_url: str, square_size: int, server_id: str,
                 channel_id: str, size: Tuple[int, int], frame_color: str, frame_secondary_color: str):
        super().__init__(server_id, channel_id, image_url, square_size)
        self._position = position
        self._name = name
        self._image_url = image_url
        self._server_id = server_id
        self._square_size = square_size
        self._frame_color = frame_color
        self._frame_secondary_color = frame_secondary_color
        self._size = size
        self._changed_frame = False

    def _get_frame(self) -> Image:
        size_x, size_y = size = self._square_size * self._size[0], self._square_size * self._size[1]
        image = Image.new('RGBA', size)
        draw = ImageDraw.Draw(image)
        thickness = math.ceil(size_x / 10)
        outer_border_thickness = thickness/4
        draw.ellipse((0, 0, size_x, size_y),
                     None,
                     ImageColor.getrgb(self._frame_color),
                     thickness)
        draw.ellipse((0, 0, size_x, size_y),
                     None,
                     ImageColor.getrgb(self._frame_secondary_color),
                     int(outer_border_thickness))
        return image

    def _get_token_image(self, overwrite=False) -> Image:
        cache_token_path = self._files_dir + self._name + '.png'
        if path.exists(cache_token_path) and not overwrite:
            return Image.open(cache_token_path)
        size = (self._square_size * self._size[0], self._square_size * self._size[1])
        response = requests.get(self._image_url)
        source = Image.open(BytesIO(response.content))
        source = source.convert(mode='RGBA')
        source = source.resize(size, resample=Image.LANCZOS, reducing_gap=3.0)
        background = Image.new(source.mode, size, (0, 0, 0, 0))
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        offset = math.ceil(2 * self._square_size / 45)
        draw.ellipse((offset, offset, size[0] - offset, size[1] - offset), fill=255)
        img = Image.composite(source, background, mask)
        frame = self._get_frame()
        img.alpha_composite(frame)
        img.save(cache_token_path, quality=85, optimize=True)
        return img

    def get_image(self, overwrite=False) -> Image:
        return self._get_token_image(overwrite)
