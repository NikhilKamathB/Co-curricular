from rest_framework import viewsets
from .models import Course
from .serializer import CourseSerializer


# Create your views here.
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
