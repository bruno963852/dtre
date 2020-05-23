import shutil
from abc import ABC, abstractmethod
from io import BytesIO
from os import path, makedirs

from PIL import Image

IMAGE_CACHE_DIR = '../cache/'


class ImageProcessor(ABC):
    def __init__(self, server_id: str, image_url: str, square_size: int):
        self._server_id = server_id
        self._image_url = image_url
        self._square_size = square_size

    @abstractmethod
    def get_image(self) -> Image:
        raise NotImplementedError

    def get_image_bytes(self) -> BytesIO:
        img = self.get_image()
        image_bytes = BytesIO()
        img.save(image_bytes, quality=85, optimize=True, format='PNG')
        image_bytes.seek(0)
        return image_bytes

    def erase_cache(self):
        cache_image_path = IMAGE_CACHE_DIR + self._server_id + '/'
        if path.exists(cache_image_path):
            shutil.rmtree(cache_image_path)
        makedirs(cache_image_path)

    @property
    def server_id(self) -> str:
        return self._server_id

    @property
    def image_url(self) -> str:
        return self._image_url

    @image_url.setter
    def image_url(self, value: str):
        self.image_url = value

    @property
    def square_size(self) -> int:
        return self._square_size

    @square_size.setter
    def square_size(self, value: int):
        self._square_size = value