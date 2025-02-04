import paho.mqtt.client as mqtt

# Configuration du broker
BROKER = "192.168.214.5"  # Remplace par l'IP de ton serveur Linux
PORT = 1883
TOPIC = "station04/sensor/+"

# Fonction appelée lorsqu'une connexion au broker est établie
def on_connect(client, userdata, flags, rc):
    print(f"Connecté avec le code de résultat {rc}")
    # S'abonner au topic
    client.subscribe(TOPIC)

# Fonction appelée lorsqu'un message est reçu sur le topic
def on_message(client, userdata, msg):
    print(f"Message reçu : {msg.payload.decode()}")

# Créer un client MQTT
client = mqtt.Client()

# Définir les fonctions de rappel (callback)
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(BROKER, PORT, 60)

# Boucle pour écouter les messages entrants
client.loop_forever()
