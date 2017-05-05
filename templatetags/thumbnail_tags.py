import os
from django import template
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer

register = template.Library()

THUMBNAILER_EXTENSIONS_FILTER = getattr(settings, "THUMBNAIL_EXTENSIONS_FILTER", ['.gif'])

@register.filter
def smart_thumbnail(value, args):
    """
    creates thumbnails on every image except the ones defined in THUMBNAILER_EXTENSIONS_FILTER
    basically I was tired to do:
    {% if '.gif' in image.original_filename %}{{ image.url }}{% else %}{% thumbnail image 200x200 upscale crop %}{% endif %}
    so instead I'm doing {{ background.image|smart_thumbnail:"200x200 upscale crop" }}
    TODO:
      - Better exception handling
    """
    thumbnailer_extensions_filter = getattr(settings, "THUMBNAIL EXTENSIONS FILTER", ['.gif'])

    argument_list = [arg.strip() for arg in args.split(' ')]
    width = None
    height = None
    crop = False
    upscale = False
    
    try:
		image_extension = os.path.splitext(value.original_filename)[1].lower()
        if image_extension in thumbnailer_extensions_filter:
            return value.url
	except Exception as e:
        raise Exception(e)

    try:
        for arg in argument_list:
            if 'x' in arg.lower():
                size_list = [size.strip() for size in arg.split('x')]
                if len(size_list) != 2 or "px" in args:
                    raise Exception('%s is not a correct format. Use widthxheight. Example: 600x300' % (args))
                width = int(size_list[0])
                height = int(size_list[1])
        if not width and not height:
            raise Exception("Please provide a size value in the format widthxheight")
    except Exception as e:
        raise Exception(e)

    try:
        for arg in argument_list:
            if arg == "crop":
                crop = True

            if arg == "upscale":
                upscale = True

        thumbnailer_options = {'size': (width, height), 'crop': crop, 'upscale': upscale}

        if crop:
            thumbnailer_options["subject_location"] = value.subject_location

        thumbnail_url = get_thumbnailer(value).get_thumbnail(thumbnailer_options).url

        return thumbnail_url

    except Exception as e:
        raise Exception(e)

    return ''
