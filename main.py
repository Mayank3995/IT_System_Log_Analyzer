import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import log_parser, exporter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import mplcursors 
import os
import pandas as pd
import numpy as np

class LogAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☢️ TERMINAL COMMANDER v13.0 - THE ULTIMATE STABLE")
        self.root.geometry("1600x950")
        
        # --- Theme Colors ---
        self.bg_deep = "#050505"
        self.sidebar_bg = "#0a0a12"
        self.parrot_green = "#32de84"  
        self.neon_cyan = "#00f7ff"
        self.neon_magenta = "#ff00ff"
        self.neon_red = "#ff3131"
        self.text_white = "#ffffff"
        
        self.file_path = "" 
        self.all_logs = []
        self.is_paused = False
        self.phase = 0 
        self.ingress_buffer = [0] * 30 
        
        self.root.configure(bg=self.bg_deep)
        self.setup_ui()
        
        # 2x4 Matrix Figure Setup
        self.fig = plt.figure(figsize=(18, 10), facecolor=self.bg_deep)
        self.gs = self.fig.add_gridspec(2, 4, hspace=0.45, wspace=0.35)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.ani = FuncAnimation(self.fig, self.update_dashboard, interval=1000, cache_frame_data=False)

    def setup_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=self.sidebar_bg, width=320, highlightthickness=2, highlightbackground=self.parrot_green)
        sidebar.pack(side="left", fill="y", padx=5, pady=5)
        
        tk.Label(sidebar, text="COMMAND CENTER", fg=self.parrot_green, bg=self.sidebar_bg, font=("Impact", 22)).pack(pady=30)
        
        def create_btn(text, cmd, clr):
            btn = tk.Button(sidebar, text=text, command=cmd, bg="#111520", fg=self.text_white, 
                            activebackground=clr, activeforeground="black",
                            relief="flat", font=("Verdana", 11, "bold"), height=2, cursor="hand2",
                            highlightthickness=1, highlightbackground=clr)
            btn.pack(fill="x", padx=15, pady=6)
            btn.bind("<Enter>", lambda e: btn.config(bg=clr, fg="black"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#111520", fg=self.text_white))
            return btn

        # 6 Buttons (Sahi se connect kiye hain)
        create_btn("📊 OVERVIEW", self.show_overview, self.parrot_green)
        create_btn("📡 NEON STREAM", self.open_live_stream, self.neon_cyan)
        self.btn_pause = create_btn("⏸ KILL PROCESS", self.toggle_pause, self.neon_red)
        create_btn("📂 MOUNT DATA", self.select_file, self.neon_magenta)
        create_btn("📜 ANALYSIS", self.show_full_summary, self.parrot_green)
        create_btn("📥 DATA DUMP", self.export_data, self.neon_red)
        
        self.status_label = tk.Label(sidebar, text="● SYSTEM READY", fg=self.parrot_green, bg=self.sidebar_bg, font=("Consolas", 12, "bold"))
        self.status_label.pack(side="bottom", pady=40)

        # Right Side Container
        self.container = tk.Frame(self.root, bg=self.bg_deep)
        self.container.pack(side="right", fill="both", expand=True)

        # Parrot Green Table Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.bg_deep, foreground=self.parrot_green, fieldbackground=self.bg_deep, font=("Consolas", 10))
        style.configure("Treeview.Heading", background="#1a1a2e", foreground=self.neon_cyan, font=("Verdana", 9, "bold"))

        self.tree_frame = tk.Frame(self.container, bg=self.bg_deep)
        self.tree_frame.pack(fill="x", padx=20, pady=10)
        self.tree = ttk.Treeview(self.tree_frame, columns=("T", "L", "M"), show="headings", height=4)
        for c, h in zip(("T", "L", "M"), ("TIME", "LEVEL", "MESSAGE")): 
            self.tree.heading(c, text=h); self.tree.column(c, anchor="center")
        self.tree.pack(fill="x")

        self.chart_frame = tk.Frame(self.container, bg=self.bg_deep)
        self.chart_frame.pack(fill="both", expand=True)

    def style_ax(self, ax, title, color):
        ax.set_title(f"// {title}", color=color, fontsize=9, fontweight='bold', loc='left')
        ax.set_facecolor("#020205")
        ax.tick_params(colors=color, labelsize=7)
        for spine in ax.spines.values(): spine.set_edgecolor("#1f1f2e")

    def update_dashboard(self, i):
        if self.is_paused or not self.file_path or not os.path.exists(self.file_path): return
        
        try:
            new_logs = log_parser.parse_logs(self.file_path)
            if not new_logs: return
            
            self.all_logs = new_logs
            df = pd.DataFrame(self.all_logs, columns=['Time', 'Level', 'Msg'])
            self.phase += 0.8
            
            self.fig.clear()
            self.fig.patch.set_facecolor(self.bg_deep)

            # --- Row 1 ---
            ax1 = self.fig.add_subplot(self.gs[0,0])
            counts = df['Level'].value_counts()
            ax1.bar(counts.index, counts.values, color=self.parrot_green); self.style_ax(ax1, "NODE LOAD", self.parrot_green)

            ax2 = self.fig.add_subplot(self.gs[0,1])
            ax2.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=[self.parrot_green, self.neon_cyan, self.neon_red], textprops={'color':"w", 'size':7})
            self.style_ax(ax2, "THREAT MIX", self.neon_magenta)

            ax3 = self.fig.add_subplot(self.gs[0,2])
            ax3.plot(np.random.rand(10), color=self.parrot_green, marker='o', lw=2); self.style_ax(ax3, "NET TRAFFIC", self.parrot_green)

            ax4 = self.fig.add_subplot(self.gs[0,3])
            ax4.scatter(range(10), np.random.rand(10), color=self.neon_red, s=30); self.style_ax(ax4, "ANOMALIES", self.neon_red)

            # --- Row 2 ---
            ax5 = self.fig.add_subplot(self.gs[1,0])
            ax5.hist(np.random.randn(50), color=self.neon_magenta, bins=10); self.style_ax(ax5, "LOG FREQ", self.neon_magenta)

            ax6 = self.fig.add_subplot(self.gs[1,1])
            self.ingress_buffer.append(len(new_logs) % 15)
            self.ingress_buffer = self.ingress_buffer[-30:]
            ax6.fill_between(range(30), self.ingress_buffer, color=self.parrot_green, alpha=0.3)
            ax6.plot(self.ingress_buffer, color=self.parrot_green, lw=1.5); self.style_ax(ax6, "DATA INGRESS", self.parrot_green)

            ax7 = self.fig.add_subplot(self.gs[1,2])
            ax7.boxplot(np.random.rand(10), patch_artist=True, boxprops=dict(facecolor=self.parrot_green)); self.style_ax(ax7, "LATENCY", self.parrot_green)

            ax8 = self.fig.add_subplot(self.gs[1,3])
            x = np.linspace(0, 10, 100); y = np.sin(x + self.phase)
            ax8.plot(x, y, color=self.parrot_green, lw=2); self.style_ax(ax8, "SIGNAL WAVE", self.parrot_green)

            # Interactivity & Table Sync
            mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f"VAL: {sel.target[1]:.2f}"))
            self.tree.delete(*self.tree.get_children())
            for log in self.all_logs[-4:]: self.tree.insert("", "end", values=log)
            
            self.canvas.draw()
        except Exception as e:
            print(f"Update Error: {e}")

    # --- Functions ---
    def toggle_pause(self): self.is_paused = not self.is_paused
    def select_file(self):
        path = filedialog.askopenfilename()
        if path: self.file_path = path; self.status_label.config(text="● RUNNING", fg=self.parrot_green)

    def export_data(self):
        if not self.all_logs: return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            exporter.export_to_csv(self.all_logs, file_path)
            messagebox.showinfo("Success", "File Saved Successfully!")

    def open_live_stream(self):
        win = tk.Toplevel(self.root); win.configure(bg="#000")
        txt = scrolledtext.ScrolledText(win, bg="#000", fg=self.parrot_green); txt.pack(fill="both", expand=True)
        for log in self.all_logs[-15:]: txt.insert(tk.END, f"{log}\n")

    def show_overview(self): messagebox.showinfo("SOC", "All Systems Nominal")
    def show_full_summary(self): messagebox.showinfo("SOC", f"Total Records: {len(self.all_logs)}")

if __name__ == "__main__":
    root = tk.Tk(); app = LogAnalyzerApp(root); root.mainloop()