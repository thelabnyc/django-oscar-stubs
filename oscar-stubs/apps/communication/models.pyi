from oscar.apps.communication.abstract_models import (
    AbstractCommunicationEventType,
    AbstractEmail,
    AbstractNotification,
)

class Email(AbstractEmail):
    id: int

class CommunicationEventType(AbstractCommunicationEventType):
    id: int

class Notification(AbstractNotification):
    id: int
