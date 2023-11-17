from os import path, system

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from voice_gallery.models import Voice
from .models import VoiceResult
from .serializers import VoiceResultSerializer
from .tasks import offline_inference

task_status = None


class OfflineHotWordDetectionViewSet(ModelViewSet):
    serializer_class = VoiceResultSerializer
    queryset = VoiceResult.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def list(self, request, *args, **kwargs):
        global task_status
        voice_id = int(self.kwargs["voice_id"])
        try:
            voice = Voice.objects.get(id=voice_id)
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
                offline_inference_task = offline_inference.delay(convert_name, 'Speech/chime.wav',
                                                                 'Speech/release_files',
                                                                 voice_id)
                task_status = offline_inference_task.status
                message = "started"
                explanation = "the voice recognition has been started"

                return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice file not found"

            return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)
