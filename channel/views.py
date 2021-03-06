from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from channel.models import Message, Channel
from channel.forms import MessageForm


class ChannelListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = 'channel/channel_list.html'
    context_object_name = 'channels'

    def get_queryset(self):
        return Channel.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'channel_nav': 'active'
        })
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'channel/message_list.html'
    context_object_name = 'messages'

    def get_object(self):
        return get_object_or_404(Channel, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return Message.objects.filter(channel=self.get_object()).order_by('created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'channel_nav': 'active',
            'message_form': MessageForm(),
            'channel': self.get_object()
        })
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('channel:message-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.channel_id = self.kwargs.get('pk')
        return super().form_valid(form)

