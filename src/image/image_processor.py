import shutil
from abc import ABC, abstractmethod
from io import BytesIO
from os import path, makedirs

from PIL import Image

IMAGE_CACHE_DIR = '../cache/'


class ImageProcessor(ABC):
    def __init__(self, server_id: str, channel_id: str, image_url: str, square_size: int):
        """
        Abstract class with some common fields and methods to the other imageprocessor classes
        """
        self._server_id = server_id
        self._image_url = image_url
        self._square_size = square_size
        self._channel_id = channel_id

    @property
    def _files_dir(self):
        return f'{IMAGE_CACHE_DIR}{self._server_id}/{self._channel_id}/'

    @abstractmethod
    def get_image(self, overwrite=False) -> Image:
        """
        Gets the processed image
        @rtype: Image
        @return: the processed image
        """
        raise NotImplementedError

    def get_image_bytes(self, overwrite=False) -> BytesIO:
        """
        Gets the processed image in BytesIO format
        @rtype: BytesIO
        @return: the processed image in BytesIO format
        """
        img = self.get_image(overwrite)
        image_bytes = BytesIO()
        img.save(image_bytes, quality=85, optimize=True, format='PNG')
        image_bytes.seek(0)
        return image_bytes

    def erase_cache(self):
        """
        Erases the cache of saved images for this server
        """
        cache_image_path = self._files_dir
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
