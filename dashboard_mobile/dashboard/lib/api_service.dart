import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl =
      "http://localhost:5000"; // 📌 Assure-toi que l'API tourne

  // 📌 Récupérer les données des capteurs DHT
  static Future<List<dynamic>> fetchSensorDHT() async {
    final response = await http.get(Uri.parse("$baseUrl/sensor_dht"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erreur lors de la récupération des données DHT");
    }
  }

  // 📌 Récupérer les données des capteurs PIR
  static Future<List<dynamic>> fetchSensorPIR() async {
    final response = await http.get(Uri.parse("$baseUrl/sensor_pir"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erreur lors de la récupération des données PIR");
    }
  }

  // 📌 Récupérer les données des capteurs Son
  static Future<List<dynamic>> fetchSensorSound() async {
    final response = await http.get(Uri.parse("$baseUrl/sensor_sound"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erreur lors de la récupération des données Son");
    }
  }

  // 📌 Récupérer les données des capteurs de Qualité de l'Air
  static Future<List<dynamic>> fetchSensorAirQuality() async {
    final response = await http.get(Uri.parse("$baseUrl/sensor_air_quality"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erreur lors de la récupération des données Air Quality");
    }
  }

  // 📌 Récupérer l'URL de la dernière image stockée
  static Future<String?> fetchLatestImage() async {
    final response = await http.get(Uri.parse("$baseUrl/images"));

    if (response.statusCode == 200) {
      List<dynamic> images = jsonDecode(response.body);
      if (images.isNotEmpty) {
        return images
            .last['image_path']; // 📌 Récupère le chemin de la dernière image
      }
    }
    return null;
  }
}
