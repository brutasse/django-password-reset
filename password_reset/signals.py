from django.dispatch import Signal

# signal sent when a user successfully recovers his/her password
user_recovers_password = Signal(
    providing_args=['user', 'request']
)
