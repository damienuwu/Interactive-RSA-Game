import tkinter as tk
from tkinter import messagebox
import random
import math
import os

# --- STYLE CONFIGURATION ---
BG_COLOR = "#0d0d0d"       
ACCENT_GREEN = "#00ff41"    
ACCENT_RED = "#ff3333"      
BTN_BG = "#1a1a1a"          
TEXT_COLOR = "#e0e0e0"      

class RSAVaultFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA MISSION CONTROL v2.0")
        self.root.geometry("1100x650")
        self.root.configure(bg=BG_COLOR)
        
        self.agent_name = "Unknown Agent"
        self.p = self.q = self.n = self.phi = self.e = self.d = 0
        self.time_elapsed = 0
        self.timer_running = False
        self.leaderboard_file = "leaderboard.txt"
        
        self.setup_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def styled_button(self, parent, text, command, color=ACCENT_GREEN, width=20):
        btn = tk.Button(parent, text=text, command=command, 
                        bg=BTN_BG, fg=color, activebackground=color, 
                        activeforeground=BG_COLOR, font=("Courier New", 11, "bold"),
                        width=width, height=2, bd=1, relief="flat", cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg=color, fg=BG_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG, fg=color))
        return btn

    def create_layout(self, stage_name, instruction):
        self.clear_screen()
        # LEFT PANEL: System Status
        self.left_panel = tk.Frame(self.root, bg=BTN_BG, width=350)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)

        tk.Label(self.left_panel, text=f"AGENT: {self.agent_name}", fg=ACCENT_GREEN, 
                 bg=BTN_BG, font=("Courier New", 10)).pack(pady=(20, 0))

        self.timer_label = tk.Label(self.left_panel, text=f"SESSION_TIME: {self.time_elapsed}s", 
                                   fg=ACCENT_GREEN, bg=BTN_BG, font=("Courier New", 12))
        self.timer_label.pack(pady=10)

        tk.Label(self.left_panel, text=f"STATUS: {stage_name}", fg=ACCENT_GREEN, 
                 bg=BTN_BG, font=("Courier New", 14, "bold")).pack(pady=10)
        
        tk.Label(self.left_panel, text=instruction, fg=TEXT_COLOR, bg=BTN_BG, 
                 font=("Courier New", 10), justify="left", wraplength=300).pack(pady=20, padx=20)

        self.styled_button(self.left_panel, "ABORT MISSION", self.setup_welcome_screen, 
                           color=ACCENT_RED, width=15).pack(side="bottom", pady=30)

        # RIGHT PANEL: Workspace
        self.workspace = tk.Frame(self.root, bg=BG_COLOR)
        self.workspace.pack(side="right", expand=True, fill="both")

    def setup_welcome_screen(self):
        self.timer_running = False
        self.clear_screen()
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="R S A  V A U L T", fg=ACCENT_GREEN, 
                 bg=BG_COLOR, font=("Courier New", 40, "bold")).pack()
        tk.Label(main_frame, text="[SECURE DATA TRANSMISSION PROTOCOL]", fg="#555555", 
                 bg=BG_COLOR, font=("Courier New", 12)).pack(pady=30)

        btn_row = tk.Frame(main_frame, bg=BG_COLOR)
        btn_row.pack()
        self.styled_button(btn_row, "INITIATE MISSION", self.agent_id_screen).pack(side="left", padx=10)
        self.styled_button(btn_row, "LEADERBOARD", self.show_leaderboard, color="#ffff00").pack(side="left", padx=10)

    def agent_id_screen(self):
        """New UI for Agent Name Entry"""
        self.clear_screen()
        cont = tk.Frame(self.root, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(cont, text="I D E N T I T Y   V E R I F I C A T I O N", fg=ACCENT_GREEN, 
                 bg=BG_COLOR, font=("Courier New", 18, "bold")).pack(pady=20)
        
        tk.Label(cont, text="ENTER AGENT ID:", fg="#888888", bg=BG_COLOR, font=("Courier New", 12)).pack()
        
        self.name_entry = tk.Entry(cont, font=("Courier New", 20), bg=BTN_BG, fg=ACCENT_GREEN, 
                                  justify="center", insertbackground=ACCENT_GREEN, relief="flat", width=20)
        self.name_entry.pack(pady=20, ipady=5)
        self.name_entry.focus_set()

        self.styled_button(cont, "AUTHORIZE ACCESS", self.process_agent_id).pack(pady=10)

    def process_agent_id(self):
        name = self.name_entry.get().strip()
        if name:
            self.agent_name = name
            self.difficulty_selection()
        else:
            messagebox.showwarning("IDENTITY ERROR", "Agent ID cannot be empty.")

    def difficulty_selection(self):
        self.create_layout("DIFFICULTY", f"Agent {self.agent_name}, select the bit-strength for this mission.")
        cont = tk.Frame(self.workspace, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")
        
        levels = {"EASY": (10, 50), "MEDIUM": (50, 150), "HARD": (150, 500)}
        for lvl, s in levels.items():
            self.styled_button(cont, lvl, lambda l=lvl, r=s: self.start_game(l, r)).pack(pady=10)

    def start_game(self, level, r):
        self.difficulty = level
        self.current_range = r
        self.time_elapsed = 0
        self.timer_running = True
        self.update_timer()
        self.stage_1_prime_input()

    def stage_1_prime_input(self):
        self.create_layout("STAGE_01", "Input or generate two distinct primes p and q.")
        input_cont = tk.Frame(self.workspace, bg=BG_COLOR)
        input_cont.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(input_cont, text="PRIME P:", fg=ACCENT_GREEN, bg=BG_COLOR).grid(row=0, column=0, pady=10)
        self.p_entry = tk.Entry(input_cont, font=("Courier New", 14), bg=BTN_BG, fg="white")
        self.p_entry.grid(row=0, column=1, padx=10)
        
        tk.Label(input_cont, text="PRIME Q:", fg=ACCENT_GREEN, bg=BG_COLOR).grid(row=1, column=0, pady=10)
        self.q_entry = tk.Entry(input_cont, font=("Courier New", 14), bg=BTN_BG, fg="white")
        self.q_entry.grid(row=1, column=1, padx=10)

        self.styled_button(input_cont, "AUTO-GENERATE", self.auto_gen_primes, width=15).grid(row=2, column=0, columnspan=2, pady=20)
        self.styled_button(input_cont, "VALIDATE", self.validate_primes_input, width=25).grid(row=3, column=0, columnspan=2)

    def validate_primes_input(self):
        try:
            p_val, q_val = int(self.p_entry.get()), int(self.q_entry.get())
            if p_val != q_val and self.is_prime(p_val) and self.is_prime(q_val):
                self.p, self.q = p_val, q_val
                self.stage_2_keygen()
            else:
                messagebox.showerror("ERROR", "Invalid or identical prime inputs.")
        except:
            messagebox.showerror("ERROR", "Integer inputs required.")

    def auto_gen_primes(self):
        primes = [n for n in range(self.current_range[0], self.current_range[1]) if self.is_prime(n)]
        p, q = random.sample(primes, 2)
        self.p_entry.delete(0, tk.END); self.p_entry.insert(0, str(p))
        self.q_entry.delete(0, tk.END); self.q_entry.insert(0, str(q))

    def stage_2_keygen(self):
        self.n, self.phi = self.p * self.q, (self.p - 1) * (self.q - 1)
        e_opts = [e for e in range(3, self.phi) if math.gcd(e, self.phi) == 1][:5]
        self.create_layout("STAGE_02: KEYGEN", f"n: {self.n}\nφ: {self.phi}")
        btn_cont = tk.Frame(self.workspace, bg=BG_COLOR)
        btn_cont.place(relx=0.5, rely=0.5, anchor="center")
        for val in e_opts:
            self.styled_button(btn_cont, f"e = {val}", lambda v=val: self.calc_d(v), width=15).pack(pady=5)

    def calc_d(self, chosen_e):
        self.e = chosen_e
        self.d = pow(self.e, -1, self.phi)
        self.create_layout("STAGE_02: SECURED", "Key derived. Memorize this value.")
        cont = tk.Frame(self.workspace, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cont, text="PRIVATE KEY (d)", fg=ACCENT_GREEN, bg=BG_COLOR).pack()
        tk.Label(cont, text=str(self.d), fg="#ffff00", bg=BTN_BG, font=("Courier", 40), padx=20).pack(pady=10)
        self.styled_button(cont, "PROCEED", self.stage_3_encrypt).pack(pady=20)

    def stage_3_encrypt(self):
        self.create_layout("STAGE_03", "Input secret message.")
        cont = tk.Frame(self.workspace, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")
        self.msg_entry = tk.Entry(cont, font=("Courier New", 18), bg=BTN_BG, fg=ACCENT_GREEN, width=25)
        self.msg_entry.pack(pady=20)
        self.styled_button(cont, "ENCRYPT", self.encrypt_action).pack()

    def encrypt_action(self):
        msg = self.msg_entry.get()
        if not msg: return
        self.encrypted_msg = [pow(ord(c), self.e, self.n) for c in msg]
        self.stage_4_decrypt()

    def stage_4_decrypt(self):
        self.create_layout("STAGE_04", f"CIPHER:\n{self.encrypted_msg}")
        cont = tk.Frame(self.workspace, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cont, text="ENTER PRIVATE KEY (d):", fg=ACCENT_RED, bg=BG_COLOR).pack(pady=10)
        self.d_input = tk.Entry(cont, font=("Courier New", 20), bg=BTN_BG, fg=ACCENT_RED, width=15, justify="center")
        self.d_input.pack(pady=10)
        self.styled_button(cont, "UNLOCK", self.finish_game, color=ACCENT_RED).pack()

    def finish_game(self):
        try:
            if int(self.d_input.get()) == self.d:
                decrypted = "".join([chr(pow(c, self.d, self.n)) for c in self.encrypted_msg])
                self.timer_running = False
                # Save to leaderboard
                with open(self.leaderboard_file, "a") as f:
                    f.write(f"{self.agent_name},{self.time_elapsed},{self.difficulty}\n")
                self.show_access_granted(decrypted)
            else:
                messagebox.showerror("DENIED", "Incorrect Private Key.")
        except: pass

    def show_access_granted(self, msg):
        self.create_layout("SUCCESS", "Vault decrypted.")
        cont = tk.Frame(self.workspace, bg=BG_COLOR)
        cont.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cont, text="A C C E S S   G R A N T E D", fg=ACCENT_GREEN, bg=BG_COLOR, font=("Courier New", 24, "bold")).pack()
        msg_box = tk.Frame(cont, bg=BTN_BG, padx=30, pady=20, highlightthickness=1, highlightbackground=ACCENT_GREEN)
        msg_box.pack(pady=20)
        tk.Label(msg_box, text=f"MESSAGE: {msg}", fg="white", bg=BTN_BG, font=("Courier New", 14)).pack()
        self.styled_button(cont, "MAIN TERMINAL", self.setup_welcome_screen).pack()

    def show_leaderboard(self):
        self.clear_screen()
        tk.Label(self.root, text="TOP AGENTS", fg="#ffff00", bg=BG_COLOR, font=("Courier New", 30, "bold")).pack(pady=30)
        list_frame = tk.Frame(self.root, bg=BG_COLOR)
        list_frame.pack(expand=True, fill="both")

        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "r") as f:
                lines = [l.strip().split(",") for l in f.readlines() if "," in l]
                scores = sorted(lines, key=lambda x: int(x[1]))[:10]
                for i, s in enumerate(scores):
                    tk.Label(list_frame, text=f"{i+1}. {s[0]:<15} {s[1]}s | Level: {s[2]}", 
                             fg="white", bg=BG_COLOR, font=("Courier New", 14)).pack()
        else:
            tk.Label(list_frame, text="NO MISSION DATA FOUND", fg="white", bg=BG_COLOR).pack()

        self.styled_button(self.root, "RETURN", self.setup_welcome_screen).pack(pady=40)

    def is_prime(self, n):
        if n < 2: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            if hasattr(self, 'timer_label'): self.timer_label.config(text=f"SESSION_TIME: {self.time_elapsed}s")
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk(); app = RSAVaultFinal(root); root.mainloop()