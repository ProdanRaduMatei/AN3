import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';

class MatchingGame extends StatelessWidget {
  final AudioPlayer _audioPlayer = AudioPlayer();
  final Map<String, List<String>> words = {
    'A': ['Ana', 'aer'],
    'E': ['Elena', 'energie'],
    'I': ['India', 'inel'],
    'O': ['Oscar', 'ochi'],
    'U': ['Ungaria', 'urs']
  };

  void _playSound(String file) async {
    final filePath = 'assets/sounds/$file.mp3';
    await _audioPlayer.play(AssetSource(filePath));
  }

  void _checkMatch(String vowel, String word, Function onMatch) {
    if (word.startsWith(vowel)) {
      _playSound('correct');
      onMatch();
    } else {
      _playSound('wrong');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Asociază cuvântul'),
      ),
      body: Center(
        child: ListView.builder(
          itemCount: words.length,
          itemBuilder: (context, index) {
            String vowel = words.keys.elementAt(index);
            return ExpansionTile(
              title: Text(vowel, style: TextStyle(fontSize: 24)),
              children: words[vowel]!.map((word) {
                return ListTile(
                  title: Text(word),
                  onTap: () => _checkMatch(vowel, word, () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Bravo!')),
                    );
                  }),
                );
              }).toList(),
            );
          },
        ),
      ),
    );
  }
}