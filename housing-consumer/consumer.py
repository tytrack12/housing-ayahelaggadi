from confluent_kafka import Consumer, KafkaException
import json
import requests

def main():
    conf = {
        'bootstrap.servers': 'broker:9092',  # ou 'localhost:29092' si tu es hors conteneur
        'group.id': 'housing_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe(['housing_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            data = json.loads(msg.value().decode('utf-8'))
            print("Message reçu :", data)

            # Optionnel : envoyer à l'API
            r = requests.post("http://api:8000/houses", json=data)
            print("Réponse API :", r.status_code)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
