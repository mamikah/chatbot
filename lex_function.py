def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']


def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None   


def get_none_slot_list(d):
    return [k for k, v in d.items() if v == None]


def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}


def elicit_slot(intent_request, session_attributes, slot, message):
    return {
        'sessionState': {
            "activeContexts": [
                {
                    "name": "slot",
                    "contextAttributes": {
                        "last": slot
                    },
                    "timeToLive": {
                        "timeToLiveInSeconds": 20,
                        "turnsToLive": 20
                    }
                }
            ],
            'dialogAction': {
                'slotToElicit': slot,
                'type': 'ElicitSlot'
            },
            "intent": {
            "name": intent_request['sessionState']['intent']['name'],
            "slots": intent_request['sessionState']['intent']['slots']
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None, 
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def lambda_handler(event, context):
    print(event)
    intent_name = event['sessionState']['intent']['name'] # インテント名取得
    slots = get_slots(event)
    none_list = get_none_slot_list(slots) # 空きスロットのリスト取得
    
    if str(intent_name) == "add": # 追加インテントの場合
        if len(none_list) == 2: # 空きスロットが2個の時
            session_attributes = get_session_attributes(event)
            text = "商品を追加してください"
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        elif len(none_list) == 1:
            session_attributes = get_session_attributes(event)
            text = "賞味・消費期限の日付を追加してください"
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        else:
            try:
                shohin = str(get_slot(event, "addition")) # ユーザ入力を取得
                timelimit = str(get_slot(event, "timelimit"))

            except:
                text = "適切な名前を入れてください"
            else:
                text = "商品を追加しました"
            JankenCount = 0
            message =  {
                    'contentType': 'PlainText',
                    'content': text
            }
            fulfillment_state = "Fulfilled"    
            session_attributes = get_session_attributes(event)
            return close(event, session_attributes, fulfillment_state, message)
            
    elif str(intent_name) == "Uranai": # 占いインテントの場合
        pass
        
    