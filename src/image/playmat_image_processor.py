import shutil
from abc import ABC
from io import BytesIO
from os import makedirs, path
from typing import Tuple, Dict, Optional, List

import requests
from PIL import Image, ImageFont, ImageDraw, ImageColor

from src.char import Character
from src.image.image_processor import ImageProcessor, IMAGE_CACHE_DIR
from src.image.player_token import Token

DEFAULT_MAP_FILENAME = 'image/files/default_dungeon.png'
BACKGROUND_FILENAME = 'background.png'
BACKGROUND_GRIDDED_FILENAME = 'background_gridded.png'

MODE_RGBA = 'RGBA'


class PlaymatImageProcessor(ImageProcessor, ABC):

    def __init__(self, server_id: str, channel_id, image_url: str, offset_pixels: Tuple[int, int], square_size: int,
                 zoom=1.0, crop_box: Tuple[int, int, int, int] = None,
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 movement_color: Tuple[int, int, int] = (0, 255, 255)):
        super().__init__(server_id, channel_id, image_url, square_size)
        self._offset_pixels = offset_pixels
        self.erase_cache()
        self._map_size = self._get_image_size()
        self._crop_box = (0, 0) + self._map_size if crop_box is None else crop_box
        self._zoom = zoom
        self._text_color = text_color
        self._movement_color = movement_color

    @property
    def size(self):
        return self._map_size

    @property
    def offset(self):
        return self._offset_pixels

    def _get_background(self, overwrite=False) -> Image:
        if self._image_url is None:
            return Image.open(DEFAULT_MAP_FILENAME)
        cache_image_path = self._files_dir + BACKGROUND_FILENAME
        if not overwrite and path.exists(cache_image_path):
            return Image.open(cache_image_path)
        response = requests.get(self._image_url)
        img = Image.open(BytesIO(response.content))
        if img.mode != MODE_RGBA:
            img = img.convert(mode=MODE_RGBA)
        img.save(cache_image_path, quality=85, optimize=True)
        return img

    def get_image(self, overwrite=False) -> Image:
        cache_image_path = self._files_dir + BACKGROUND_GRIDDED_FILENAME
        if path.exists(cache_image_path):
            return Image.open(cache_image_path)
        img = self._get_background(overwrite)

        if img.mode != MODE_RGBA:
            img = img.convert(mode=MODE_RGBA)

        size_x, size_y = self._map_size
        offset_x, offset_y = self._offset_pixels

        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype('image/files/FreeMonoBold.ttf', int(self._square_size / 2))

        for x in range(size_x):
            for y in range(size_y):
                top_left_corner = (offset_x + (x * self._square_size), offset_y + (y * self._square_size))
                bottom_right_corner = (top_left_corner[0] + self._square_size, top_left_corner[1] + self._square_size)
                if y == 0:
                    draw.text(
                        (
                            top_left_corner[0] + int(self._square_size / 4),
                            offset_y + int(self._square_size / 4)
                        ),
                        str(x),
                        fill=self._text_color,
                        font=font
                    )
                elif x == 0:
                    draw.text(
                        (
                            offset_x + int(self._square_size / 4),
                            top_left_corner[1] + int(self._square_size / 4)
                        ),
                        str(y),
                        fill=self._text_color,
                        font=font
                    )
                draw.rectangle((top_left_corner, bottom_right_corner), outline=(0, 0, 0, 255))

        img.save(cache_image_path, quality=85, optimize=True)
        return img

    def _get_image_size(self):
        img = self._get_background()
        size_x = int((img.size[0] - self._offset_pixels[0]) / self._square_size)
        size_y = int((img.size[1] - self._offset_pixels[1]) / self._square_size)
        return size_x, size_y

    def get_full_map(self, characters: Dict[str, Character], movement: List[Tuple[int, int]] = None, overwrite=False):
        img = self.get_image(overwrite)

        size_x, size_y = self._map_size
        offset_x, offset_y = self._offset_pixels

        for x in range(size_x):
            for y in range(size_y):
                pos_x = offset_x + (x * self._square_size)
                pos_y = offset_y + (y * self._square_size)
                if movement is not None:
                    for mov in movement:
                        if mov == (x, y):
                            draw = ImageDraw.Draw(img)
                            size = self._square_size / 3
                            draw.ellipse(
                                (
                                    (pos_x + size, pos_y + size),
                                    (pos_x + self._square_size - size, pos_y + self._square_size - size)
                                ),
                                fill=self._movement_color
                            )
                for char in characters.values():
                    if char.token.position == (x, y):
                        img.alpha_composite(
                            char.token.get_image(),
                            (pos_x, pos_y)
                        )
        image_bytes = BytesIO()
        img.save(image_bytes, quality=85, optimize=True, format='PNG')
        image_bytes.seek(0)
        return image_bytes

    def set_text_color(self, color: str):
        imgcolor = ImageColor.getrgb(color)
        self._text_color = imgcolor

    def set_movement_color(self, color: str):
        imgcolor = ImageColor.getrgb(color)
        self._movement_color = imgcolor
