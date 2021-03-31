from utilities.choices import ChoiceSet


class VirtualCircuitStatusChoices(ChoiceSet):
    """List of possible status for a Virtual Circuit."""

    STATUS_PENDING_CONFIGURATION = 'pending-configuration'
    STATUS_CONFIGURED = 'configured'
    STATUS_CONFIGURATION_ERROR = 'configuration-error'

    CHOICES = (
        (STATUS_PENDING_CONFIGURATION, 'Ответственный за ИТ'),
        (STATUS_CONFIGURED, 'Ответственный за ИБ'),
        (STATUS_CONFIGURATION_ERROR, 'Ответственный за сеть'),
    )
