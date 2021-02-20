from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from channel.models import Message
from channel.forms import MessageForm


class MessageListView(ListView):
    model = Message
    template_name = 'channel/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(channel_id=1)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'channel_nav': 'active',
            'message_form': MessageForm()
        })
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('channel:message-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.channel_id = 1
        return super().form_valid(form)

