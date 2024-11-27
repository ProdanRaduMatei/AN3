import 'package:flutter/material.dart';

class DragAndDropGame extends StatefulWidget {
  @override
  _DragAndDropGameState createState() => _DragAndDropGameState();
}

class _DragAndDropGameState extends State<DragAndDropGame> {
  final List<String> vowels = ['A', 'E', 'I', 'O', 'U']; // Lista de vocale
  final Map<String, String> basketMapping = {}; // Coșurile și vocalele asociate
  int score = 0;

  @override
  void initState() {
    super.initState();
    _generateBaskets();
  }

  void _generateBaskets() {
    for (var vowel in vowels) {
      basketMapping[vowel] = ''; // Inițial, coșurile sunt goale
    }
  }

  void _checkPlacement(String vowel, String basket) {
    if (vowel == basket) {
      setState(() {
        score++;
        basketMapping[basket] = vowel;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bravo! Ai plasat corect!')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Mai încearcă! Vocala nu corespunde coșului.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Joacă - Drag and Drop'),
      ),
      body: Column(
        children: [
          Expanded(
            flex: 1,
            child: Center(
              child: Text(
                'Trage vocalele în coșul corect!',
                style: TextStyle(fontSize: 24),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: vowels.map((basket) {
                return DragTarget<String>(
                  builder: (context, candidateData, rejectedData) {
                    return Container(
                      width: 100,
                      height: 100,
                      decoration: BoxDecoration(
                        color: basketMapping[basket] == basket
                            ? Colors.green
                            : Colors.teal,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Center(
                        child: Text(
                          basket,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    );
                  },
                  onAccept: (vowel) {
                    _checkPlacement(vowel, basket);
                  },
                );
              }).toList(),
            ),
          ),
          Expanded(
            flex: 3,
            child: Center(
              child: Wrap(
                spacing: 16,
                runSpacing: 16,
                children: vowels.map((vowel) {
                  return Draggable<String>(
                    data: vowel,
                    feedback: Material(
                      color: Colors.transparent,
                      child: Container(
                        width: 80,
                        height: 80,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: Colors.orange,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          vowel,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                    childWhenDragging: Container(
                      width: 80,
                      height: 80,
                      decoration: BoxDecoration(
                        color: Colors.grey,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Center(
                        child: Text(
                          vowel,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                    child: Container(
                      width: 80,
                      height: 80,
                      decoration: BoxDecoration(
                        color: Colors.blue,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Center(
                        child: Text(
                          vowel,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
          Expanded(
            flex: 1,
            child: Center(
              child: Text(
                'Scor: $score',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }
}