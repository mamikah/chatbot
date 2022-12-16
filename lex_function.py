# import osSS
# import sys
                               
# import pymysql
# from aws_lambda_powertools import Logger
# from aws_lambda_powertools.utilities.typing import LambdaContext
 
# DB_HOST = os.environ["DB_ENDPOINT"]
# DB_USER = os.environ["DB_USER"]
# DB_PASSWORD = os.environ["DB_PASSWORD"]
# DB_NAME = os.environ["DB_NAME"]
 
# logger = Logger(level='INFO', service=__name__)
 

# @logger.inject_lambda_context()
# def handler(event=None, context=LambdaContext):
#     try:
#         # RDS Proxyに接続
#         connect = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, connect_timeout=5)
#         with connect.cursor() as cursor:
#             cursor.execute("select * from sample")
#             result = cursor.fetchall()
#             # selectのみなので、commit()は不要
#             # conn.commit()
#             logger.info(result)
#         connect.close()
#     except pymysql.MySQLError as e:
#         logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
#         logger.error(e)
#         sys.exit()
#     except Exception:
#         logger.error("ERROR: Unexpected error: Could not get value")
#         sys.exit()
 
#     return result
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

    global JankenCount

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

                text = "実行できませんでした。最初からやり直してください。"

            else:

                text = "商品を追加しました"

            message =  {

                    'contentType': 'PlainText',

                    'content': text

            }

            fulfillment_state = "Fulfilled"    

            session_attributes = get_session_attributes(event)

            return close(event, session_attributes, fulfillment_state, message)

           

    elif str(intent_name) == "delete": # 削除インテントの場合

        if none_list != []: # 空きスロットがある時

            session_attributes = get_session_attributes(event)

            text = "削除する商品を送信してください"

            message =  {

                'contentType': 'PlainText',

                'content': text

            }

        else: # スロットが全て埋まっている場合

            delshohin = int(get_slot(event, "delshohin")) # ユーザ入力を取得

            text = '削除しました'

            message =  {

                    'contentType': 'PlainText',

                    'content': text

                }

            fulfillment_state = "Fulfilled"

            session_attributes = get_session_attributes(event)

            return close(event, session_attributes, fulfillment_state, message)



    elif str(intent_name) == "display": # 表示インテントの場合

            session_attributes = get_session_attributes(event)

            # データベースの処理

            text = "" # データベースの結果を書く

            message =  {

                'contentType': 'PlainText',

                'content': text

            }

            fulfillment_state = "Fulfilled"

            session_attributes = get_session_attributes(event)

            return close(event, session_attributes, fulfillment_state, message)