import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'api_service.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? latestDHT;
  Map<String, dynamic>? latestPIR;
  Map<String, dynamic>? latestSound;
  Map<String, dynamic>? latestAirQuality;
  String? latestImageUrl; // 📌 Stocke l'URL de l'image la plus récente

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      var dhtData = await ApiService.fetchSensorDHT();
      var pirData = await ApiService.fetchSensorPIR();
      var soundData = await ApiService.fetchSensorSound();
      var airQualityData = await ApiService.fetchSensorAirQuality();
      var imageUrl = await ApiService.fetchLatestImage();

      setState(() {
        latestDHT = dhtData.isNotEmpty ? dhtData.last : null;
        latestPIR = pirData.isNotEmpty ? pirData.last : null;
        latestSound = soundData.isNotEmpty ? soundData.last : null;
        latestAirQuality =
            airQualityData.isNotEmpty ? airQualityData.last : null;
        latestImageUrl = imageUrl; // 📌 Mise à jour de l'URL de l'image
      });
    } catch (e) {
      print("Erreur lors de la récupération des données : $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Tableau de Bord des Capteurs"),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed:
                fetchData, // 📌 Rafraîchir les données en appuyant sur le bouton
          ),
        ],
      ),
      body: Column(
        children: [
          // 📌 Affichage des capteurs sous forme de cartes
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Wrap(
              spacing: 10,
              runSpacing: 10,
              children: [
                _buildSensorCard(
                    "Température", latestDHT?["temperature"] ?? "N/A", "°C"),
                _buildSensorCard(
                    "Humidité", latestDHT?["humidity"] ?? "N/A", "%"),
                _buildSensorCard("Qualité de l'air",
                    latestAirQuality?["co2"] ?? "N/A", "ppm"),
                _buildSensorCard("Son", latestSound?["Sound"] ?? "N/A", "dB"),
                _buildSensorCard(
                    "Mouvement", latestPIR?["move"] == 1 ? "Oui" : "Non", ""),
              ],
            ),
          ),

          // 📌 Affichage de l'image la plus récente
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: _buildLatestImage(),
            ),
          ),
        ],
      ),
    );
  }

  // 📌 Widget pour afficher une carte d'information capteur
  Widget _buildSensorCard(String type, dynamic valeur, String unite) {
    return Container(
      width: 150,
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.blueGrey[800],
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(type,
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          SizedBox(height: 10),
          Text("$valeur $unite",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  // 📌 Widget pour afficher la dernière image capturée
  Widget _buildLatestImage() {
    return Card(
      color: Colors.blueGrey[900],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text("Dernière Image Capturée",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            latestImageUrl != null
                ? Image.network(latestImageUrl!) // 📌 Affichage de l'image
                : Text("Aucune image disponible",
                    style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
