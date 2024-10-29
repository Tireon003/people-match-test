from fastapi import UploadFile
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

from app.exceptions import BadImageProvidedError


def save_image_with_watermark(
        image_file: UploadFile,
        watermark_label: str = "some_watermark",
        upload_folder: str = "member_avatars",
) -> uuid.UUID:
    image_uuid = uuid.uuid4()
    unique_filename = f"{image_uuid}.jpeg"
    file_path = os.path.join(upload_folder, unique_filename)
    os.makedirs(upload_folder, exist_ok=True)
    try:
        image = Image.open(image_file.file)
        watermark_image = image.copy()
        draw = ImageDraw.Draw(watermark_image)
        font = ImageFont.load_default()
        text_bbox = draw.textbbox(
            xy=(0, 0),
            text=watermark_label,
            font=font
        )
        text_width, text_height = (
            text_bbox[2] - text_bbox[0],
            text_bbox[3] - text_bbox[1],
        )

        position = (
            watermark_image.width - text_width - 10,
            watermark_image.height - text_height - 10,
        )
        draw.text(
            xy=position,
            text=watermark_label,
            font=font,
            fill=(255, 255, 255, 128)
        )

        watermark_image = watermark_image.convert("RGB")
        watermark_image.save(file_path, format="JPEG")
        return image_uuid

    except Exception:
        raise BadImageProvidedError()
