from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import PitchShiftResultSerializers
from .models import PitchShiftResult
from os import path, mkdir
from voice_gallery.models import Voice
from django.http import HttpResponse


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PitchShiftProcessViewSet(ModelViewSet):
    queryset = PitchShiftResult.objects.all().order_by('publish_date')
    serializer_class = PitchShiftResultSerializers
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
            voice = Voice.objects.get(id=request.data['voice_id'], user=user)
            """
                put your pitch shift algorithm here
            """
            info = "load your pitch shift func here that could send json response"
            pitch_shift_result = PitchShiftResult.objects.create(sample_rate=info['output_sr'],
                                                                 channel=info['output_channels'],
                                                                 file_extension=info['output_format'],
                                                                 filename=info['output_file'],
                                                                 voice=voice)
            pitch_shift_result.save()
            message = "done"
            explanation = "the pitch shift voice is done"
            return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)


class GetPitchShiftResultViewSet(ModelViewSet):
    queryset = PitchShiftResult.objects.all().order_by('publish_date')
    serializer_class = PitchShiftResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        pitch_shift_result = PitchShiftResult.objects.all().order_by('publish_date')
        pitch_shift_result_serializer = PitchShiftResultSerializers(pitch_shift_result)
        return Response(data=pitch_shift_result_serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        pitch_shift_result_link = request.data["pitch_shift_result_link"]
        pitch_shift_result_file_extension = request.data["pitch_shift_result_file_extension"]
        f = open(pitch_shift_result_link, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = f'audio/{pitch_shift_result_file_extension}'
        response['Content-Length'] = path.getsize(pitch_shift_result_link)
        return response
