import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model extending AbstractUser with a UUID primary key
    and the additional fields defined in the specification.
    """
    # Replace the default integer PK with a UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    # Override/extend fields
    first_name = models.CharField(max_length=150)   # required (NOT NULL)
    last_name = models.CharField(max_length=150)    # required (NOT NULL)
    email = models.EmailField(unique=True)          # UNIQUE & NOT NULL
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Role(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    # Timestamp
    created_at = models.DateTimeField(default=timezone.now)

    # Keep Django's secure password hashing (AbstractUser.password)
    # We don't create a separate password_hash field because Django
    # already stores a hashed password safely in 'password'.

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Keep 'username' if you still want it, otherwise adjust

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    """
    Tracks which users are involved in a conversation.
    Many-to-many so we can support group or 1-to-1 chats.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Stores individual messages inside a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"