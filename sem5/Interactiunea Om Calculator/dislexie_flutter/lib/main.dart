import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';

void main() {
  runApp(DislexieApp());
}

class DislexieApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: MainMenu(),
    );
  }
}

class MainMenu extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dislexie App'),
        backgroundColor: Colors.teal,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => LearnVowelsScreen()),
                );
              },
              child: Text('Învățăm Vocalele'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => VowelGameScreen()),
                );
              },
              child: Text('Joc Interactiv Vocale'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => PlayLockedMessageScreen()),
                );
              },
              child: Text('Mesaj Blocare'),
            ),
          ],
        ),
      ),
    );
  }
}

class LearnVowelsScreen extends StatelessWidget {
  final AudioPlayer _audioPlayer = AudioPlayer();

  void _playSound(String vowel) async {
    final filePath = 'assets/sounds/$vowel.mp3';
    await _audioPlayer.play(AssetSource(filePath));
  }

  @override
  Widget build(BuildContext context) {
    final vowels = ['A', 'E', 'I', 'O', 'U'];

    return Scaffold(
      appBar: AppBar(
        title: Text('Învățăm Vocalele'),
        backgroundColor: Colors.teal,
      ),
      body: Container(
        color: Color(0xFFE0F7FA),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: vowels.map((vowel) {
              return Padding(
                padding: const EdgeInsets.all(8.0),
                child: ElevatedButton(
                  onPressed: () => _playSound(vowel),
                  child: Text(
                    vowel,
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.teal[300],
                    padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  ),
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}

class VowelGameScreen extends StatefulWidget {
  @override
  _VowelGameScreenState createState() => _VowelGameScreenState();
}

class _VowelGameScreenState extends State<VowelGameScreen> {
  final AudioPlayer _audioPlayer = AudioPlayer();
  final List<String> vowels = ['A', 'E', 'I', 'O', 'U'];
  String? correctAnswer;

  @override
  void initState() {
    super.initState();
    _setNewQuestion();
  }

  void _setNewQuestion() {
    setState(() {
      correctAnswer = (vowels..shuffle()).first;
    });
  }

  void _playCorrectSound() async {
    await _audioPlayer.play(AssetSource('assets/sounds/correct.mp3'));
  }

  void _playWrongSound() async {
    await _audioPlayer.play(AssetSource('assets/sounds/wrong.mp3'));
  }

  void _checkAnswer(String answer) {
    if (answer == correctAnswer) {
      _playCorrectSound();
      _setNewQuestion();
    } else {
      _playWrongSound();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Joc Interactiv Vocale'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Selectează litera: $correctAnswer',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            ...vowels.map((vowel) {
              return ElevatedButton(
                onPressed: () => _checkAnswer(vowel),
                child: Text(
                  vowel,
                  style: TextStyle(fontSize: 24),
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }
}

class PlayLockedMessageScreen extends StatelessWidget {
  final AudioPlayer _audioPlayer = AudioPlayer();

  void _playLockedMessage() async {
    final filePath = 'assets/sounds/locked_message.mp3';
    await _audioPlayer.play(AssetSource(filePath));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Mesaj Blocare'),
        backgroundColor: Colors.redAccent,
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: _playLockedMessage,
          child: Text('Redă Mesaj Blocare'),
        ),
      ),
    );
  }
}