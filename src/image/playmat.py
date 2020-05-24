from io import BytesIO
from typing import Tuple, Optional

from src.image.playmat_image_processor import PlaymatImageProcessor


class Playmat(PlaymatImageProcessor):
    def __init__(self, server_id: str, image_url: Optional[str] = None, offset_pixels: Tuple[int, int] = (0, 0),
                 square_size: int = 64):
        super().__init__(server_id, image_url, offset_pixels, square_size)
