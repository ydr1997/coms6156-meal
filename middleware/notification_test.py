from notification import NotificationMiddlewareHandler
import json

def t_sns_1():
    sns = NotificationMiddlewareHandler.get_sns_client()
    print("Got SNS Client!")
    tps = NotificationMiddlewareHandler.get_sns_topics()
    print("SNS Topics = \n", json.dumps(tps, indent=2))

    message = {"msg": "new participant signed up to join the meal"}
    NotificationMiddlewareHandler.send_sns_message(
        "arn:aws:sns:us-east-2:843691262496:mealSNS",           # updated sns for meal-sns
        message
    )