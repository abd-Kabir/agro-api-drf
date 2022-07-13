from config.settings import FILE_UPLOAD_DIR
from apps.files_app.models import File

from os.path import join as join_path
from os import sep
import uuid
import time


def get_extension(filename: str) -> str:
    return filename.split(".")[-1]


def unique_code() -> str:
    return "%s%s" % (time.time_ns(), str(uuid.uuid4()).replace("-", ""))


def upload_path() -> str:
    return FILE_UPLOAD_DIR


def media_path(file_name):
    return f'media/uploads/{file_name}'


def gen_new_name(file) -> str:
    return "%s.%s" % (unique_code(), get_extension(filename=file.name))


def upload_file(file, tech_id=None, order_id=None, leasing_id=None, guarantor_id=None, expert_assessment_id=None):
    name = file.name
    size = file.size
    gen_name = gen_new_name(file)
    content_type = file.content_type
    extension = get_extension(filename=file.name)
    path = media_path(gen_name)
    if tech_id:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension,
                             technique=tech_id)
    elif order_id:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension,
                             order=order_id)
    elif leasing_id:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension,
                             leasing_agreem=leasing_id)
    elif guarantor_id:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension,
                             guarantee_agreem=guarantor_id)
    elif expert_assessment_id:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension,
                             expert_assessment=expert_assessment_id)
    else:
        uploaded_file = File(name=name,
                             size=size,
                             gen_name=gen_name,
                             path=path,
                             content_type=content_type,
                             extension=extension)
    uploaded_file.save()

    with open(join_path(upload_path(), gen_name.replace(sep, '/')), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return uploaded_file
