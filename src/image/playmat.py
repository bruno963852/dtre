from io import BytesIO
from typing import Tuple, Optional

from src.image.playmat_image_processor import PlaymatImageProcessor

_ATTR_IMAGE_URL = 'image_url'
_ATTR_OFFSET = 'offset'
_ATTR_SQUARE_SIZE = 'square_size'


class Playmat(PlaymatImageProcessor):
    def __init__(self, server_id: str, image_url: Optional[str] = None, offset_pixels: Tuple[int, int] = (0, 0),
                 square_size: int = 64):
        super().__init__(server_id, image_url, offset_pixels, square_size)

    @property
    def dict(self) -> dict:
        return {
            _ATTR_IMAGE_URL: self.image_url,
            _ATTR_OFFSET: self._offset_pixels,
            _ATTR_SQUARE_SIZE: self.square_size
        }

    @staticmethod
    def from_dict(dict_: dict, server_id: str):
        return Playmat(
            server_id=server_id,
            image_url=dict_[_ATTR_IMAGE_URL],
            offset_pixels=tuple(dict_[_ATTR_OFFSET]),
            square_size=dict_[_ATTR_SQUARE_SIZE]
        )
