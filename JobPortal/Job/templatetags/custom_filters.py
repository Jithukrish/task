from django import template
register = template.Library()

@register.filter
def unique_names(messages, user):
    unique_receivers = set()
    unique_list = []
    for message in messages:
        if message.sender == user:
            if message.receiver not in unique_receivers:
                unique_receivers.add(message.receiver)
                unique_list.append(message)
    return unique_list