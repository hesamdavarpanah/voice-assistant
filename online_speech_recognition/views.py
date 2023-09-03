from celery.app import default_app
from django.core.exceptions import ObjectDoesNotExist
from pyaudio import PyAudio
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Device
from .serializers import DeviceSerializer
from .tasks import online


class SystemDeviceViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        try:
            p = PyAudio()
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if dev.get('maxInputChannels'):
                    try:
                        device = Device.objects.get(id=i)
                        device.device_name = dev.get('name')
                        device.description = "This audio channel is active"
                        device.save()
                    except ObjectDoesNotExist:
                        device = Device.objects.create(id=i, device_name=dev.get('name'),
                                                       description="This audio channel is active")
                        device.save()

            device_list = Device.objects.all()
            device_serializer = DeviceSerializer(device_list, many=True)
            return Response(data=device_serializer.data, status=200)
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)


task_status = None
task_id = None


class OnlineVoiceDetectionViewSet(ModelViewSet):
    http_method_names = ['post', 'delete']

    def create(self, request, *args, **kwargs):
        global task_status
        global task_id
        try:
            device_id = request.data['id']
            if task_status:
                message = task_status.lower()
                explanation = f"the voice recognition is {task_status.lower()}"
                return Response(data={"message": message, "explanation": explanation}, status=200)
            online_task = online.delay(device_id, 'localhost', 6379, 1)
            task_id = online_task.id
            task_status = online_task.status
            message = "started"
            explanation = f"the online voice recognition has been started on device id number {device_id}"
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

        return Response({"message": message, "explanation": explanation}, status=201)

    def destroy(self, request, *args, **kwargs):
        global task_status
        global task_id
        if task_status and task_id:
            default_app.control.revoke(task_id=task_id, terminate=True, signal='SIGKILL')
            task_id = None
            task_status = None
            message = "stopped"
            explanation = f"the online voice recognition has been stopped"

            return Response({"message": message, "explanation": explanation}, status=204)
        else:
            message = "not started"
            explanation = f"the online voice recognition has been not started,first start online voice " \
                          f"recognition please"

            return Response({"message": message, "explanation": explanation}, status=404)
