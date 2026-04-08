from django.utils import timezone
from django.db.models import Count, F, ExpressionWrapper, FloatField
from responders.models import Responder

def balanced_respons(required_skills=None):
  now = timezone.now()
  queryset = Responder.objects.filter(shifts__start_time__lte=now, shifts__end_time__gte=now)

  if required_skills:
    queryset = queryset.filter(skills__id__in=required_skills)
    queryset = queryset.distinct()
  queryset = queryset.annotate(current_load_count=Count('loads'))
  queryset = queryset.filter(current_load_count__lt=F('max_load')).annotate(utilization=ExpressionWrapper(
    (F('current_load_count') * 1.0 / F('max_load')) * 100.0, output_field=FloatField())).order_by('utilization') 

  return queryset