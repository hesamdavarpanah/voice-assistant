from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import PitchShiftResultSerializers, PitchShiftResultFileSerializers
from .models import PitchShiftResult
from voice_manager.models import Voice
from .pitch_shift.pitch_shift import Pitch_shift


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PitchShiftViewSet(ModelViewSet):
    queryset = PitchShiftResult.objects.all().order_by('publish_date')
    serializer_class = PitchShiftResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username='admin')
        query_set = queryset.filter(user=user)
        # query_set = queryset.filter(user=self.request.user)
        return query_set

    def create(self, request, *args, **kwargs):
        try:
            voice = Voice.objects.get(id=request.data['voice_id'])
            pitch_shift = Pitch_shift('pitch_shift_recognition/temp')
            name, file_path = pitch_shift.change_sr_ch(voice.voice_file)
            audio = pitch_shift.load(file_path)
            to_process, audio = pitch_shift.prepare(audio, request.data['start'], request.data['end'])
            board = pitch_shift.board_define(request.data['step'])
            effected = pitch_shift.effect(board, to_process)
            output_file = pitch_shift.generate(audio, effected, name,
                                               'pitch_shift_recognition/output_files',
                                               request.data['step'])
            pitch_shift.clean_temp(name)
            info = pitch_shift.get_log(output_file, 'wav')
            print(info)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)