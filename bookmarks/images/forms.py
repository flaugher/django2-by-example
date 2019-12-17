from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """Form to submit new images.

    The user will provide the URL of the image, a title, and optional description. Our application will download the image and create a new Image object in the database.
    """
    class Meta:
        # Create form from the Image model.
        model = Image
        # Only display these fields from that model.
        fields = ('title', 'url', 'description')
        # Users will not enter the image URL directly in the form. Instead, we will provide them with a JavaScript tool to choose an image from an external site, and our form will receive its URL as a parameter. We override the default widget of the url field to use a HiddenInput widget. This widget is rendered as an HTML input element with a type="hidden" attribute. We use this widget because we don't want this field to be visible to users.
        widgets = {
            'url': forms.HiddenInput,
        }

        def clean_url(self):
            """Verify that the provided URL is valid.

            We will check that the filename ends with a .jpg or .jpeg extension to only allow JPEG files.
            """
            url = self.cleaned_data['url']
            #valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in ['jpg', 'jpeg']:
                raise forms.ValidationError('The given URL does not ' \
                'match valid image extensions.')
            return url

        def save(self, force_insert=False, force_update=False, commit=True):
            """Override save method.

            We will override the save() method of our form in order to retrieve the given image and save it.
            commit=True means, save the image to the database after fetching it.
            """
            # Create a new image instance to work with.
            image = super(ImageCreateForm, self).save(commit=False)

            image_url = self.cleaned_data['url']

            # Image name is slugified image title combined with the original image file extension.
            # rsplit params:
            # . - Divide string at the "."
            # 1 - Just do one split
            # [1] - Take the first element, which is the extension (0 would be file name)
            image_name = '{}.{}'.format(slugify(image.title),
                image_url.rsplit('.', 1)[1].lower())

            # Download the image from the given URL.  Using ContentFile causes the image file to be saved to our media directory.
            response = request.urlopen(image_url)
            image.image.save(image_name, ContentFile(response.read()), save=False)

            # To maintain same behavior as the save() method, only save the form to the database when commit=True.
            if commit:
                image.save()
            return image
