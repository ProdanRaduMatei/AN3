import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:math';

class VowelGame extends StatefulWidget {
  @override
  _VowelGameState createState() => _VowelGameState();
}

class _VowelGameState extends State<VowelGame> {
  final AudioPlayer _audioPlayer = AudioPlayer();
  final Random _random = Random();
  final List<String> vowels = ['A', 'E', 'I', 'O', 'U'];
  String? currentVowel;
  int score = 0;

  void _playSound(String file) async {
    final filePath = 'assets/sounds/$file.mp3';
    await _audioPlayer.play(AssetSource(filePath));
  }

  void _generateQuestion() {
    setState(() {
      currentVowel = vowels[_random.nextInt(vowels.length)];
    });
  }

  void _checkAnswer(String answer) {
    if (answer == currentVowel) {
      score++;
      _playSound('correct');
    } else {
      _playSound('wrong');
    }
    _generateQuestion();
  }

  @override
  void initState() {
    super.initState();
    _generateQuestion();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Selectează vocala'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Alege vocala: $currentVowel',
              style: TextStyle(fontSize: 24),
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
            Text('Scor: $score', style: TextStyle(fontSize: 20)),
          ],
        ),
      ),
    );
  }
}