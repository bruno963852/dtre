from typing import Tuple
from play_mat.play_token_image_processor import TokenImageProcessor


class Token(TokenImageProcessor):
    def __init__(self, name: str, position: Tuple[int, int], url: str,
                 frame_url: str = TokenImageProcessor.DEFAULT_TOKEN_FRAME_FILE):
        super().__init__(name, position, url, frame_url)

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._position = value

    @property
    def frame_url(self) -> str:
        return self._frame_url

    @frame_url.setter
    def frame_url(self, value):
        self._frame_url = value

    def increment_position(self, x: int = 0, y: int = 0):
        self._position = (self._position[0] + x, self.position[1] + y)


