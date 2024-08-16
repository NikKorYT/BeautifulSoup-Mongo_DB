import pika
import json
from mongoengine import connect
import configparser
from models import users


# read config file for DB key safety
config = configparser.ConfigParser()
config.read("configs/config.ini")

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
domain = config.get("DB", "domain")


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    #save the user_id from the message to the variable
    user_id = message["user_id"]
    #call the function that sends email to the user
    send_email_to_user(user_id)


channel.basic_consume(queue="task_queue", on_message_callback=callback)


# function immitating that email has been send to the customer with recieved user_id
# also updates the message_sent_status to True
def send_email_to_user(user_id):
    user = users.objects(id=user_id).first()
    if user is None:
        print(f"No user found with id {user_id}")
        return
    user.message_sent_status = True
    user.save()
    print(f"Email sent to {user.name} with email {user.email}")


if __name__ == "__main__":
    # check connection to DB
    try:
        connect(
            host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority""",
            ssl=True,
        )
        print("Connected to DB")
    except Exception as e:
        print("Error: ", e)
    try:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Thanks for using our service!")
        connection.close()
