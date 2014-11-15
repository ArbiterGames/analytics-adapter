import json
from django.http import HttpResponse


def geckoboard_arpu(request):
    response = {
        'item': [
            {'value': 200},
            {'value': 140}
        ]
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
