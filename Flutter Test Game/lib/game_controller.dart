import 'dart:math';
import 'dart:ui';

import 'package:flame/flame.dart';
import 'package:flame/game.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_game/components/healh_bar.dart';
import 'package:flutter_game/components/highscore_text.dart';
import 'package:flutter_game/components/score_text.dart';
import 'package:flutter_game/components/start_text.dart';
import 'package:flutter_game/enemy_spawner.dart';
import 'package:flutter_game/game_state.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'components/enemy.dart';
import 'components/player.dart';

// brain of game: contains instance variables and logic, display on screen with render method, update game using update method (takes no time), resize to set size of screen

class GameController extends Game {
  final SharedPreferences storage;
  Random rand;
  Size screenSize; //dimensions of screen
  double
      tileSize; //smaller portion of screen (move at same speed regardless of size)
  Player player;
  EnemySpawner enemySpawner;
  List<Enemy> enemies;
  HealthBar healthBar;
  int score;
  ScoreText scoreText;
  GameState state;
  HighscoreText highscoreText;
  StartText startText;

  GameController(this.storage) {
    initialize();
  }

  void initialize() async {
    resize(await Flame.util.initialDimensions());
    state = GameState.menu;
    rand = Random();
    player = Player(this);
    enemies = List<Enemy>();
    enemySpawner = EnemySpawner(this);
    healthBar = HealthBar(this);
    score = 0;
    scoreText = ScoreText(this);
    highscoreText = HighscoreText(this);
    startText = StartText(this);
  }

  // order matters with rendering
  void render(Canvas c) {
    Rect background = Rect.fromLTWH(0, 0, screenSize.width, screenSize.height);
    Paint backgroundPaint = Paint()..color = Color(0xFFFAFAFA);
    c.drawRect(background, backgroundPaint);

    player.render(c);

    if (state == GameState.menu) {
      startText.render(c);
      highscoreText.render(c);
    } else {
      enemies.forEach((Enemy enemy) => enemy.render(c));
      scoreText.render(c);
      healthBar.render(c);
    }
  }

  void update(double t) {
    if (state == GameState.menu) {
      startText.update(t);
      highscoreText.update(t);
    } else if (state == GameState.playing) {
      enemySpawner.update(t);
      enemies.forEach((Enemy enemy) => enemy.update(t));
      enemies.removeWhere((Enemy enemy) => enemy.isDead);
      player.update(t);
      scoreText.update(t);
      healthBar.update(t);
    }
  }

  void resize(Size size) {
    screenSize = size;
    tileSize = screenSize.width / 10; //tile size is 1/10 the width
  }

  void onTapDown(TapDownDetails d) {
    if (state == GameState.menu) {
      state = GameState.playing;
    } else if (state == GameState.playing) {
      enemies.forEach((Enemy enemy) {
        if (enemy.enemyRect.contains(d.globalPosition)) {
          enemy.onTapDown();
        }
      });
    }
  }

  void spawnEnemy() {
    double x, y;
    switch (rand.nextInt(4)) {
      case 0:
        // Top
        x = rand.nextDouble() * screenSize.width;
        y = -tileSize * 2.5;
        break;
      case 1:
        // Right
        x = screenSize.width + tileSize * 2.5;
        y = rand.nextDouble() * screenSize.height;
        break;
      case 2:
        // Bottom
        x = rand.nextDouble() * screenSize.width;
        y = screenSize.height + tileSize * 2.5;
        break;
      case 3:
        // Left
        x = -tileSize * 2.5;
        y = rand.nextDouble() * screenSize.height;
        break;
    }
    enemies.add(Enemy(this, x, y));
  }
}
