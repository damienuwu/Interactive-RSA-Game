import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import math
import os

class RSAVaultGame:
    def __init__(self, root):
        self.root = root
        self.root.title("The Vault of Primes: RSA Mission")
        self.root.geometry("500x750")
        self.root.configure(bg="#0d0d0d")

        # Game State Variables
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.time_elapsed = 0  # Now tracks total time taken
        self.difficulty = ""
        self.current_range = (10, 50) 
        self.encrypted_msg = []
        self.leaderboard_file = "leaderboard.txt"
        self.timer_running = False

        self.setup_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def is_prime(self, n): # Feature: Prime Validation [cite: 30]
        if n < 2: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    def update_timer(self): # Feature: Time Tracking
        if self.timer_running:
            self.time_elapsed += 1
            try:
                if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                    self.timer_label.config(text=f"TIME ELAPSED: {self.time_elapsed}s")
            except:
                pass 
            self.root.after(1000, self.update_timer)

    def add_quit_button(self): # Global Quit Feature
        tk.Button(self.root, text="ABORT MISSION", command=self.setup_welcome_screen, 
                  bg="#330000", fg="white", font=("Courier", 10)).pack(side="bottom", pady=20)

    def setup_welcome_screen(self): # Sample Game Flow: Welcome [cite: 64]
        self.timer_running = False 
        self.clear_screen()
        tk.Label(self.root, text="SECURITY SYSTEM: RSA", fg="#00ff41", bg="#0d0d0d", font=("Courier", 20, "bold")).pack(pady=40)
        
        tk.Button(self.root, text="START MISSION", command=self.difficulty_selection, 
                  bg="#1a1a1a", fg="#00ff41", font=("Courier", 12), width=25).pack(pady=10)
        
        tk.Button(self.root, text="VIEW LEADERBOARD", command=self.show_leaderboard, 
                  bg="#1a1a1a", fg="#ffff00", font=("Courier", 12), width=25).pack(pady=10)
        
        tk.Button(self.root, text="EXIT SYSTEM", command=self.root.quit, 
                  bg="#330000", fg="white", font=("Courier", 12), width=25).pack(pady=10)

    def difficulty_selection(self): # Feature: Difficulty Levels [cite: 54, 57, 68]
        self.clear_screen()
        tk.Label(self.root, text="SELECT ENCRYPTION STRENGTH", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14)).pack(pady=30)
        
        levels = {
            "Easy": {"range": (10, 50)},
            "Medium": {"range": (50, 150)},
            "Hard": {"range": (150, 500)}
        }

        for level, settings in levels.items():
            tk.Button(self.root, text=level.upper(), 
                      command=lambda l=level, s=settings: self.start_game(l, s), 
                      bg="#1a1a1a", fg="white", font=("Courier", 12), width=20).pack(pady=10)
        self.add_quit_button()

    def start_game(self, level, settings):
        self.difficulty = level
        self.time_elapsed = 0
        self.current_range = settings["range"]
        
        # Guarantee primes in the pool
        start, end = self.current_range
        all_possible_primes = [n for n in range(start, end) if self.is_prime(n)]
        
        if len(all_possible_primes) < 2:
            all_possible_primes = [11, 13, 17, 19, 23]
            
        guaranteed_primes = random.sample(all_possible_primes, 2)
        remaining_pool = [n for n in range(start, end) if n not in guaranteed_primes]
        decoys = random.sample(remaining_pool, min(6, len(remaining_pool)))
        
        self.prime_pool = guaranteed_primes + decoys
        random.shuffle(self.prime_pool)
        
        self.timer_running = True
        self.stage_1_ui()
        self.update_timer()

    def stage_1_ui(self): # Stage 1: Prime Selection [cite: 16, 28, 66]
        self.clear_screen()
        self.timer_label = tk.Label(self.root, text=f"TIME ELAPSED: {self.time_elapsed}s", fg="#00ff41", bg="#0d0d0d", font=("Courier", 12, "bold"))
        self.timer_label.pack(pady=10)

        tk.Label(self.root, text="STAGE 1: SELECT TWO PRIMES", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="INSTRUCTION: Identify and click two prime\nnumbers from the grid below.", fg="#cccccc", bg="#0d0d0d", font=("Courier", 9)).pack(pady=5)
        
        self.selected_primes = []
        self.prime_buttons = []
        container = tk.Frame(self.root, bg="#0d0d0d")
        container.pack(pady=10)

        for num in self.prime_pool:
            btn = tk.Button(container, text=str(num), width=10, bg="#1a1a1a", fg="white",
                            command=lambda n=num: self.toggle_prime(n))
            btn.pack(pady=2)
            self.prime_buttons.append((num, btn))

        tk.Button(self.root, text="VALIDATE PRIMES", command=self.validate_selection, bg="#004400", fg="white", width=20).pack(pady=20)
        self.add_quit_button()

    def toggle_prime(self, n):
        if n in self.selected_primes:
            self.selected_primes.remove(n)
        elif len(self.selected_primes) < 2:
            self.selected_primes.append(n)
        
        for num, btn in self.prime_buttons:
            btn.config(bg="#00ff41" if num in self.selected_primes else "#1a1a1a", fg="black" if num in self.selected_primes else "white")

    def validate_selection(self):
        if len(self.selected_primes) != 2:
            messagebox.showwarning("Error", "Please select exactly two numbers.")
            return

        p, q = self.selected_primes
        if self.is_prime(p) and self.is_prime(q):
            self.p, self.q = p, q
            messagebox.showinfo("SUCCESS", "Primes Validated.")
            self.stage_2_ui()
        else:
            messagebox.showerror("FAILURE", "One or more values were not prime. Resetting...")
            self.start_game(self.difficulty, {"range": self.current_range})

    def stage_2_ui(self): # Stage 2: Key Generation [cite: 17, 31, 67]
        self.n = self.p * self.q # Requirement: n=p*q [cite: 35]
        self.phi = (self.p - 1) * (self.q - 1) # Requirement: phi(n)=(p-1)(q-1) [cite: 36]
        e_list = [e for e in range(3, self.phi) if math.gcd(e, self.phi) == 1][:5]
        
        self.clear_screen()
        self.timer_label = tk.Label(self.root, text=f"TIME ELAPSED: {self.time_elapsed}s", fg="#00ff41", bg="#0d0d0d", font=("Courier", 12, "bold"))
        self.timer_label.pack(pady=10)

        tk.Label(self.root, text="STAGE 2: KEY GENERATION", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Modulus (n): {self.n}\nTotient (phi): {self.phi}", fg="white", bg="#0d0d0d", font=("Courier", 12)).pack(pady=10)
        tk.Label(self.root, text="INSTRUCTION: Select an exponent (e) that is\ncoprime to the totient value shown above.", fg="#cccccc", bg="#0d0d0d", font=("Courier", 9)).pack(pady=5)
        
        for val in e_list:
            tk.Button(self.root, text=f"Select e = {val}", command=lambda v=val: self.calc_d(v), width=20).pack(pady=5)
        self.add_quit_button()

    def calc_d(self, chosen_e): # Requirement: Modular Inverse for Private Key 
        self.e = chosen_e
        self.d = pow(self.e, -1, self.phi)
        messagebox.showinfo("Key Generated", f"Your private key (d) is: {self.d}\nKEEP THIS SECURE!")
        self.stage_3_ui()

    def stage_3_ui(self): # Stage 3: Encryption [cite: 18, 39, 78]
        self.clear_screen()
        self.timer_label = tk.Label(self.root, text=f"TIME ELAPSED: {self.time_elapsed}s", fg="#00ff41", bg="#0d0d0d", font=("Courier", 12, "bold"))
        self.timer_label.pack(pady=10)

        tk.Label(self.root, text="STAGE 3: ENCRYPTION", fg="#00ff41", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="INSTRUCTION: Type the message you wish to\nencrypt in the text box below.", fg="#cccccc", bg="#0d0d0d", font=("Courier", 9)).pack(pady=5)
        
        self.msg_entry = tk.Entry(self.root, font=("Courier", 12), width=30)
        self.msg_entry.pack(pady=10)
        tk.Button(self.root, text="GENERATE CIPHERTEXT", command=self.encrypt_msg_action, bg="#1a1a1a", fg="#00ff41").pack(pady=10)
        self.add_quit_button()

    def encrypt_msg_action(self): # Requirement: Convert text to ASCII values [cite: 42, 44, 45]
        msg = self.msg_entry.get()
        if not msg: return
        self.encrypted_msg = [pow(ord(c), self.e, self.n) for c in msg]
        self.stage_4_ui()

    def stage_4_ui(self): # Stage 4: Decryption [cite: 19, 46, 81]
        self.clear_screen()
        self.timer_label = tk.Label(self.root, text=f"TIME ELAPSED: {self.time_elapsed}s", fg="#00ff41", bg="#0d0d0d", font=("Courier", 12, "bold"))
        self.timer_label.pack(pady=10)

        tk.Label(self.root, text="STAGE 4: DECRYPTION", fg="#ff3333", bg="#0d0d0d", font=("Courier", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"CIPHERTEXT:\n{self.encrypted_msg}", wraplength=400, fg="white", bg="#0d0d0d", font=("Courier", 10)).pack(pady=10)
        
        tk.Label(self.root, text="INSTRUCTION: Enter your Private Key (d) below\nto decrypt the message and complete the mission.", fg="#cccccc", bg="#0d0d0d", font=("Courier", 9)).pack(pady=5)
        
        self.d_input = tk.Entry(self.root, font=("Courier", 12), width=20)
        self.d_input.pack(pady=10)
        tk.Button(self.root, text="ACCESS DATA", command=self.finish_game, bg="#440000", fg="white").pack(pady=10)
        self.add_quit_button()

    def finish_game(self): # Feature: Decryption and Verification [cite: 49, 50, 85]
        try:
            val = self.d_input.get()
            if not val: return
            user_d = int(val)
            if user_d == self.d:
                decrypted_text = "".join([chr(pow(c, self.d, self.n)) for c in self.encrypted_msg])
                self.timer_running = False 
                messagebox.showinfo("DECRYPTED", f"Decryption Result: {decrypted_text}\nMISSIONS COMPLETE!")
                name = simpledialog.askstring("AGENT ID", f"Completion Time: {self.time_elapsed}s\nEnter your name for the records:")
                if name: self.save_score(name, self.time_elapsed)
                self.setup_welcome_screen()
            else:
                messagebox.showerror("ERROR", "Invalid Private Key! Decryption Failed.")
        except ValueError:
            messagebox.showwarning("Input Error", "The private key must be a number.")

    def save_score(self, name, score): # Feature: Leaderboard Log 
        with open(self.leaderboard_file, "a") as f:
            f.write(f"{name},{score},{self.difficulty}\n")

    def show_leaderboard(self):
        self.clear_screen()
        tk.Label(self.root, text="TOP AGENTS (Fastest Completions)", fg="#ffff00", bg="#0d0d0d", font=("Courier", 16, "bold")).pack(pady=20)
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, "r") as f:
                    lines = [l.strip().split(",") for l in f.readlines() if "," in l]
                    # Sorted by lowest time (Fastest)
                    scores = sorted(lines, key=lambda x: int(x[1]), reverse=False)
                    for s in scores[:10]:
                        tk.Label(self.root, text=f"{s[0]}: {s[1]}s | Level: {s[2]}", fg="white", bg="#0d0d0d", font=("Courier", 11)).pack()
            except:
                tk.Label(self.root, text="Log empty.", fg="white", bg="#0d0d0d").pack()
        else:
            tk.Label(self.root, text="No mission data found.", fg="white", bg="#0d0d0d").pack()
        tk.Button(self.root, text="MAIN TERMINAL", command=self.setup_welcome_screen).pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAVaultGame(root)
    root.mainloop()