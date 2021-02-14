import json


class Constant:
    APP_NAME = 'MU Online Judge'


def get_constant(key, data_type='str'):
    from core.models import Constant as ConstantModel
    from pydoc import locate

    try:
        constant = ConstantModel.objects.get(key=key)
    except ConstantModel.DoesNotExist:
        constant = ConstantModel.objects.create(key=key, value=getattr(Constant, key))

    if data_type == 'json':
        return json.loads(constant.value)
    return locate(data_type)(constant.value)
