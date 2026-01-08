import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import math
import time
import os

class RSAVaultGame:
    def __init__(self, root):
        self.root = root
        self.root.title("The Vault of Primes: RSA Mission")
        self.root.geometry("500x700")
        self.root.configure(bg="#0d0d0d")

        # Game State Variables
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.start_time = 0
        self.difficulty = ""
        self.encrypted_msg = []
        self.leaderboard_file = "leaderboard.txt"

        self.setup_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def is_prime(self, n):
        if n < 2: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    # --- UI SCREENS ---

    def setup_welcome_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="SECURITY SYSTEM: RSA", fg="#00ff41", bg="#0d0d0d", font=("Courier", 20, "bold")).pack(pady=40)
        
        tk.Button(self.root, text="START MISSION", command=self.difficulty_selection, 
                  bg="#1a1a1a", fg="#00ff41", font=("Courier", 12), width=25).pack(pady=10)
        
        tk.Button(self.root, text="VIEW LEADERBOARD", command=self.show_leaderboard, 
                  bg="#1a1a1a", fg="#ffff00", font=("Courier", 12), width=25).pack(pady=10)
        
        tk.Button(self.root, text="QUIT SYSTEM", command=self.root.quit, 
                  bg="#330000", fg="white", font=("Courier", 12), width=25).pack(pady=10)

    def difficulty_selection(self):
        self.clear_screen()
        tk.Label(self.root, text="SELECT ENCRYPTION STRENGTH", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14)).pack(pady=30)
        
        for level in ["Easy", "Medium", "Hard"]:
            tk.Button(self.root, text=level.upper(), command=lambda l=level: self.start_game(l), 
                      bg="#1a1a1a", fg="white", font=("Courier", 12), width=20).pack(pady=10)
        
        tk.Button(self.root, text="BACK", command=self.setup_welcome_screen, font=("Courier", 10)).pack(pady=20)

    def start_game(self, level):
        self.difficulty = level
        self.start_time = time.time()
        
        # Stage 1: Prime Number Selection via Random Function
        ranges = {'Easy': (10, 50), 'Medium': (50, 150), 'Hard': (150, 500)}
        start, end = ranges[level]
        primes = [i for i in range(start, end) if self.is_prime(i)]
        self.p, self.q = random.sample(primes, 2)
        
        self.stage_1_ui()

    def stage_1_ui(self):
        self.clear_screen()
        tk.Label(self.root, text="STAGE 1: PRIME SELECTION", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"The system generated:\nP = {self.p}\nQ = {self.q}", 
                 fg="white", bg="#0d0d0d", font=("Courier", 12), justify="center").pack(pady=20)
        
        # Validation Requirement
        tk.Button(self.root, text="VALIDATE & COMPUTE N", command=self.stage_2_ui, bg="#004400", fg="white", width=20).pack(pady=20)

    def stage_2_ui(self):
        # Stage 2: Key Generation Calculations
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        
        e_list = [e for e in range(3, self.phi) if math.gcd(e, self.phi) == 1][:5]
        
        self.clear_screen()
        tk.Label(self.root, text="STAGE 2: KEY GENERATION", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Modulus (n): {self.n}\nPhi(n): {self.phi}", fg="white", bg="#0d0d0d", font=("Courier", 12)).pack(pady=10)
        
        tk.Label(self.root, text="Choose Public Exponent (e):", fg="#ffff00", bg="#0d0d0d").pack(pady=10)
        for val in e_list:
            tk.Button(self.root, text=f"e = {val}", command=lambda v=val: self.calc_d(v), width=15).pack(pady=5)

    def calc_d(self, chosen_e):
        self.e = chosen_e
        # Calculate private key d
        self.d = pow(self.e, -1, self.phi)
        messagebox.showinfo("Private Key", f"Private Key (d) is: {self.d}\nKeep this safe to decrypt your message!")
        self.stage_3_ui()

    def stage_3_ui(self):
        # Stage 3: Encryption
        self.clear_screen()
        tk.Label(self.root, text="STAGE 3: ENCRYPTION", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="Enter message to secure:", fg="white", bg="#0d0d0d").pack()
        
        self.msg_entry = tk.Entry(self.root, font=("Courier", 12))
        self.msg_entry.pack(pady=10)
        
        tk.Button(self.root, text="ENCRYPT", command=self.encrypt_msg_action, bg="#1a1a1a", fg="#00ff41").pack(pady=10)

    def encrypt_msg_action(self):
        msg = self.msg_entry.get()
        if not msg: return
        self.encrypted_msg = [pow(ord(c), self.e, self.n) for c in msg]
        self.stage_4_ui()

    def stage_4_ui(self):
        # Stage 4: Decryption
        self.clear_screen()
        tk.Label(self.root, text="STAGE 4: DECRYPTION", fg="#ff3333", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Encrypted Message:\n{self.encrypted_msg}", wraplength=400, fg="white", bg="#0d0d0d").pack(pady=10)
        
        tk.Label(self.root, text="Enter Private Key (d):", fg="white", bg="#0d0d0d").pack()
        self.d_input = tk.Entry(self.root, font=("Courier", 12))
        self.d_input.pack(pady=10)
        
        tk.Button(self.root, text="UNLOCK VAULT", command=self.finish_game, bg="#440000", fg="white").pack(pady=10)

    def finish_game(self):
        try:
            user_d = int(self.d_input.get())
            if user_d == self.d:
                total_time = round(time.time() - self.start_time, 2)
                name = simpledialog.askstring("MISSION SUCCESS", f"Time: {total_time}s\nEnter your name for the leaderboard:")
                if name:
                    self.save_score(name, total_time)
                self.setup_welcome_screen()
            else:
                messagebox.showerror("ALARM", "Incorrect Key! Security breach detected.")
        except ValueError:
            messagebox.showwarning("Error", "Input must be a number.")

    # --- LEADERBOARD LOGIC ---

    def save_score(self, name, score):
        with open(self.leaderboard_file, "a") as f:
            f.write(f"{name},{score},{self.difficulty}\n")

    def show_leaderboard(self):
        self.clear_screen()
        tk.Label(self.root, text="TOP AGENTS", fg="#ffff00", bg="#0d0d0d", font=("Courier", 16, "bold")).pack(pady=20)
        
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "r") as f:
                scores = [line.strip().split(",") for line in f.readlines()]
                scores.sort(key=lambda x: float(x[1])) # Sort by time
                
                for i, (name, score, diff) in enumerate(scores[:10]):
                    tk.Label(self.root, text=f"{i+1}. {name} | {score}s | {diff}", 
                             fg="white", bg="#0d0d0d", font=("Courier", 11)).pack()
        else:
            tk.Label(self.root, text="Leaderboard is empty.", fg="gray", bg="#0d0d0d").pack()

        tk.Button(self.root, text="BACK TO MENU", command=self.setup_welcome_screen).pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAVaultGame(root)
    root.mainloop()