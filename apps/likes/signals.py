import django.dispatch

likes_enabled_test = django.dispatch.Signal()
can_vote_test = django.dispatch.Signal()

object_liked = django.dispatch.Signal()
