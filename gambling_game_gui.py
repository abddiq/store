import tkinter as tk
from tkinter import messagebox
import random

ROULETTE_NUMBERS = list(range(37))
RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

class RouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("روليت")
        self.root.geometry("400x300")
        self.player_name = ""
        self.balance = 0
        self.build_game()

    def build_game(self):
        tk.Label(self.root, text="روليت", font=("Arial", 24, "bold")).pack(pady=14)
        info_fr = tk.Frame(self.root)
        info_fr.pack(pady=7, fill="x")
        self.info_lbl = tk.Label(info_fr, text=f" اللاعب: {self.player_name}    |    الرصيد: {self.balance}$", font=("Arial", 14, "bold"))
        self.info_lbl.pack(pady=4)
        bet_fr = tk.LabelFrame(self.root, text="خيارات الرهان", font=("Arial", 13, "bold"))
        bet_fr.pack(padx=16, pady=8)
        tk.Label(bet_fr, text="مبلغ الرهان:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=6, sticky="e")
        self.bet_var = tk.StringVar(value="10")
        tk.Entry(bet_fr, textvariable=self.bet_var, font=("Arial", 12), width=8, justify="center").grid(row=0, column=1, padx=5, pady=6)
        self.bet_type = tk.StringVar(value="even")
        choices = [
            (" رقم محدد", "number"), (" أحمر", "red"), (" أسود", "black"), (" زوجي", "even"),
            (" فردي", "odd"), (" صفر", "zero"), (" عشرات 1-12", "dozen1"), (" عشرات 13-24", "dozen2"), (" عشرات 25-36", "dozen3")
        ]
        self.number_var = tk.StringVar(value="0")
        bets_frm = tk.Frame(bet_fr)
        bets_frm.grid(row=1, column=0, columnspan=4, pady=3)
        for i, (txt, val) in enumerate(choices):
            tk.Radiobutton(bets_frm, text=txt, variable=self.bet_type, value=val, font=("Arial", 11)).grid(row=0, column=i, padx=2, pady=2)
        tk.Label(bets_frm, text="رقم:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=2)
        tk.Entry(bets_frm, textvariable=self.number_var, font=("Arial", 11), width=5, justify="center").grid(row=1, column=1, pady=2)
        tk.Button(bet_fr, text=" دُر الروليت!", font=("Arial", 14, "bold"), command=self.play_round).grid(row=2, column=0, columnspan=4, pady=9)
        self.result_lbl = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.result_lbl.pack(pady=8)
        btn_fr = tk.Frame(self.root)
        btn_fr.pack(pady=8)
        tk.Button(btn_fr, text=" خروج", font=("Arial", 12), command=self.root.destroy).pack(side="left", padx=10)

    def play_round(self):
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.result_lbl.config(text="أدخل مبلغ صحيح!")
            return
        if bet <= 0:
            self.result_lbl.config(text="الرهان يجب أن يكون أكبر من صفر!")
            return
        if bet > self.balance:
            self.result_lbl.config(text="لا يوجد رصيد كافٍ!")
            return
        self.last_bet = bet
        btype = self.bet_type.get()
        number = int(self.number_var.get()) if btype == "number" else None
        result = random.SystemRandom().choice(ROULETTE_NUMBERS)
        win, msg = self.check_win(result)
        self.balance += win - self.last_bet
        self.result_lbl.config(text=f"الرقم الفائز: {result} | {msg}")

    def check_win(self, result):
        btype = self.bet_type.get()
        bet = self.last_bet
        win = 0
        msg = "خسرت!"
        if btype == "number":
            number = int(self.number_var.get())
            if result == number:
                win = bet * 35
                msg = f"فزت! ربحت {win}$ (رقم)"
        elif btype == "red":
            if result in RED_NUMBERS:
                win = bet * 2
                msg = f"فزت! ربحت {win}$ (أحمر)"
        elif btype == "black":
            if result in BLACK_NUMBERS:
                win = bet * 2
                msg = f"فزت! ربحت {win}$ (أسود)"
        elif btype == "even":
            if result != 0 and result % 2 == 0:
                win = bet * 2
                msg = f"فزت! ربحت {win}$ (زوجي)"
        elif btype == "odd":
            if result % 2 == 1:
                win = bet * 2
                msg = f"فزت! ربحت {win}$ (فردي)"
        elif btype == "zero":
            if result == 0:
                win = bet * 18
                msg = f"فزت! ربحت {win}$ (صفر)"
        elif btype == "dozen1":
            if 1 <= result <= 12:
                win = bet * 3
                msg = f"فزت! ربحت {win}$ (1-12)"
        elif btype == "dozen2":
            if 13 <= result <= 24:
                win = bet * 3
                msg = f"فزت! ربحت {win}$ (13-24)"
        elif btype == "dozen3":
            if 25 <= result <= 36:
                win = bet * 3
                msg = f"فزت! ربحت {win}$ (25-36)"
        return win, msg

if __name__ == "__main__":
    root = tk.Tk()
    RouletteGame(root)
    root.mainloop()