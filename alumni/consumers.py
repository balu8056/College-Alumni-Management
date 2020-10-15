from channels.consumer import AsyncConsumer
import asyncio
from app1.models import additionalUser
from django.contrib.auth.models import User
from app1.models import additionalUser
from .models import college, chat_room_messages
import json

chat_room = "Unknown"
college_name_in_user = ""
chat_room_m = ""

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected===>", event)
        global chat_room, college_name_in_user, chat_room_m
        #other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        if User.objects.filter(username=me):
            requesting_user = User.objects.get(username=me)
            requested_user = additionalUser.objects.get(user=requesting_user)
            if requested_user.college.index(' '):
                college_name_in_user = requested_user.college
                chat_room = requested_user.college.replace(' ', '_')
                if chat_room.index(','):
                    chat_room = chat_room.replace(',', '_')
        if college.objects.filter(college_name=college_name_in_user):
            college_name = college.objects.get(college_name=college_name_in_user)
            if chat_room_messages.objects.filter(chat_room_name=college_name):
                chat_room_m = chat_room_messages.objects.get(chat_room_name=college_name)
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive===>", event)
        initial = event.get('text', None)
        if initial is not None:
            load_dict = json.loads(initial)
            msg = load_dict.get('message')
            msg_send_user = load_dict.get("user")
            userprofile = load_dict.get('userprofile')
            me = self.scope['user']
            dict_mes = json.dumps({'message': msg, 'userSent': msg_send_user, 'sentUserName': str(me), 'userprofile': userprofile})
            await self.channel_layer.group_send(
                self.chat_room, {
                    "type": "chat_room_message",
                    "text": dict_mes,
                }
            )
            chat_room_m.M1, chat_room_m.M2, chat_room_m.M3, chat_room_m.M4, chat_room_m.M5, chat_room_m.M6, chat_room_m.M7, chat_room_m.M8, chat_room_m.M9, chat_room_m.M10 = chat_room_m.M2, chat_room_m.M3, chat_room_m.M4, chat_room_m.M5, chat_room_m.M6, chat_room_m.M7, chat_room_m.M8, chat_room_m.M9, chat_room_m.M10, dict_mes
            chat_room_m.save()

    async def chat_room_message(self, event):
        print("chat_room_message===>", event)
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })
    async def websocket_disconnect(self, event):
        print("disconnected===>", event)
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )