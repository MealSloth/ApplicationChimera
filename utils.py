from Chimera.settings import PROTOCOL, GCS_URL
from django.core.serializers import serialize


def model_to_dict(model):
    dictionary = {}
    model_dictionary = serialize('python', [model, ])[0].get('fields')
    if not model_dictionary.get('id'):
        model_dictionary['id'] = str(model.id)
    for key, value in model_dictionary.iteritems():
        dictionary[key] = value
    return dictionary


def blob_to_dict(blob):
    new_model = model_to_dict(blob)
    new_model['url'] = PROTOCOL + GCS_URL + blob.gcs_id
    return new_model


def format_phone_number(country_code, phone_number):
    if country_code is None or country_code <= 0:
        country_code = 1
    country_code = "+" + str(country_code)
    phone_number = str(phone_number)
    phone_number = phone_number.replace("+", "")
    phone_number = phone_number.replace("-", "")
    phone_number = phone_number.replace("_", "")
    phone_number = phone_number.replace(" ", "")
    return country_code + "_" + phone_number
