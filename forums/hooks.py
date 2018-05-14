from django.utils.html import conditional_escape, escape, linebreaks, urlize
from django.utils.safestring import mark_safe

from .conf import settings


class ForumsDefaultHookSet(object):

    def can_access(self, request, forum):
        "can the given request access the given forum?"
        return True

    def parse(self, text):
        return conditional_escape(
            mark_safe(
                linebreaks(
                    urlize(
                        escape(text)
                    )
                )
            )
        )


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.PINAX_FORUMS_HOOKSET, attr)


hookset = HookProxy()
