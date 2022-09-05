import json
import re

import channels.layers
from asgiref.sync import async_to_sync
from core.trade import Trade
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
@login_required()
def trade(request, value):
    value = re.sub("'", '"', value)
    value = json.loads(value)

    tradeObject = Trade(request.user, "market", value["type"], value["pair"], value["amount"])
    result = tradeObject.result
    if result["state"] == 0:
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)("orderBook", {"type": "order.display", "content": result})
    return JsonResponse(result)
