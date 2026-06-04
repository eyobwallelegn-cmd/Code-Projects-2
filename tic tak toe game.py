import tkinter as tk
from tkinter import ttk, messagebox
import random

# font setup
TITLE_FONT = ("Segoe UI", 18, "bold")
TEXT_FONT = ("Segoe UI", 11)
BOARD_FONT = ("Segoe UI", 24, "bold")

N_INF = -999
P_INF = 999

class Scores:
    def __init__(self):
        self.w = 0
        self.l = 0
        self.t = 0

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        # try zoomed, fallback
        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1100x700")

        self.s = Scores()
        self.p = tk.StringVar(value="X")
        self.d = tk.StringVar(value="Medium")

        self.b = []
        self.btns = []
        self.over = False

        self.mk_menu()
        self.layout()
        self.reset()

    def mk_menu(self):
        mb = tk.Menu(self.root)
        gm = tk.Menu(mb, tearoff=0)
        gm.add_command(label="New Game", command=self.reset)
        gm.add_command(label="Reset Scores", command=self.clr)
        gm.add_separator()
        gm.add_command(label="Exit", command=self.root.destroy)
        mb.add_cascade(label="Game", menu=gm)
        self.root.config(menu=mb)

    def layout(self):
        c = ttk.Frame(self.root, padding=20)
        c.pack(fill="both", expand=True)
        self.mk_board(c)
        self.side(c)
        self.keys()

    def mk_board(self, p):
        self.bf = ttk.Frame(p)
        self.bf.pack(side="left", padx=(0, 60))
        for r in range(3):
            tmp = []
            for c in range(3):
                btn = tk.Button(
                    self.bf,
                    width=5,
                    height=2,
                    font=BOARD_FONT,
                    command=lambda rr=r, cc=c: self.pmove(rr, cc)
                )
                btn.grid(row=r, column=c, padx=8, pady=8)
                tmp.append(btn)
            self.btns.append(tmp)

    def side(self, p):
        s = ttk.Frame(p)
        s.pack(side="left", fill="y")
        ttk.Label(s, text="Tic-Tac-Toe", font=TITLE_FONT).pack(anchor="w", pady=(0, 20))
        ttk.Label(s, text="Difficulty").pack(anchor="w")
        ttk.Combobox(s, textvariable=self.d, values=["Easy", "Medium", "Hard"], state="readonly", width=20).pack(anchor="w", pady=(0, 15))
        ttk.Label(s, text="Play As").pack(anchor="w")
        ttk.Combobox(s, textvariable=self.p, values=["X", "O"], state="readonly", width=20).pack(anchor="w", pady=(0, 15))
        ttk.Button(s, text="New Game", command=self.reset).pack(fill="x", pady=3)
        ttk.Button(s, text="Reset Scores", command=self.clr).pack(fill="x", pady=3)
        ttk.Button(s, text="Exit", command=self.root.destroy).pack(fill="x", pady=3)
        self.sl = ttk.Label(s, font=TEXT_FONT, justify="left")
        self.sl.pack(anchor="w", pady=(20, 10))
        self.st = ttk.Label(s, font=TEXT_FONT)
        self.st.pack(anchor="w")

    def keys(self):
        km = {"1":(0,0),"2":(0,1),"3":(0,2),"4":(1,0),"5":(1,1),"6":(1,2),"7":(2,0),"8":(2,1),"9":(2,2)}
        for k,v in km.items():
            r,c=v
            self.root.bind(k, lambda e,rr=r,cc=c: self.pmove(rr,cc))

    def reset(self):
        self.b = [[" " for _ in range(3)] for _ in range(3)]
        self.over = False
        for row in self.btns:
            for btn in row:
                btn.config(text="", state="normal", bg="SystemButtonFace")
        self.st.config(text="Your turn")
        self.upd()

    def clr(self):
        self.s = Scores()
        self.upd()

    def upd(self):
        self.sl.config(text="Wins: %d\nLosses: %d\nTies: %d" % (self.s.w, self.s.l, self.s.t))

    def moves(self):
        m = []
        for r in range(3):
            for c in range(3):
                if self.b[r][c] == " ":
                    m.append((r,c))
        return m

    def win(self, sym):
        for i,row in enumerate(self.b):
            if row[0]==row[1]==row[2]==sym:
                return [(i,0),(i,1),(i,2)]
        for c in range(3):
            if self.b[0][c]==self.b[1][c]==self.b[2][c]==sym:
                return [(0,c),(1,c),(2,c)]
        if self.b[0][0]==self.b[1][1]==self.b[2][2]==sym:
            return [(0,0),(1,1),(2,2)]
        if self.b[0][2]==self.b[1][1]==self.b[2][0]==sym:
            return [(0,2),(1,1),(2,0)]
        return None

    def full(self):
        return len(self.moves())==0

    def put(self, r, c, sym):
        self.b[r][c] = sym
        self.btns[r][c].config(text=sym)

    def pmove(self, r, c):
        if self.over:
            return
        if self.b[r][c] != " ":
            self.st.config(text="Occupied")
            return
        pl = self.p.get()
        ai = "O" if pl=="X" else "X"
        self.put(r, c, pl)
        w = self.win(pl)
        if w:
            self.s.w += 1
            self.end("You won!", w)
            return
        if self.full():
            self.s.t += 1
            self.end("Tie!")
            return
        self.cpu(ai, pl)

    def cpu(self, ai, pl):
        self.st.config(text="Thinking...")
        self.root.update()
        diff = self.d.get()
        if diff == "Easy":
            mv = random.choice(self.moves())
        elif diff == "Medium":
            mv = self.med(ai, pl)
        else:
            mv = self.hard(ai, pl)
        r,c = mv
        self.put(r, c, ai)
        w = self.win(ai)
        if w:
            self.s.l += 1
            self.end("You lost!", w)
            return
        if self.full():
            self.s.t += 1
            self.end("Tie!")
            return
        self.st.config(text="Your turn")

    def med(self, ai, pl):
        # try win
        for r,c in self.moves():
            self.b[r][c] = ai
            if self.win(ai):
                self.b[r][c] = " "
                return r,c
            self.b[r][c] = " "
        # block
        for r,c in self.moves():
            self.b[r][c] = pl
            if self.win(pl):
                self.b[r][c] = " "
                return r,c
            self.b[r][c] = " "
        # center
        if self.b[1][1] == " ":
            return 1,1
        return random.choice(self.moves())

    def mm(self, mx, ai, pl):
        if self.win(ai):
            return 1
        if self.win(pl):
            return -1
        if self.full():
            return 0
        if mx:
            best = N_INF
            for r,c in self.moves():
                self.b[r][c] = ai
                s = self.mm(False, ai, pl)
                self.b[r][c] = " "
                if s > best:
                    best = s
            return best
        else:
            best = P_INF
            for r,c in self.moves():
                self.b[r][c] = pl
                s = self.mm(True, ai, pl)
                self.b[r][c] = " "
                if s < best:
                    best = s
            return best

    def hard(self, ai, pl):
        best = N_INF
        bm = None
        for r,c in self.moves():
            self.b[r][c] = ai
            s = self.mm(False, ai, pl)
            self.b[r][c] = " "
            if s > best:
                best = s
                bm = (r,c)
        return bm

    def end(self, msg, line=None):
        self.over = True
        if line:
            for r,c in line:
                self.btns[r][c].config(bg="#90EE90")
        for row in self.btns:
            for btn in row:
                btn.config(state="disabled")
        self.upd()
        self.st.config(text=msg)
        messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()