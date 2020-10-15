from django.shortcuts import render
from django.contrib.auth.models import User
from .models import college, chat_room_messages
from app1.models import additionalUser
from django.contrib import messages
from django.shortcuts import redirect
import json

def AlumniHome(request):
    dictMessages = []
    userAdditional = None
    try:
        username = str(request.user)
        if len(username) > 0:
            userCurrent = User.objects.get(username=username)
            userAdditional = additionalUser.objects.get(user=userCurrent)
            userCollege = userAdditional.college
            findChatroom = college.objects.get(college_name=userCollege)
            chatMessageModel = chat_room_messages.objects.get(chat_room_name=findChatroom)
            print("chat_room_messages ==", chatMessageModel)
            arrayMessages = [chatMessageModel.M1, chatMessageModel.M2, chatMessageModel.M3, chatMessageModel.M4, chatMessageModel.M5, chatMessageModel.M6, chatMessageModel.M7, chatMessageModel.M8, chatMessageModel.M9, chatMessageModel.M10]
            for i in arrayMessages:
                if i != "":
                    json_loads = json.loads(i)
                    dict_form = {
                        'message': str(json_loads['message'].replace("<br>", "\n")),
                        'userSent': json_loads['userSent'],
                        'sentUserName': json_loads['sentUserName'],
                        'userprofile': json_loads['userprofile'],
                    }
                    dictMessages.append(dict_form)
            print(dictMessages)
    except Exception as e:
        print("Error in vie", str(e))
        messages.warning(request, "your request not allowed please login...")
        return redirect('app1:HomePage')
    print(userAdditional.profile)
    return render(request, 'alumni/AlumniHomePage.html', {'messagesModel': dictMessages, 'currentProfile': userAdditional.profile})