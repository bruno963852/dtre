from io import BytesIO
from typing import Tuple, Optional

from src.image.playmat_image_processor import PlaymatImageProcessor

_ATTR_IMAGE_URL = 'image_url'
_ATTR_OFFSET = 'offset'
_ATTR_SQUARE_SIZE = 'square_size'
_ATTR_CROP_BOX = 'crop_box'
_ATTR_ZOOM = 'zoom'
_ATTR_TEXT_COLOR = 'text_color'
_ATTR_MOVEMENT_COLOR = 'movement_color'


class Playmat(PlaymatImageProcessor):
    def __init__(self, server_id: str, channel_id: str, image_url: Optional[str] = None,
                 offset_pixels: Tuple[int, int] = (0, 0), square_size: int = 64,
                 zoom=1.0, crop_box: Tuple[int, int, int, int] = None,
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 movement_color: Tuple[int, int, int] = (0, 255, 255)
                 ):
        super().__init__(server_id, channel_id, image_url, offset_pixels, square_size, zoom, crop_box, text_color,
                         movement_color)

    @property
    def dict(self) -> dict:
        return {
            _ATTR_IMAGE_URL: self.image_url,
            _ATTR_OFFSET: self._offset_pixels,
            _ATTR_SQUARE_SIZE: self.square_size,
            _ATTR_CROP_BOX: self._crop_box,
            _ATTR_ZOOM: self._zoom,
            _ATTR_TEXT_COLOR: self._text_color,
            _ATTR_MOVEMENT_COLOR: self._movement_color,
        }

    @staticmethod
    def from_dict(dict_: dict, server_id: str, channel_id: str):
        return Playmat(
            server_id=server_id,
            channel_id=channel_id,
            image_url=dict_[_ATTR_IMAGE_URL],
            offset_pixels=tuple(dict_[_ATTR_OFFSET]),
            square_size=dict_[_ATTR_SQUARE_SIZE],
            crop_box=dict_[_ATTR_CROP_BOX],
            zoom=dict_[_ATTR_TEXT_COLOR],
            movement_color=dict_[_ATTR_MOVEMENT_COLOR]
        )
