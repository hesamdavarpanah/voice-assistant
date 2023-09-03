from os import path, system

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Voice, VoiceResult
from .serializers import VoiceSerializer, VoiceResultSerializer
from .tasks import offline_inference


class CRUDVoiceViewSet(ModelViewSet):
    serializer_class = VoiceSerializer
    queryset = Voice.objects.all().order_by('publish_date')
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def retrieve(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username='admin')
            voice = Voice.objects.filter(user=user).order_by('publish_date')
            voice_serializer = VoiceSerializer(voice, many=True)
            return Response(data=voice_serializer.data, status=200)
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username='admin')
            voice = Voice.objects.create(title=request.data['title'], description=request.data['description'],
                                         voice_file=request.data['voice_file'], user=user)
            voice.save()

            message = "the voice created"
            explanation = "the voice has been created successfully"

            return Response({"message": message, "explanation": explanation}, status=201)
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def update(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            user = User.objects.get(username='admin')
            voice = Voice.objects.get(pk=pk, user=user)
            voice.title = request.data['title']
            voice.description = request.data['description']
            voice.voice_file = request.data['voice_file']

            voice.save()

            message = "the voice updated"
            explanation = "the voice has been updated successfully"

            return Response({"message": message, "explanation": explanation}, status=204)
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def destroy(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            user = User.objects.get(username='admin')
            voice = Voice.objects.get(pk=pk, user=user)

            voice.delete()

            message = "the voice deleted"
            explanation = "the voice has been deleted successfully"

            return Response({"message": message, "explanation": explanation}, status=204)
        except ObjectDoesNotExist:
            message = "the voice not found"
            explanation = "the voice does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)


task_status = None


class OfflineVoiceDetectionViewSet(ModelViewSet):
    serializer_class = VoiceResultSerializer
    queryset = VoiceResult.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        global task_status
        user = User.objects.get(username='admin')
        voice = Voice.objects.get(id=request.data['id'], user=user)
        try:
            find_result = VoiceResult.objects.get(voice=voice)
            voice_result_serializer = VoiceResultSerializer(find_result)
            task_status = None
            return Response(data=voice_result_serializer.data, status=200)
        except ObjectDoesNotExist:
            if task_status:
                message = task_status.lower()
                explanation = f"the voice recognition is {task_status.lower()}"
                return Response(data={"message": message, "explanation": explanation}, status=200)

            name = path.split(voice.voice_file.path)[-1][:-4]
            convert_name = f'Speech/temp/convert_{name}.wav'
            system(f"ffmpeg -i {voice.voice_file.path} -ar 16000 -ac 1 {convert_name} -y")
            offline_inference_task = offline_inference.delay(convert_name, 'Speech/chime.wav', 'Speech/release_files',
                                                             request.data['id'])
            task_status = offline_inference_task.status
            message = "started"
            explanation = "the voice recognition has been started"

            return Response({"message": message, "explanation": explanation}, status=200)
