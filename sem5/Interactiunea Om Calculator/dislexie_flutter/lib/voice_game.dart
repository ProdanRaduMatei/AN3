import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class VoiceGame extends StatefulWidget {
  @override
  _VoiceGameState createState() => _VoiceGameState();
}

class _VoiceGameState extends State<VoiceGame> {
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = '';
  String currentVowel = 'A';

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  void _startListening() async {
    bool available = await _speech.initialize();
    if (available) {
      setState(() => _isListening = true);
      _speech.listen(onResult: (result) {
        setState(() {
          _text = result.recognizedWords.toUpperCase();
          if (_text == currentVowel) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Bravo! Ai citit corect!')),
            );
          }
        });
      });
    }
  }

  void _stopListening() {
    _speech.stop();
    setState(() => _isListening = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Citește vocala'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Citește vocala: $currentVowel', style: TextStyle(fontSize: 24)),
            ElevatedButton(
              onPressed: _isListening ? _stopListening : _startListening,
              child: Text(_isListening ? 'Oprește' : 'Ascultă'),
            ),
            Text('Ai spus: $_text', style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}