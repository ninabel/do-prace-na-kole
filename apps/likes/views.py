import random

from django.http import HttpResponseNotFound
from django.contrib.contenttypes.models import ContentType
from django import template

from secretballot import views as secretballot_views

from apps.likes.utils import can_vote
from apps.likes import signals


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def can_vote_test(request, content_type, object_id, vote):
    return can_vote(
        content_type.get_object_for_this_type(id=object_id),
        request.user,
        request,
    )


def like(request, content_type, id, vote):
    if "HTTP_REFERER" not in request.META:
        return HttpResponseNotFound()

    url_friendly_content_type = content_type
    app, modelname = content_type.split("-")
    content_type = ContentType.objects.get(app_label=app, model__iexact=modelname)

    if _is_ajax(request):
        likes_template = "likes/inclusion_tags/likes_%s.html" % modelname.lower()
        try:
            template.loader.get_template(likes_template)
        except template.TemplateDoesNotExist:
            likes_template = "likes/inclusion_tags/likes.html"

        response = secretballot_views.vote(
            request,
            content_type=content_type,
            object_id=id,
            vote=vote,
            template_name=likes_template,
            can_vote_test=can_vote_test,
            extra_context={
                "likes_enabled": True,
                "can_vote": False,
                "content_type": url_friendly_content_type,
            },
        )
    else:
        redirect_url = "%s?v=%s" % (request.META["HTTP_REFERER"], random.randint(0, 10))
        response = secretballot_views.vote(
            request,
            content_type=content_type,
            object_id=id,
            vote=vote,
            redirect_url=redirect_url,
            can_vote_test=can_vote_test,
        )

    signals.object_liked.send(
        sender=content_type.model_class(),
        instance=content_type.get_object_for_this_type(id=id),
        request=request,
    )
    return response
