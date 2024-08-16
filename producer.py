import pika
import faker
from mongoengine import connect
import configparser
from models import users
import json

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="task_mock", exchange_type="direct")
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_bind(exchange="task_mock", queue="task_queue")


# read config file for DB key safety
config = configparser.ConfigParser()
config.read("configs/config.ini")

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
domain = config.get("DB", "domain")

def seed_users():
    fake = faker.Faker()
    for user in range(20):
        user = users(
            name = fake.name(),
            email = fake.email(),
            message_sent_status = False
        )
        user.save()
    print("Users seeded!")

def clear_users():
    users.objects().delete()
    print("Users cleared!")

# get object ids of every created user from db and send them to the queue
def send_users_to_queue():
    users_list = users.objects()
    print(f"Number of users in DB: {len(users_list)}")
    for user in users_list:
        message = {"user_id": str(user.id)}
        channel.basic_publish(
            exchange="task_mock",
            routing_key="task_queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f" [x] Sent {message}")

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
    clear_users()
    seed_users()
    send_users_to_queue()
