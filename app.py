"""Run with: python app.py. All search computation lives in engine/search.py."""
import tkinter as tk
from tkinter import ttk
from engine.search import Grid, search

BG="#f2f4f8"; PANEL="#e5eaf2"; TEXT="#203049"; MUTED="#52647b"
COLORS={"open":"#ffffff", "wall":"#7c8ca1", "weight":"#edd59d", "visited":"#a7cef1", "path":"#f5c66d", "start":"#397ee8", "goal":"#e89796"}

def configure_controls(root):
    # Clam honors color styling on macOS; Aqua draws native white controls.
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", background=PANEL, foreground=TEXT,
                    bordercolor="#ccd5e2", lightcolor=PANEL, darkcolor=PANEL,
                    relief="flat", borderwidth=1, padding=(16, 11),
                    font=("Helvetica", 12), focusthickness=2, focuscolor="#397ee8")
    style.map("TButton", background=[("pressed", "#d5e1f2"), ("active", "#e3ebf7")],
              bordercolor=[("focus", "#397ee8"), ("active", "#86a8d7")])
    style.configure("Run.TButton", background="#397ee8", foreground="#ffffff",
                    bordercolor="#397ee8", lightcolor="#397ee8", darkcolor="#397ee8",
                    font=("Helvetica", 12, "bold"), focuscolor=BG)
    style.map("Run.TButton", background=[("pressed", "#2864c1"), ("active", "#5793ef")],
              bordercolor=[("focus", TEXT), ("active", "#5793ef")])
    style.configure("TCombobox", fieldbackground=PANEL, background=PANEL,
                    foreground=TEXT, arrowcolor="#397ee8", bordercolor="#ccd5e2",
                    lightcolor=PANEL, darkcolor=PANEL, padding=(10, 9), arrowsize=14)
    style.map("TCombobox", fieldbackground=[("readonly", PANEL)],
              foreground=[("readonly", TEXT)], selectbackground=[("readonly", PANEL)],
              selectforeground=[("readonly", TEXT)],
              background=[("active", "#e3ebf7")],
              bordercolor=[("focus", "#397ee8")])
    style.configure("Horizontal.TScale", background="#397ee8", troughcolor=PANEL,
                    bordercolor=BG, lightcolor="#397ee8", darkcolor="#397ee8",
                    sliderlength=18, sliderthickness=12, borderwidth=0)
    style.map("Horizontal.TScale", background=[("active", "#5793ef")])
    root.option_add("*TCombobox*Listbox.background", PANEL)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", "#a7cef1")
    root.option_add("*TCombobox*Listbox.selectForeground", TEXT)
    root.option_add("*TCombobox*Listbox.font", "Helvetica 12")


class App:
    def __init__(self, root):
        self.root=root; root.title("Search Lab · AI Search & Decision Engine")
        root.configure(bg=BG); root.minsize(1040,740)
        configure_controls(root)
        self.grid=Grid(26,16); self.start=(2,8); self.goal=(23,8)
        self.visited=set(); self.path=set(); self.results={}; self.queue=[]; self.index=0
        self.playing=False; self.job=None; self.cell=27
        self.tool=tk.StringVar(value="Wall"); self.algorithm=tk.StringVar(value="A*")
        self.speed=tk.IntVar(value=25)
        tk.Label(root,text="SEARCH LAB",font=("Helvetica",12,"bold"),fg="#397ee8",bg=BG).pack(anchor="w",padx=26,pady=(22,4))
        tk.Label(root,text="Watch a decision take shape.",font=("Helvetica",25,"bold"),fg=TEXT,bg=BG).pack(anchor="w",padx=26)
        tk.Label(root,text="V1 / Classical search     •     Four-way movement     •     Python engine",fg=MUTED,bg=BG).pack(anchor="w",padx=26,pady=(5,18))
        bar=tk.Frame(root,bg=BG); bar.pack(fill="x",padx=26)
        for label,command in [("Run",self.run),("Pause / Resume",self.toggle),("Step",self.step),("Compare",self.compare),("Reset map",self.reset)]:
            ttk.Button(bar,text=label,command=command,style="Run.TButton" if label=="Run" else "TButton",cursor="hand2").pack(side="left",padx=(0,7))
        ttk.Combobox(bar,textvariable=self.algorithm,values=["A*","Uniform-cost"],state="readonly",width=14,font=("Helvetica",12)).pack(side="left")
        edit=tk.Frame(root,bg=BG); edit.pack(fill="x",padx=26,pady=12)
        tk.Label(edit,text="Paint:",fg=TEXT,bg=BG).pack(side="left")
        ttk.Combobox(edit,textvariable=self.tool,values=["Wall","Erase","Cost 5","Start","Goal"],state="readonly",width=12,font=("Helvetica",12)).pack(side="left",padx=8)
        tk.Label(edit,text="Delay (ms)",fg=MUTED,bg=BG).pack(side="left",padx=10)
        ttk.Scale(edit,from_=1,to=150,variable=self.speed).pack(side="left")
        tk.Label(edit,text="Click or drag to edit. Compare uses the same map.",fg=MUTED,bg=BG).pack(side="left",padx=16)
        self.canvas=tk.Canvas(root,bg=BG,highlightthickness=0,height=432)
        self.canvas.pack(fill="both",expand=True,padx=26)
        self.canvas.bind("<Configure>",lambda e:self.draw())
        self.canvas.bind("<Button-1>",self.paint); self.canvas.bind("<B1-Motion>",self.paint)
        legend=tk.Frame(root,bg=BG); legend.pack(fill="x",padx=26,pady=8)
        for key in ["start","goal","wall","weight","visited","path"]:
            tk.Label(legend,text="■ "+("cost 5" if key=="weight" else key),fg=COLORS[key],bg=BG).pack(side="left",padx=(0,18))
        self.status=tk.Label(root,text="",fg=TEXT,bg=PANEL,anchor="w",justify="left",font=("Menlo",11),padx=15,pady=12)
        self.status.pack(fill="x",padx=26,pady=(0,8))
        tk.Label(root,text="A*: f(n) = g(n) + h(n)   |   g = cost so far   |   h = Manhattan distance × minimum step cost",fg=MUTED,bg=BG).pack(pady=(0,16))
        self.reset()

    def cancel(self):
        if self.job is not None: self.root.after_cancel(self.job)
        self.job=None; self.playing=False

    def invalidate(self):
        self.cancel(); self.visited.clear(); self.path.clear(); self.queue=[]; self.index=0; self.results={}
        self.status.config(text="Ready. Run A* to explore, or Compare to check it against uniform-cost search.")

    def reset(self):
        self.invalidate(); self.grid=Grid(26,16); self.start=(2,8); self.goal=(23,8)
        self.grid.walls={(10,y) for y in range(13) if y!=3} | {(17,y) for y in range(3,16) if y!=12}
        self.grid.weights={(x,8):5 for x in range(4,10)}
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.cell=min(max(self.canvas.winfo_width(),702)/26,max(self.canvas.winfo_height(),432)/16)
        s=self.cell
        for y in range(16):
            for x in range(26):
                c=(x,y); kind="open"
                if c in self.grid.weights: kind="weight"
                if c in self.visited: kind="visited"
                if c in self.path: kind="path"
                if c in self.grid.walls: kind="wall"
                if c==self.start: kind="start"
                if c==self.goal: kind="goal"
                self.canvas.create_rectangle(x*s+1,y*s+1,(x+1)*s-1,(y+1)*s-1,fill=COLORS[kind],outline="")
                label="S" if c==self.start else "G" if c==self.goal else "5" if c in self.grid.weights else ""
                if label: self.canvas.create_text((x+.5)*s,(y+.5)*s,text=label,fill="#ffffff" if kind=="start" else TEXT,font=("Helvetica",10,"bold"))

    def paint(self,event):
        c=(int(event.x/self.cell),int(event.y/self.cell))
        if not self.grid.valid(c): return
        tool=self.tool.get()
        if c in (self.start,self.goal): return
        self.invalidate()
        self.grid.walls.discard(c); self.grid.weights.pop(c,None)
        if tool=="Wall": self.grid.walls.add(c)
        elif tool=="Cost 5": self.grid.weights[c]=5
        elif tool=="Start": self.start=c
        elif tool=="Goal": self.goal=c
        self.draw()

    def prepare(self):
        self.invalidate()
        result=search(self.grid,self.start,self.goal,"astar" if self.algorithm.get()=="A*" else "ucs")
        self.result=result; self.queue=result.expanded

    def run(self):
        self.prepare(); self.playing=True; self.tick()

    def tick(self):
        self.job=None
        if not self.playing: return
        self.advance()
        if self.playing: self.job=self.root.after(max(1,int(self.speed.get())),self.tick)

    def advance(self):
        if self.index<len(self.queue):
            self.visited.add(self.queue[self.index]); self.index+=1
            self.status.config(text=f"Exploration playback: {self.index} / {len(self.queue)} expanded states. Timing excludes animation.")
        if self.index==len(self.queue):
            self.playing=False; self.path=set(self.result.path)
            self.status.config(text=self.summary(self.result))
        self.draw()

    def step(self):
        self.cancel()
        if not self.queue: self.prepare()
        self.advance()

    def toggle(self):
        if self.playing: self.cancel()
        elif self.queue and self.index<len(self.queue): self.playing=True; self.tick()

    def summary(self,r):
        cost="unreachable" if r.cost is None else f"{r.cost:g}"
        return f"{r.algorithm.upper():6} | expanded {len(r.expanded):3} | discovered {r.discovered:3} | cost {cost} | {r.elapsed_ms:.3f} ms"

    def compare(self):
        self.invalidate()
        a=search(self.grid,self.start,self.goal); u=search(self.grid,self.start,self.goal,"ucs")
        self.visited=set(a.expanded); self.path=set(a.path); self.draw()
        verdict="Both report no route." if a.cost is None else f"Optimal cost verified against uniform-cost: {a.cost==u.cost}."
        self.status.config(text=self.summary(a)+"\n"+self.summary(u)+"\n"+verdict+" Displaying A*. Single-run timings are illustrative.")

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
