from PIL import Image
from io import BytesIO
import asyncio
from datetime import datetime

async def create_gif(frames: list) -> bytes:
    pil_frames = [Image.open(BytesIO(image)) for image in frames]
    frame_one = pil_frames[0]
    image_bytes = BytesIO()
    frame_one.save(image_bytes, format="GIF", append_images=pil_frames, save_all=True, duration=200, loop=0)

    return image_bytes.getbuffer()

async def write_gif(frames: list, name: str) -> bytes:
    try:
        image_bytes = await create_gif(frames)
        filename = f'{name}.gif'
        with open(filename, 'wb') as f:
            f.write(image_bytes)
        print(f'wrote {filename}')
    except Exception as e:
        raise e

    return image_bytes
    