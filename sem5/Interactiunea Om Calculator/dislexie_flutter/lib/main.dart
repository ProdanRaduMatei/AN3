import 'package:flutter/material.dart';
import 'learning_mode.dart';
import 'vowel_game.dart';
import 'matching_game.dart';
import 'voice_game.dart';
import 'drag_and_drop.dart';

void main() {
  runApp(DislexieApp());
}

class DislexieApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Dislexie App',
      theme: ThemeData(primarySwatch: Colors.teal),
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
      ),
      body: ListView(
        padding: EdgeInsets.all(16.0),
        children: [
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => LearningMode()));
            },
            child: Text('Mod de învățare'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => VowelGame()));
            },
            child: Text('Joacă un joc - Selectează vocala'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => MatchingGame()));
            },
            child: Text('Joacă un joc - Asociază cuvântul'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => VoiceGame()));
            },
            child: Text('Joacă un joc - Citește vocala cu vocea'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => DragAndDropGame()));
            },
            child: Text('Joacă un joc - Drag and Drop'),
          ),
        ],
      ),
    );
  }
}