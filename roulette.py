import tkinter as tk
import random
import time

class VerticalRoulette:
    def __init__(self, root):
        self.root = root
        self.root.title("ルーレット")
        self.root.geometry("600x500")
        self.root.configure(bg="#2C3E50")
        
        # ルーレットに表示する項目
        self.items = [
            "+90 kg", "-70 kg", "+70 kg", "-90 kg", "+80 kg", 
            "-60 kg", "+60 kg", "-80 kg", "+50 kg", "-50 kg"
        ]
        
        # 当選アイテム
        self.winning_item = "+90 kg"
        
        # フレームの作成
        self.control_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=20)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.display_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=20)
        self.display_frame.pack(expand=True, fill=tk.BOTH)
        
        # コントロール要素        
        self.spin_button = tk.Button(self.control_frame, text="回転開始", command=self.start_spin, 
                                    bg="#E74C3C", fg="white", font=("Arial", 14, "bold"), 
                                    width=10, height=1)
        self.spin_button.pack(pady=10)
        
        # 表示要素
        self.canvas = tk.Canvas(self.display_frame, bg="#34495E", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # 中央の選択マーカー (画像のように少し暗い背景色と白枠)
        self.canvas.create_rectangle(0, 220, 600, 280, fill="#2C3E50", outline="white", width=2)
        
        # 現在表示中の項目
        self.current_items = []
        self.item_widgets = []
        
        # 初期表示（ランダムな項目を表示）
        self.initialize_display()
        
        # アニメーション関連
        self.is_spinning = False
        self.animation_id = None
        self.speed = 30  # ミリ秒ごとに更新
    
    def initialize_display(self):
        # 項目をランダムに配置（ただし+90kgは含まない）
        items_without_winner = [item for item in self.items if item != self.winning_item]
        random.shuffle(items_without_winner)
        
        # 表示する5つの項目
        self.current_items = []
        for i in range(5):
            if i == 2:  # 中央位置
                self.current_items.append(random.choice(items_without_winner))
            else:
                self.current_items.append(random.choice(items_without_winner))
        
        self.update_display()
    
    def update_display(self):
        # 古い項目を削除
        for widget in self.item_widgets:
            self.canvas.delete(widget)
        
        self.item_widgets = []
        
        # 新しい項目を描画
        for i, item in enumerate(self.current_items):
            y_pos = 130 + i * 60
            
            # 色を決定（+はピンク、-は青）
            if "+" in item:
                color = "#FF69B4"  # ピンク
            else:
                color = "#1E90FF"  # 青
            
            # テキストを追加
            widget = self.canvas.create_text(300, y_pos, text=item, fill=color, font=("Arial", 36, "bold"))
            self.item_widgets.append(widget)
    
    def shift_items_up(self):
        # 項目を上に移動（項目が下から上に移動する）
        item_to_remove = self.current_items[0]
        self.current_items = self.current_items[1:]
        
        # 新しい項目を追加（通常は完全ランダムだが、+90kgが出るまで）
        items_without_winner = [item for item in self.items if item != self.winning_item]
        
        # 中央に+90kgがある場合、回転を停止する条件をチェック
        if self.current_items[1] == self.winning_item:
            self.stop_spinning()
            return
            
        # ランダムな項目を追加（ただし一定確率で+90kgにする）
        if not self.is_spinning or random.random() < 0.1:  # 10%の確率で+90kgを追加
            new_item = self.winning_item
        else:
            new_item = random.choice(items_without_winner)
        
        self.current_items.append(new_item)
        self.update_display()
    
    def start_spin(self):
        if self.is_spinning:
            return
            
        self.is_spinning = True
        self.spin_button.config(state=tk.DISABLED)
        
        # リストをリセット（ただし+90kgは含まない）
        items_without_winner = [item for item in self.items if item != self.winning_item]
        random.shuffle(items_without_winner)
        
        # 初期表示を設定
        self.current_items = []
        for i in range(5):
            self.current_items.append(random.choice(items_without_winner))
        
        self.update_display()
        self.animate_spin()
    
    def animate_spin(self):
        if not self.is_spinning:
            return
            
        # 項目を一つ上にシフト
        self.shift_items_up()
        
        # 次のフレームのアニメーション
        self.animation_id = self.root.after(self.speed, self.animate_spin)
    
    def stop_spinning(self):
        # アニメーションを停止し、+90kgが中央に来るようにする
        self.is_spinning = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            
        # +90kgが中央に表示されるように調整
        if self.current_items[1] != self.winning_item:
            self.current_items[1] = self.winning_item
            self.update_display()
            
        self.spin_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = VerticalRoulette(root)
    root.mainloop()