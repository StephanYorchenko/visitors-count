from io import BytesIO

from PIL import Image, ImageDraw


class ImageGenerator:
    def make_image(self, stat=None):
        return self._text_on_img(text=stat)

    @staticmethod
    def _text_on_img(text="", size=12, color=(255, 255, 0), bg="red"):
        image = Image.new(
            mode="RGB", size=(int(size / 2) * len(text), size + 50), color=bg
        )
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, fill=color)
        img_io = BytesIO()
        image.save(img_io, "JPEG", quality=70)
        img_io.seek(0)
        return img_io
