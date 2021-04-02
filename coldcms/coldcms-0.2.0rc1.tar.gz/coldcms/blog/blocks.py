from coldcms.blog.models import BlogPage
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks


class BlogListValue(blocks.StructValue):
    @cached_property
    def blog_list(self):
        return BlogPage.objects.order_by("-date")[:self['number']]


class BlogListBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, label=_("Title"))
    number = blocks.IntegerBlock(min_value=0, max_value=10, help_text=_("Number of article in the block."))

    class Meta:
        icon = "list-ul"
        label = _("List Blog Block")
        value_class = BlogListValue
