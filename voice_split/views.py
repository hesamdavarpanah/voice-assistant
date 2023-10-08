from os import path, mkdir

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from voice_manager.models import Voice
from .models import LowDenoiseResult, HighDenoiseResult
from .serializers import HighDenoiseResultSerializers, LowDenoiseResultSerializers
from .tasks import high_denoise_task, low_denoise_task


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


high_denoise_status = None


class HighDenoiseProcessViewSet(ModelViewSet):
    queryset = HighDenoiseResult.objects.all().order_by('publish_date')
    serializer_class = HighDenoiseResultSerializers
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        global high_denoise_status
        output_files = 'voice_split/output_files'
        temp_dir = 'voice_split/temp'
        is_output_files = path.isdir(output_files)
        is_temp_dir = path.isdir(temp_dir)
        if not is_output_files:
            mkdir(output_files)
        if not is_temp_dir:
            mkdir(temp_dir)
        try:
            # user = User.objects.get(username=request.user.username)
            user = User.objects.get(id=1)
            voice = Voice.objects.get(id=request.data['voice_id'], user=user)
            try:
                find_result = HighDenoiseResult.objects.get(voice=voice)
                find_result_serializer = HighDenoiseResultSerializers(find_result)
                high_denoise_status = None
                return Response(data=find_result_serializer.data, status=200)
            except ObjectDoesNotExist:
                if high_denoise_status:
                    message = high_denoise_status.lower()
                    explanation = f"the high voice denoiser is {high_denoise_status.lower()}"
                    return Response(data={"message": message, "explanation": explanation}, status=200)
                else:
                    the_high_denoise_task = high_denoise_task.delay(request.data['voice_id'],
                                                                    request.data['file_extension'], temp_dir,
                                                                    temp_dir)
                    high_denoise_status = the_high_denoise_task.status
                    message = "started"
                    explanation = "the high denoise voice started"
                    return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)


class HighDenoiseResultViewSet(ModelViewSet):
    queryset = HighDenoiseResult.objects.all().order_by('publish_date')
    serializer_class = HighDenoiseResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        high_denoise = HighDenoiseResult.objects.all().order_by('publish_date')
        high_denoise_serializers = HighDenoiseResultSerializers(high_denoise)
        return Response(data=high_denoise_serializers.data, status=200)

    def create(self, request, *args, **kwargs):
        high_denoise_result_link = request.data["high_denoise_result_link"]
        high_denoise_result_file_extension = request.data["high_denoise_result_file_extension"]
        f = open(high_denoise_result_link, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = f'audio/{high_denoise_result_file_extension}'
        response['Content-Length'] = path.getsize(high_denoise_result_link)
        return response


low_denoise_status = None


class LowDenoiseProcessViewSet(ModelViewSet):
    queryset = LowDenoiseResult.objects.all().order_by('publish_date')
    serializer_class = LowDenoiseResultSerializers
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=1)
        global low_denoise_status
        try:
            voice = Voice.objects.get(id=request.data['voice_id'], user=user)
            try:
                find_result = LowDenoiseResult.objects.get(voice=voice)
                find_result_serializer = LowDenoiseResultSerializers(find_result)
                low_denoise_status = None
                return Response(data=find_result_serializer.data, status=200)
            except ObjectDoesNotExist:
                if low_denoise_status:
                    message = low_denoise_status.lower()
                    explanation = f"the low voice denoiser is {low_denoise_status.lower()}"
                    return Response(data={"message": message, "explanation": explanation}, status=200)
                else:
                    the_low_denoise_task = low_denoise_task.delay(request.data['voice_id'],
                                                                  request.data['hop_length'],
                                                                  request.data['batch_size'],
                                                                  request.data['crop_size'],
                                                                  request.data['n_fft'],
                                                                  request.data['sr'],
                                                                  request.data['file_extension'])
                    low_denoise_status = the_low_denoise_task.status
                    message = "started"
                    explanation = "the low denoise voice started"
                    return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)

        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)


class LowDenoiseResultViewSet(ModelViewSet):
    queryset = LowDenoiseResult.objects.all().order_by('publish_date')
    serializer_class = LowDenoiseResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        low_denoise = LowDenoiseResult.objects.all().order_by('publish_date')
        low_denoise_serializers = LowDenoiseResultSerializers(low_denoise)
        return Response(data=low_denoise_serializers.data, status=200)

    def create(self, request, *args, **kwargs):
        low_denoise_result_link = request.data["low_denoise_result_link"]
        low_denoise_result_file_extension = request.data["low_denoise_result_file_extension"]
        f = open(low_denoise_result_link, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = f'audio/{low_denoise_result_file_extension}'
        response['Content-Length'] = path.getsize(low_denoise_result_link)
        return response
