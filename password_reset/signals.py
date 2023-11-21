from django.dispatch import Signal

# signal sent when users successfully recover their passwords
# args=['user', 'request']
user_recovers_password = Signal()
