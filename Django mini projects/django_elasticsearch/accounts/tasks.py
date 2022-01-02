import time
from django.conf import settings
from opentracing.ext import tags


tracing = settings.OPENTRACING_TRACING

@tracing.trace()
def delay_1(request):
    with tracing.tracer.start_active_span("delay_1_child_span") as  delay_1_child_span: 
        delay_1_child_span.span.set_tag(tags.COMPONENT, 'django')
        delay_1_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
        delay_1_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
        time.sleep(5)
        with tracing.tracer.start_active_span("delay_1_child_child_span") as  delay_1_child_child_span: 
            delay_1_child_child_span.span.set_tag(tags.COMPONENT, 'django')
            delay_1_child_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
            delay_1_child_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
            time.sleep(5)

@tracing.trace()
def delay_2(request):
    with tracing.tracer.start_active_span("delay_2_child_span") as  delay_2_child_span: 
        delay_2_child_span.span.set_tag(tags.COMPONENT, 'django')
        delay_2_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
        delay_2_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
        time.sleep(5)

@tracing.trace()
def delay_3(request):
    with tracing.tracer.start_active_span("delay_3_child_span") as  delay_3_child_span: 
        delay_3_child_span.span.set_tag(tags.COMPONENT, 'django')
        delay_3_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
        delay_3_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
        time.sleep(5)
        with tracing.tracer.start_active_span("delay_3_child_child_span") as  delay_3_child_child_span: 
            delay_3_child_child_span.span.set_tag(tags.COMPONENT, 'django')
            delay_3_child_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
            delay_3_child_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
            time.sleep(5)

@tracing.trace()
def delay_4(request):
    with tracing.tracer.start_active_span("delay_4_child_span") as  delay_4_child_span: 
        delay_4_child_span.span.set_tag(tags.COMPONENT, 'django')
        delay_4_child_span.span.set_tag(tags.HTTP_METHOD, request.method)
        delay_4_child_span.span.set_tag(tags.HTTP_URL, request.build_absolute_uri())
        time.sleep(5)