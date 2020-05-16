import math
import shutil
from io import BytesIO
from os import makedirs, path
from typing import Tuple, Dict

import requests
from PIL import Image, ImageFont, ImageDraw

from play_mat.play_token import Token
from play_mat.exceptions import FrameWithoutAlphaException


class PlayMatImageProcessor:
    IMAGE_CACHE_DIR = 'cache/'
    BACKGROUND_FILENAME = '/background.png'
    BACKGROUND_GRIDDED_FILENAME = '/background_gridded.png'
    FRAME_FILE_SUFFIX = '_frame.png'

    def __init__(self, server_id: str, url: str, offset: Tuple[int, int], square_size: int):
        self._server_id = server_id
        self._url = url
        self._offset = offset
        self._square_size = square_size
        self._tokens: Dict[str, Token] = {}
        self._remove_cache()
        self._map_size = self._get_image_size()
        self._box = (0, 0) + self._map_size
        self._text_color = (0xff, 0xa5, 0x00, 0xff)
        self._changed_frame = False

    def _remove_cache(self):
        cache_image_path = self.IMAGE_CACHE_DIR + self._server_id + '/'
        if path.exists(cache_image_path):
            shutil.rmtree(cache_image_path)
        makedirs(cache_image_path)

    def _get_background(self, overwrite=False) -> Image:
        cache_image_path = self.IMAGE_CACHE_DIR + self._server_id + self.BACKGROUND_FILENAME
        if not overwrite and path.exists(cache_image_path):
            return Image.open(cache_image_path)
        response = requests.get(self._url)
        img = Image.open(BytesIO(response.content))
        if img.mode != 'RGBA':
            img = img.convert(mode='RGBA')
        img.save(cache_image_path, quality=85, optimize=True)
        return img

    def _get_background_gridded(self) -> Image:
        cache_image_path = self.IMAGE_CACHE_DIR + self._server_id + self.BACKGROUND_GRIDDED_FILENAME
        if path.exists(cache_image_path):
            return Image.open(cache_image_path)
        img = self._get_background()

        if img.mode != 'RGBA':
            img = img.convert(mode='RGBA')

        size_x, size_y = self._map_size
        offset_x, offset_y = self._offset

        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype('play_mat/FreeMono.ttf', int(self._square_size / 2))

        for x in range(size_x):
            for y in range(size_y):
                top_left_corner = (offset_x + (x * self._square_size), offset_x + (y * self._square_size))
                bottom_right_corner = (top_left_corner[0] + self._square_size, top_left_corner[1] + self._square_size)
                if y == 0:
                    draw.text(
                        (
                            top_left_corner[0] + int(self._square_size / 4),
                            offset_x + int(self._square_size / 4)
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

    def _get_frame(self, token: Token, overwrite: bool = False) -> Image:
        frame_image_path = self.IMAGE_CACHE_DIR + self._server_id + token.name + self.FRAME_FILE_SUFFIX
        if not overwrite and path.exists(frame_image_path):
            return Image.open(frame_image_path)
        if token.frame_url.startswith('http'):
            response = requests.get(token.frame_url)
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGBA':
                img = img.convert(mode='RGBA')
            return img
        else:
            img = Image.open(Token.DEFAULT_TOKEN_FRAME_FILE)
            img = img.resize((self._square_size, self._square_size), resample=Image.LANCZOS, reducing_gap=3.0)
            img.save(frame_image_path, quality=85, optimize=True)
            return img

    def _get_token_image(self, token: Token) -> Image:
        cache_token_path = self.IMAGE_CACHE_DIR + self._server_id + '/' + token.name + '.png'
        if path.exists(cache_token_path) and not self._changed_frame:
            return Image.open(cache_token_path)
        self._changed_frame = False
        response = requests.get(token.url)
        source = Image.open(BytesIO(response.content))
        source = source.convert(mode='RGBA')
        source = source.resize((self._square_size, self._square_size), resample=Image.LANCZOS, reducing_gap=3.0)
        background = Image.new(source.mode, (self._square_size, self._square_size), (0, 0, 0, 0))
        mask = Image.new('L', (self._square_size, self._square_size), 0)
        draw = ImageDraw.Draw(mask)
        offset = math.ceil(2 * self._square_size / 45)
        draw.ellipse((offset, offset, self._square_size - offset, self._square_size - offset), fill=255)
        img = Image.composite(source, background, mask)
        frame = self._get_frame(token)
        img.alpha_composite(frame)
        img.save(cache_token_path, quality=85, optimize=True)
        return img

    def _get_image_size(self):
        img = self._get_background()
        size_x = int((img.size[0] - self._offset[0]) / self._square_size)
        size_y = int((img.size[1] - self._offset[1]) / self._square_size)
        return size_x, size_y

    def _process(self) -> BytesIO:
        img = self._get_background_gridded()

        size_x, size_y = self._map_size

        for x in range(size_x):
            for y in range(size_y):
                for tk in self._tokens.values():
                    if tk.position == (x, y):
                        offset_x, offset_y = self._offset
                        img.alpha_composite(
                            self._get_token_image(tk),
                            (offset_x + (x * self._square_size), offset_y + (y * self._square_size))
                        )
        playmat = BytesIO()
        img.save(playmat, quality=85, optimize=True, format='PNG')
        playmat.seek(0)
        return playmat
