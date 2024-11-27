import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';

class LearningMode extends StatelessWidget {
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
        title: Text('Mod de învățare'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: vowels.map((vowel) {
            return Padding(
              padding: const EdgeInsets.all(8.0),
              child: ElevatedButton(
                onPressed: () => _playSound(vowel),
                child: Text(
                  vowel,
                  style: TextStyle(fontSize: 24),
                ),
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}