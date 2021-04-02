from coldcms.form_page.models import FormPage
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get("custom_url"):
            return self.get("custom_url") + self.get("extra_url", "")
        elif self.get("page"):
            return self.get("page").url + self.get("extra_url", "")
        return self.get("extra_url") or "#"

    def text(self):
        if self.get("text"):
            return self.get("text")
        if self.get("page"):
            return self.get("page").title
        return self.url()


class CTABlock(blocks.StructBlock):
    text = blocks.CharBlock(
        label=_("Link text"),
        help_text=_(
            "Use this as the text of an external URL or if you want to "
            "override the Page's title"
        ),
        required=False,
        max_length=40,
    )
    custom_url = blocks.CharBlock(label=_("External URL"), required=False)
    page = blocks.PageChooserBlock(
        label=_("Link to an internal page"),
        help_text=_("Ignored if the external URL is used"),
        required=False,
    )
    extra_url = blocks.CharBlock(
        label=_("Append to URL"),
        help_text=_("Use this to optionally append a #hash or querystring to the URL."),
        required=False,
        default="",
    )
    blank = blocks.BooleanBlock(required=False, label=_("Open link in a new tab"))

    class Meta:
        icon = "site"
        value_class = LinkStructValue


def svg_only(value):
    if value.content_type != "image/svg+xml":
        raise ValidationError(_(f"{value} is not an svg file"))


class ImageBlock(blocks.StructBlock):
    image_type = blocks.ChoiceBlock(
        choices=[
            ("image", "JPG, PNG, WEBP, GIF"),
            ("svg", "SVG"),
        ],
        required=True,
        default="image",
        label="Image type",
        classname=(
            "coldcms-admin__choice-handler coldcms-admin__choice-handler--image_type"
        ),
    )
    img = ImageChooserBlock(
        required=False,
        label="Image",
        classname=(
            "coldcms-admin__choice-handler-target--image_type "
            "coldcms-admin__choice-handler-hidden-if--svg"
        ),
    )
    svg = DocumentChooserBlock(
        required=False,
        label="Svg",
        classname=(
            "coldcms-admin__choice-handler-target--image_type "
            "coldcms-admin__choice-handler-hidden-if--image"
        ),
        validators=[svg_only]
    )
    alt = blocks.CharBlock(
        max_length=200,
        label=_("Svg description"),
        default="",
        classname=(
            "coldcms-admin__choice-handler-target--image_type "
            "coldcms-admin__choice-handler-hidden-if--image"
        ),
        required=False
    )

    class Meta:
        icon = "image"
        label = _("Image block")


class FormStructValue(blocks.StructValue):
    def text(self):
        if self.get("text"):
            return self.get("text")
        if self.get("page"):
            return self.get("page").title
        return ""

    def form_page(self):
        if self.get("page"):
            return self.get("page")
        return None


class FormBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        label=_("Form title"),
        help_text=_(
            "Use this as the text of an external URL or if you want to "
            "override the Page's title"
        ),
        required=False,
        max_length=40,
    )
    page = blocks.PageChooserBlock(
        label=_("Link to an internal page"),
        required=True,
        page_type=FormPage,
    )

    class Meta:
        icon = "form"
        value_class = FormStructValue


class LogoBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=False, max_length=100, label=_("Name"))
    logo = ImageBlock(required=False)

    class Meta:
        icon = "radio-full"
        label = _("Logo Block")


class QuoteBlock(blocks.StructBlock):
    author = blocks.CharBlock(required=False, max_length=100, label=_("Author"))
    quote = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "ol", "ul", "hr"],
        label=_("Quote"),
    )

    class Meta:
        icon = "openquote"
        label = _("Quote Block")


class ImageUrlBlock(blocks.StructBlock):
    url = blocks.URLBlock(required=False, label=_("URL"))
    image = ImageBlock(required=True, label=_("Image"))
    caption = blocks.CharBlock(max_length=250, label=_("Caption"), required=False)

    class Meta:
        icon = "image"
        label = _("Image Url Block")


class HeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, label=_("Title"))
    image = ImageBlock(label=_("Image"))
    text = blocks.TextBlock(required=False, max_length=250, label=_("Header text"))
    buttons = blocks.ListBlock(CTABlock(icon="link"), label=_("Buttons"))

    class Meta:
        icon = "image"
        label = _("Header Block")
