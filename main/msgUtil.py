from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta, timezone
from django.db import transaction
from django.db.models import Q

def getAllMessagesByUser(user):
    result = []
    messagesAnswerList = MessagesAnswer.objects.all()
    messagesAnswerIdList = []
    for messageAnswer in messagesAnswerList:
        messagesAnswerIdList.append(messageAnswer.message.id)
    msgs = Messages.objects.filter(Q(from_user=user) | Q(to_user=user)).exclude(id__in=messagesAnswerIdList)
    for msg in msgs:
        from_user = User.objects.filter(id=msg.from_user.id).first()
        is_read = msg.is_read
        if MessagesAnswer.objects.filter(answer_to=msg).exists():
            tempMsgA = MessagesAnswer.objects.filter(answer_to=msg).last()
            last_msg = Messages.objects.filter(id=tempMsgA.message.id).first()
            is_read = last_msg.is_read
        result.append({
            "id": msg.id,
            "from_user_id": from_user.id,
            "from_user_name" : from_user.first_name + " "+ from_user.last_name,
            "title" : msg.title,
            "date": msg.send_date,
            "is_read": is_read 
        }) 
    return result

def getMessageDetails(message_id, user):
    results = None
    older = []
    msg = Messages.objects.filter(id=message_id).filter(Q(from_user=user) | Q(to_user=user)).first()
    msg.is_read = 1
    msg.save()
    msg.message
    msgsA = MessagesAnswer.objects.filter(answer_to=msg).order_by('-message__send_date')
    if msgsA != None:
        for msgA in msgsA:
            tempMsg = Messages.objects.filter(id=msgA.message.id).first()
            if tempMsg.to_user == user and tempMsg.is_read == 0:
                tempMsg.is_read = 1
                tempMsg.save()
            tempUser = User.objects.filter(id=tempMsg.from_user.id).first()
            older.append({
                "first_name": tempUser.first_name,
                "last_name" : tempUser.last_name,
                "date": tempMsg.send_date,
                "content": tempMsg.message
            })
    from_user = User.objects.filter(id=msg.from_user.id).first()
    results = {
        "id": msg.id,
        "from_user_id": from_user.id,
        "from_user_name" : from_user.first_name + " "+ from_user.last_name,
        "title" : msg.title,
        "date": msg.send_date,
        "content": msg.message,
        "olders": older
    }
    return results

def createMessageAnswer(answer_to, from_user, to_user, content, title):
    sid = transaction.savepoint()
    try: 
        msg = Messages.objects.create(
            from_user = from_user,
            to_user = to_user,
            title = title,
            message = content,
            is_read = False,
            send_date = datetime.now()
        )
        msgA = MessagesAnswer.objects.create(
            message = msg,
            answer_to = answer_to
        )
        transaction.savepoint_commit(sid)
        return True
    except:
        transaction.savepoint_rollback(sid)
        return False

def createMessage(from_user, to_user, content, title):
    sid = transaction.savepoint()
    try: 
        msg = Messages.objects.create(
            from_user = from_user,
            to_user = to_user,
            title = title,
            message = content,
            is_read = False,
            send_date = datetime.now()
        )
        transaction.savepoint_commit(sid)
        return True
    except:
        transaction.savepoint_rollback(sid)
        return False
