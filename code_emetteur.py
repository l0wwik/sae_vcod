import paho.mqtt.client as mqtt
import time
import picamera
import json
from lib.sensorPIR import sensorPIR
from lib.sensorDHT import sensorDHT
from lib.sensorSound import sensorSound
from lib.sensorAirquality import sensorAirquality
 
# Configuration MQTT
SERVEUR = "192.168.8.5" # Adresse IP du broker MQTT
MQTT_IMAGE_TOPIC = "station04/sensor/image"
CHUNK_SIZE = 4096 # 4 Ko par chunk
INTERVAL = 3 # Intervalle entre chaque envoi de données
IMAGE_PATH = "/home/pi/captured_image.jpg"
 
# Initialisation des capteurs
DHTSensor = sensorDHT.GroveDHTSensor(26)
SoundSensor = sensorSound.GroveSoundSensor(0)
airQualitySensor = sensorAirquality.GroveAirQualitySensor()
PIRsensor = sensorPIR.GrovePirMotionSensor(18)
 
# Données des capteurs
sensor_data_DHT = {'temperature': 0, 'humidity': 0}
sensor_data_PIR = {'move': 0}
sensor_data_Sound = {'Sound': 0}
sensor_data_Airquality = {'TVoC': 0, 'co2': 0}
 
# Connexion MQTT
client = mqtt.Client()
client.connect(SERVEUR, 1883, 60)
client.loop_start()
 
def capture_image():
    """Prend une photo avec la caméra du Raspberry Pi"""
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480) # Ajuste la résolution si nécessaire
        time.sleep(5) # Laisse le capteur s'ajuster
        camera.capture(IMAGE_PATH)
        print("📷 Photo capturée")
 
def send_image():
    """Envoie l'image en chunks via MQTT"""
    with open(IMAGE_PATH, "rb") as img_file:
        chunk_id = 0
        chunk = img_file.read(CHUNK_SIZE) # Lire le premier chunk
        while chunk: # Tant que des données existent
            payload = f"{chunk_id}|".encode() + chunk
            client.publish(MQTT_IMAGE_TOPIC, payload)
            chunk_id += 1
            chunk = img_file.read(CHUNK_SIZE) # Lire le chunk suivant
 
    # Envoyer un message de fin de transmission
    client.publish(MQTT_IMAGE_TOPIC, "END".encode())
    print("📤 Image envoyée avec succès !")
 
try:
    while True:
        # Récupération des valeurs des capteurs
        DHTSensor.getRawSensorValue()
        airQualitySensor.getRawSensorValue()
        move = PIRsensor.getSensorValue()
 
        TVoC = airQualitySensor.TVoC()
        co2 = airQualitySensor.CO2eq()
        humidity = int(DHTSensor.humidity())
        temperature = int(DHTSensor.temperature())
        sound = SoundSensor.getRawSensorValue()
 
        # Mise à jour des données
        sensor_data_DHT['temperature'] = temperature
        sensor_data_DHT['humidity'] = humidity
        sensor_data_Sound['Sound'] = sound
        sensor_data_Airquality['TVoC'] = TVoC
        sensor_data_Airquality['co2'] = co2
        sensor_data_PIR['move'] = move
 
        # Envoi des données via MQTT
        client.publish('station04/sensor/DHT', json.dumps(sensor_data_DHT), 1)
        client.publish('station04/sensor/Sound', json.dumps(sensor_data_Sound), 1)
        client.publish('station04/sensor/Airquality', json.dumps(sensor_data_Airquality), 1)
        client.publish('station04/sensor/PIR', json.dumps(sensor_data_PIR), 1)
 
        print("📡 Données des capteurs envoyées")
 
        # Capture et envoi de la photo si un mouvement est détecté
        if move:
            print("🚨 Mouvement détecté ! Capture et envoi de l'image...")
            capture_image()
            send_image()
 
        # Pause avant la prochaine lecture
        time.sleep(INTERVAL)
 
except KeyboardInterrupt:
    print("❌ Fin de la diffusion")
 
client.loop_stop()
client.disconnect()