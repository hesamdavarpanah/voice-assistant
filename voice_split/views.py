from os import path, mkdir

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from voice_gallery.models import Voice
from .models import DenoiseResult
from .serializers import DenoiseResultSerializers
from .tasks import denoise_task


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


denoise_status = None


class DenoiseProcessViewSet(ModelViewSet):
    queryset = DenoiseResult.objects.all().order_by('publish_date')
    serializer_class = DenoiseResultSerializers
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        global denoise_status
        try:
            user = User.objects.get(username=request.user.username)
            voice = Voice.objects.get(id=request.data['voice_id'], user=user)
            try:
                find_result = DenoiseResult.objects.get(voice=voice)
                find_result_serializer = DenoiseResultSerializers(find_result)
                denoise_status = None
                return Response(data=find_result_serializer.data, status=200)
            except ObjectDoesNotExist:
                if denoise_status:
                    message = denoise_status.lower()
                    explanation = f"the voice denoiser is {denoise_status.lower()}"
                    return Response(data={"message": message, "explanation": explanation}, status=200)
                else:
                    the_denoise_task = denoise_task.delay(request.data['voice_id'],
                                                                    request.data['file_extension'], temp_dir,
                                                                    temp_dir)
                    denoise_status = the_denoise_task.status
                    message = "started"
                    explanation = "the denoise voice started"
                    return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)


class DenoiseResultViewSet(ModelViewSet):
    queryset = DenoiseResult.objects.all().order_by('publish_date')
    serializer_class = DenoiseResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        denoise = DenoiseResult.objects.all().order_by('publish_date')
        denoise_serializers = DenoiseResultSerializers(denoise)
        return Response(data=denoise_serializers.data, status=200)

    def create(self, request, *args, **kwargs):
        denoise_result_link = request.data["denoise_result_link"]
        denoise_result_file_extension = request.data["denoise_result_file_extension"]
        f = open(denoise_result_link, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = f'audio/{denoise_result_file_extension}'
        response['Content-Length'] = path.getsize(denoise_result_link)
        return response