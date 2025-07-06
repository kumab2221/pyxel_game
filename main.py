import pyxel
import random

class SnakeGame:
    def __init__(self):
        pyxel.init(160, 120, title="Snake Game")
        
        # ゲーム状態
        self.game_state = "playing"  # "playing", "game_over"
        
        # 蛇の初期設定
        self.snake = [(80, 60), (70, 60), (60, 60)]  # 頭から尻尾の順
        self.direction = (10, 0)  # 右向きで開始
        self.next_direction = (10, 0)
        
        # 食べ物
        self.food = self.generate_food()
        
        # スコア
        self.score = 0
        
        # ゲーム速度制御
        self.frame_count = 0
        self.move_interval = 8  # フレーム数（小さいほど速い）
        
        pyxel.run(self.update, self.draw)

    def generate_food(self):
        """食べ物をランダムな位置に生成（蛇の体と重ならない場所）"""
        while True:
            x = random.randint(1, 15) * 10
            y = random.randint(1, 11) * 10
            if (x, y) not in self.snake:
                return (x, y)

    def update(self):
        if self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            self.update_game_over()

    def update_playing(self):
        # キー入力処理
        if pyxel.btnp(pyxel.KEY_UP) and self.direction != (0, 10):
            self.next_direction = (0, -10)
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.direction != (0, -10):
            self.next_direction = (0, 10)
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.direction != (10, 0):
            self.next_direction = (-10, 0)
        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.direction != (-10, 0):
            self.next_direction = (10, 0)
        
        # フレームカウント更新
        self.frame_count += 1
        
        # 蛇の移動（一定間隔で）
        if self.frame_count >= self.move_interval:
            self.frame_count = 0
            self.direction = self.next_direction
            self.move_snake()

    def move_snake(self):
        # 新しい頭の位置
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # 壁との衝突チェック
        if (new_head[0] < 0 or new_head[0] >= 160 or 
            new_head[1] < 0 or new_head[1] >= 120):
            self.game_over()
            return
            
        # 自分の体との衝突チェック
        if new_head in self.snake:
            self.game_over()
            return
        
        # 新しい頭を追加
        self.snake.insert(0, new_head)
        
        # 食べ物を食べたかチェック
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # スコアが上がるたびに少し速くなる
            if self.move_interval > 3:
                self.move_interval = max(3, self.move_interval - 1)
        else:
            # 食べ物を食べていない場合、尻尾を削除
            self.snake.pop()

    def game_over(self):
        self.game_state = "game_over"

    def update_game_over(self):
        # リスタート
        if pyxel.btnp(pyxel.KEY_R):
            self.restart_game()
        # 終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def restart_game(self):
        self.game_state = "playing"
        self.snake = [(80, 60), (70, 60), (60, 60)]
        self.direction = (10, 0)
        self.next_direction = (10, 0)
        self.food = self.generate_food()
        self.score = 0
        self.frame_count = 0
        self.move_interval = 8

    def draw(self):
        pyxel.cls(0)  # 背景を黒でクリア
        
        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def draw_playing(self):
        # 蛇を描画
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # 頭は明るい緑
                pyxel.rect(x, y, 10, 10, 11)
            else:
                # 体は暗い緑
                pyxel.rect(x, y, 10, 10, 3)
        
        # 食べ物を描画（赤い四角）
        food_x, food_y = self.food
        pyxel.rect(food_x, food_y, 10, 10, 8)
        
        # スコア表示
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        
        # 操作説明
        pyxel.text(5, 110, "Arrow keys: Move", 6)

    def draw_game_over(self):
        # ゲームオーバー画面
        pyxel.text(50, 40, "GAME OVER", 8)
        pyxel.text(45, 55, f"Final Score: {self.score}", 7)
        pyxel.text(35, 75, "Press R to Restart", 11)
        pyxel.text(40, 85, "Press Q to Quit", 6)

# ゲーム開始
SnakeGame()