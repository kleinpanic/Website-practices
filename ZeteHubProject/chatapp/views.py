from django.shortcuts import render, redirect, get_object_or_404
from .models import Channel, Message
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Check if the user is an admin
def admin_required(user):
    return user.is_staff

# Display a list of all chat channels
@login_required
def list_channels_view(request):
    channels = Channel.objects.all()  # Get all channels
    return render(request, 'chatapp/list_channels.html', {'channels': channels})

# Create a new chat channel (admin only)
@login_required
@user_passes_test(admin_required)
def create_channel_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        admin = request.user

        # Create the channel
        new_channel = Channel.objects.create(name=name, admin=admin)
        messages.success(request, f"Channel '{name}' created successfully.")

        # Redirect to the newly created channel's chatroom
        return redirect('chatroom', channel_name=new_channel.name)  # Removed admin_username

    return render(request, 'chatapp/create_channel.html')

# Chatroom view where users can send and see messages
@login_required
def chatroom_view(request, channel_name):
    # Fetch channel based on its name (admin_username removed)
    channel = get_object_or_404(Channel, name=channel_name)
    messages_list = Message.objects.filter(channel=channel).order_by('timestamp')

    # Decrypt all the messages before sending them to the template
    for message in messages_list:
        try:
            message.content = message.get_decrypted_message()
        except AttributeError:
            pass  # If get_decrypted_message doesn't exist, we skip decryption

    return render(request, 'chatapp/chatroom.html', {
        'channel': channel,
        'messages': messages_list
    })

# Handle sending messages in a chatroom
@login_required
def send_message(request, channel_name):
    if request.method == 'POST':
        # Fetch channel based on its name
        channel = get_object_or_404(Channel, name=channel_name)
        content = request.POST['content']
        message = Message.objects.create(user=request.user, channel=channel, content=content)
        message.save()

        return redirect('chatroom', channel_name=channel_name)
