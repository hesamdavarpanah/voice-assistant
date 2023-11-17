from mutagen.wave import WAVE

from .models import Voice
from .serializers import VoiceSerializer

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class CRUDVoiceViewSet(ModelViewSet):
    serializer_class = VoiceSerializer
    queryset = Voice.objects.all().order_by('publish_date')
    pagination_class = MyPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def retrieve(self, request, *args, **kwargs):
        try:
            voice = Voice.objects.all()
            voice_serializer = VoiceSerializer(voice)
            return Response(data=voice_serializer.data, status=200)
        except Exception as exception:
            return Response(data=f"exception: {str(exception.__class__)}", status=500)

    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES['voice_file']
            file_size = file.size / (1024 * 1024)
            audio_file_duration = WAVE(request.data['voice_file']).info.length
            if file_size > 30:
                message = "not support"
                explanation = "the voice is too large, use voice file less than 30MB"

                return Response({"message": message, "explanation": explanation}, status=400)
            if audio_file_duration > 60:
                message = "not support"
                explanation = "the voice is too long, use voice file less than 1min"

                return Response({"message": message, "explanation": explanation}, status=400)
            user = User.objects.get(username=self.request.username)
            voice = Voice.objects.create(title=request.data['title'], description=request.data['description'],
                                         voice_file=request.data['voice_file'], user=user)
            voice.save()

            message = "the voice created"
            explanation = "the voice has been created successfully"

            return Response({"message": message, "explanation": explanation}, status=201)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)

    def update(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            voice = Voice.objects.get(pk=pk)
            voice.title = request.data['title']
            voice.description = request.data['description']
            voice.voice_file = request.data['voice_file']

            voice.save()

            message = "the voice updated"
            explanation = "the voice has been updated successfully"

            return Response({"message": message, "explanation": explanation}, status=204)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)

    def destroy(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            voice = Voice.objects.get(pk=pk)

            voice.delete()

            message = "the voice deleted"
            explanation = "the voice has been deleted successfully"

            return Response({"message": message, "explanation": explanation}, status=204)
        except ObjectDoesNotExist:
            message = "the voice not found"
            explanation = "the voice does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)
