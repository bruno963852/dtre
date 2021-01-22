from typing import Tuple

from PIL.ImageEnhance import Color

from src.image.play_token_image_processor import TokenImageProcessor, DEFAULT_TOKEN_FRAME_FILE

_ATTR_POSITION = 'position'
_ATTR_IMAGE_URL = 'image_url'
_ATTR_FRAME_COLOR = 'frame_color'
_ATTR_FRAME_SECONDARY_COLOR = 'frame_secondary_color'
_ATTR_SIZE_Y = 'size_y'
_ATTR_SIZE_X = 'size_x'


class Token(TokenImageProcessor):
    def __init__(self, name, position: Tuple[int, int], image_url: str, square_size: int, server_id: str,
                 channel_id: str, size: Tuple[int, int], frame_color: str, frame_secondary_color: str):
        super().__init__(name, position, image_url, square_size, server_id, channel_id, size, frame_color,
                         frame_secondary_color)

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @property
    def url(self) -> str:
        return self._image_url

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._position = value

    @property
    def frame_color(self) -> str:
        return self._frame_color

    @frame_color.setter
    def frame_color(self, value):
        self._frame_color = value

    @property
    def dict(self) -> dict:
        return {
            _ATTR_POSITION: self.position,
            _ATTR_IMAGE_URL: self._image_url,
            _ATTR_FRAME_COLOR: self._frame_color,
            _ATTR_FRAME_SECONDARY_COLOR: self._frame_secondary_color,
            _ATTR_SIZE_X: self._size[0],
            _ATTR_SIZE_Y: self._size[1]
        }

    def increment_position(self, x: int = 0, y: int = 0):
        self._position = (self._position[0] + x, self.position[1] + y)

    @staticmethod
    def from_dict(dict_: dict, name: str, square_size: int, server_id: str, channel_id: str):
        return Token(
            server_id=server_id,
            channel_id=channel_id,
            square_size=square_size,
            position=tuple(dict_[_ATTR_POSITION]),
            image_url=dict_[_ATTR_IMAGE_URL],
            frame_color=dict_[_ATTR_FRAME_COLOR],
            frame_secondary_color=dict_[_ATTR_FRAME_SECONDARY_COLOR],
            size=(dict_[_ATTR_SIZE_X], dict_[_ATTR_SIZE_Y])
        )


if __name__ == '__main__':
    tk = Token((1, 1), 'https://image.freepik.com/free-vector/chicken-fighter_1975-119.jpg', 64, '0000', '0000',
               (2, 2), 'files/default_token_frame.png')
    tk._get_frame().save('test.png')
