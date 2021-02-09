import asyncio
import websockets
from django.shortcuts import render
from django.conf import settings

conversations = []


async def ping_server(message):
    async with websockets.connect(settings.WEBSOCKET_URI) as ws:
        await ws.send(message)
        return await ws.recv()


def home(request):
    response_ws = 'N/A'
    if request.method == 'POST':
        response_ws = asyncio.new_event_loop().run_until_complete(ping_server(request.POST['reply']))
        conversations.append((request.POST['reply'], response_ws))
    else:
        conversations.clear()
        response_ws = asyncio.new_event_loop().run_until_complete(ping_server('<START>'))
        conversations.append(('<START>', response_ws))
    if len(conversations) > 3:
        conversations.pop(0)
    
    return render(request, 'home.html', {'conversations': conversations})


def about(request):
    conversations.clear()
    return render(request, 'about.html', {})
