from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

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
    checkReadMessage(user,message_id)
    msg = Messages.objects.filter(id=message_id).filter(Q(from_user=user) | Q(to_user=user)).first()
    msg.save()
    msg.message
    msgsA = MessagesAnswer.objects.filter(answer_to=msg).order_by('-message__send_date')
    if msgsA != None:
        for msgA in msgsA:
            checkReadMessage(user,msgA.message.id)
            tempMsg = Messages.objects.filter(id=msgA.message.id).first()
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
        if MessagesAnswer.objects.filter(message=answer_to).exists():
            answer_to = MessagesAnswer.objects.filter(message=answer_to).first().answer_to
        msg =  Messages.objects.create(
                from_user = from_user,
                to_user = to_user,
                title = title,
                message = content,
                is_read = False,
                send_date = timezone.now()
            )
        msgAns = MessagesAnswer.objects.create(
            answer_to = answer_to,
            message = msg
        )
        transaction.savepoint_commit(sid)
        return True
    except :
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
            send_date = timezone.now()
        )
        transaction.savepoint_commit(sid)
        return True
    except:
        transaction.savepoint_rollback(sid)
        return False

def isNewMessages(user):
    if Messages.objects.filter(to_user=user).filter(is_read=False).exists():
        return True
    else:
        return False

def checkReadMessage(user, message_id):
    if Messages.objects.filter(to_user=user).filter(id=message_id).exists():
        msg = Messages.objects.filter(to_user=user).filter(id=message_id).first()
        msg.is_read = True
        msg.save()

def getAllReceiver(user):
    receiverList = []
    groups = Group.objects.filter(lecturer=user)
    for group in groups:
        studentGroups = StudentGroup.objects.filter(group=group)
        for studentGroup in studentGroups:
            receiverList.append({
                "student_id": studentGroup.student.id,
                "student_name": studentGroup.student.first_name + " " + studentGroup.student.last_name,
                "student_index": studentGroup.student.username [1:]
            })
    return receiverList

def getStudentDetailsToMsg(student_id):
    student = User.objects.filter(id=student_id).first()
    return {
        'id' : student.id,
        'name' : student.first_name + " " + student.last_name
    }

def getMessage(message_id):
    if Messages.objects.filter(id=message_id).exists():
        return Messages.objects.filter(id=message_id).first()
    else: 
        return None

def deletePermamentAllMessages(user):
    if Messages.objects.filter(Q(from_user=user) | Q(to_user=user)).exists():
        msgList = Messages.objects.filter(Q(from_user=user) | Q(to_user=user))
        for msg in msgList:
            deletePermamentMessageWithAnswers(msg)  

def deletePermamentMessageWithAnswers(message):
    if MessagesAnswer.objects.filter(answer_to = message).exists():
        msgAList = MessagesAnswer.objects.filter(answer_to = message)
        for msgA in msgAList:
            deletePermamentMessage(msgA.message)
    else:
        deletePermamentMessage(message)
    return True

def deletePermamentMessage(message):
    Messages.objects.filter(id=message.id).delete()

