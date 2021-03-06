import requests
import json
import boto3
import middleware.context as context
import smtplib, ssl


class NotificationMiddlewareHandler:
    sns_client = None
    s_url = 'https://hooks.slack.com/services/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'

    def __init__(self):
        pass

    @staticmethod
    def notify(req, rsp):
        subscription = context.get_subscription()
        print("[notification.notify] req.path: ", req.path)
        if req.path in subscription and rsp.status_code == 201:
            # TODO: store email in session or run SQL query to get email
            notification_data = {
                'email': 'yk2822@columbia.edu',
                'data': {'id': req.form['id'],
                         'name': req.form['name'],
                         'addr': req.form['addr'],
                         'rest': req.form['rest'],
                         'max': req.form['max'],
                         'cur': req.form['cur']
                         }
            }

            print("[notification] req_data from POST: ", notification_data)

            # Publish to SNS topic
            req_data = json.dumps(notification_data)
            print('[notification before publish] req_data: ', req_data)

            client = NotificationMiddlewareHandler.get_sns_client()
            rsp = client.publish(TopicArn="arn:aws:sns:us-east-2:843691262496:mealSNS",
                                 Message=req_data)
            print('[notification.notify] after publish to SNS --> response.status_code = ', rsp['ResponseMetadata']['HTTPStatusCode'])

            # Send slack notification
            slack_data = json.dumps(
                {'text': req_data}).encode('utf-8')
            response = requests.post(
                NotificationMiddlewareHandler.s_url, data=slack_data,
                headers={'Content-Type': 'application/json'}
            )
            print("[notification.notify] slack.Response = ", response.status_code)

            # Send an Email confirmation
            print("[notification.notify] before email notification")
            if not NotificationMiddlewareHandler.notify_email(notification_data['email'], notification_data['data']):
                print("Error sending email notification")
            print("[notification.notify] after email notification")


    @classmethod
    def get_sns_client(cls):
        if NotificationMiddlewareHandler.sns_client is None:
            NotificationMiddlewareHandler.sns_client = boto3.client("sns", region_name="us-east-2")
        return NotificationMiddlewareHandler.sns_client


    @classmethod
    def notify_email(cls, rcver, msg):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_config = context.get_smtp_sender_config()
        sender_email = sender_config['sender']
        password = sender_config['password']

        test_msg = "[Success] Testing email notification for Meal Microservice!"

        # Create a secure SSL context
        ctext = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls(context=ctext)  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, rcver, test_msg)
        except Exception as e:
            print(e)
            return False
        finally:
            server.quit()

        return True

