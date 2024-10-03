from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet

# Helper functions for encryption and decryption
def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()).decode()

class Channel(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user model
    encryption_key = models.CharField(max_length=44, blank=True, null=True)  # Store encryption key for the channel
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate encryption key if it doesn't exist
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key().decode()  # Generate and store a new encryption key
        super().save(*args, **kwargs)

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user model
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    encrypted_content = models.TextField(blank=True, null=True)  # Store encrypted messages
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure the channel's encryption key is available
        if not self.channel.encryption_key:
            raise ValueError("Encryption key for this channel is missing.")

        # Use the channel's encryption key for encryption
        encryption_key = self.channel.encryption_key.encode()
        self.encrypted_content = encrypt_message(self.content, encryption_key)
        super().save(*args, **kwargs)

    def get_decrypted_message(self):
        # Ensure the channel's encryption key is available
        if not self.channel.encryption_key:
            raise ValueError("Encryption key for this channel is missing.")

        # Use the channel's encryption key for decryption
        encryption_key = self.channel.encryption_key.encode()
        return decrypt_message(self.encrypted_content, encryption_key)
