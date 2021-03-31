from django.db.models.signals import post_save
from django.dispatch import receiver
from kitchensink.tasks.aws import task_publish_to_aws
from kitchensink.models import ArchieDoc, Sheet, FormContent


@receiver(post_save, sender=ArchieDoc)
@receiver(post_save, sender=Sheet)
@receiver(post_save, sender=FormContent)
def publish_on_save(sender, instance, **kwargs):
    task_publish_to_aws.delay(
        filepath=instance.sink_publish_path(),
        data=instance.get_data(),
        mode="preview"
    )
