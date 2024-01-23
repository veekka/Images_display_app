from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from collections import Counter
from colormap import rgb2hex
from django.urls import reverse


class Images(models.Model):
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name="Image")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.CharField(max_length=255, verbose_name="Description")
    image_size = models.CharField(max_length=255, verbose_name="Image size")
    dominant_color = models.CharField(max_length=255, verbose_name="Dominant color")
    average_color = models.CharField(max_length=255, verbose_name="Average color")
    image_palette = models.CharField(max_length=255, verbose_name="Image palette")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time update")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author of image")

    def save(self, *args, **kwargs):
        self.image_size = self.get_image_size(self.photo)
        self.dom_color_rgb = self.get_dominant_color(self.photo)
        self.dominant_color = rgb2hex(self.dom_color_rgb[0], self.dom_color_rgb[1], self.dom_color_rgb[2])
        self.av_color_rgb = self.get_average_color(self.photo)
        self.average_color = rgb2hex(self.av_color_rgb[0], self.av_color_rgb[1], self.av_color_rgb[2])
        self.im_palette_rgb = self.get_image_palette(self.photo)
        self.list_im_palette = []
        for color in self.im_palette_rgb:
            self.list_im_palette.append(rgb2hex(color[0], color[1], color[2]))
        self.image_palette = self.list_im_palette
        super(Images, self).save(*args, **kwargs)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('image_edit', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['id']

    def get_dominant_color(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        small_image = image.resize((width, height))

        pixels = list(small_image.getdata())

        color_counts = Counter(pixels)
        color = color_counts.most_common(1)[0][0]
        return color

    def get_image_size(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        return width, height

    def get_average_color(self, image_path):
        # Open the image using Pillow
        image = Image.open(image_path)
        width, height = image.size
        small_image = image.resize((width, height))

        pixels = list(small_image.getdata())

        total_pixels = len(pixels)
        average_red = sum(pixel[0] for pixel in pixels) // total_pixels
        average_green = sum(pixel[1] for pixel in pixels) // total_pixels
        average_blue = sum(pixel[2] for pixel in pixels) // total_pixels

        return average_red, average_green, average_blue

    def get_image_palette(self, image_path):
        image = Image.open(image_path)

        palette = image.convert('P', palette=Image.ADAPTIVE, colors=5).getpalette()

        rgb_palette = []
        for i in range(0, len(palette), 3):
            rgb_palette.append((palette[i], palette[i + 1], palette[i + 2]))

        return rgb_palette
