from django.dispatch import Signal


tumbleitem_saved = Signal(providing_args=['instance','created'])
tumbleitem_deleted = Signal(providing_args=['instance',])
