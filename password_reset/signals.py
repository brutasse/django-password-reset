from django.dispatch import Signal

# signal sent when users successfully recover their passwords
user_recovers_password = Signal(
    providing_args=['user', 'request']
)
