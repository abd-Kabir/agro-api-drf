from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config.utils.api_exceptions import APIValidation
from apps.technics.models import Technique
from apps.files_app.models import File
from apps.files_app.utils import upload_file

from os import remove as delete_file
import logging

logger = logging.getLogger()


class FileRetrieveAPIView(APIView):

    def get(self, request, pk):
        try:
            tech_passport = Technique.objects.get(pk=pk).technique_passport
            tech_manual = Technique.objects.get(pk=pk).technique_manual
            y = [{'id': tech_passport.id, 'url': tech_passport.path, 'name': tech_passport.name,
                  'type': 'Texnika passporti'},
                 {'id': tech_manual.id, 'url': tech_manual.path, 'name': tech_manual.name,
                  'type': 'Texnika xaqida ma’lumot va qo’llanma'}]
            images = File.objects.filter(technique_id=pk, content_type__contains='image')
            x = []
            if images:
                for image in images:
                    files = {'id': image.id, 'url': image.path, 'name': image.name}
                    x.append(files)
            logger.debug(f'func_name: {str(self.get_view_name())}; retrieving_files_belong_tech-{str(pk)}-id '
                         f'; user:{str(request.user)};')

            return Response({
                "message": "Success",
                "files": x,
                "docs": y,
                "status": status.HTTP_200_OK
            })
        except Exception as exc:
            raise APIValidation(detail=exc, status_code=status.HTTP_404_NOT_FOUND)


class DragDropCreateAPIView(APIView):
    def post(self, request):
        if request.FILES:
            files = {}
            file = request.data.get('file')
            e_file = upload_file(file=file, tech_id=None)
            files['id'] = e_file.id
            files['url'] = e_file.path
            logger.debug(f'func_name: {str(self.get_view_name())}; drag_drop_file_created-{e_file.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "File successfully uploaded",
                "files": files,
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)


class DragDropDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        file = self.get_object(pk)
        delete_file(file.path)
        file.delete()
        logger.debug(f'func_name: {str(self.get_view_name())}; drag_drop_file_deleted-{str(pk)}-id '
                     f'; user:{str(request.user)};')
        return Response({
            "message": "File successfully deleted",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
