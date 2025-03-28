# import psutil
# import tkinter as tk
# from tkinter import ttk

# class ProcessMonitor:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Real-Time Process Monitoring Dashboard")
#         self.root.geometry("800x400")

#         # Setting up the treeview
#         self.tree = ttk.Treeview(root, columns=("PID", "Name", "CPU", "Memory"), show="headings")
#         self.tree.heading("PID", text="PID")
#         self.tree.heading("Name", text="Name")
#         self.tree.heading("CPU", text="CPU (%)")
#         self.tree.heading("Memory", text="Memory (MB)")
#         self.tree.pack(fill=tk.BOTH, expand=True)

#         # Refresh data every second
#         self.update_processes()

#     def update_processes(self):
#         # Clear previous data
#         for row in self.tree.get_children():
#             self.tree.delete(row)

#         # Fetch and display process data
#         for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
#             try:
#                 pid = proc.info['pid']
#                 name = proc.info['name']
#                 cpu = proc.info['cpu_percent']
#                 memory = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
#                 self.tree.insert("", "end", values=(pid, name, cpu, round(memory, 2)))
#             except (psutil.NoSuchProcess, psutil.AccessDenied):
#                 continue

#         # Schedule next update
#         self.root.after(1000, self.update_processes)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ProcessMonitor(root)
#     root.mainloop()





import tkinter as tk
from tkinter import ttk
import psutil
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 System Dashboard")
        self.root.geometry("900x600")
        self.root.configure(bg="#2C3E50")

        # Title Label
        title_label = tk.Label(root, text="📊 System Performance Dashboard", font=("Arial", 16, "bold"), fg="white", bg="#34495E")
        title_label.pack(fill=tk.X, pady=10)

        # Frames for Widgets
        self.info_frame = tk.Frame(root, bg="#2C3E50")
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # System Info Labels
        self.cpu_label = ttk.Label(self.info_frame, text="CPU Usage: ⏳", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")
        self.cpu_label.pack(pady=5)

        self.memory_label = ttk.Label(self.info_frame, text="Memory Usage: 🔄", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")
        self.memory_label.pack(pady=5)

        self.uptime_label = ttk.Label(self.info_frame, text="System Uptime: ⏱️", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")
        self.uptime_label.pack(pady=5)

        # Graph for CPU & Memory
        self.fig, self.axs = plt.subplots(2, 1, figsize=(5, 4), dpi=100)
        self.cpu_data = []
        self.memory_data = []
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.update_info()
        self.update_graphs()

    def update_info(self):
        """ Updates CPU, Memory, and Uptime information. """
        self.cpu_label.config(text=f"CPU Usage: {psutil.cpu_percent()}% 🔥")
        self.memory_label.config(text=f"Memory Usage: {psutil.virtual_memory().percent}% 🖥️")

        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        self.uptime_label.config(text=f"System Uptime: {uptime_hours}h {uptime_minutes}m ⏳")

        self.root.after(3000, self.update_info)  # Update every 3 sec

    def update_graphs(self):
        """ Updates the CPU and Memory usage graphs. """
        self.cpu_data.append(psutil.cpu_percent())
        self.memory_data.append(psutil.virtual_memory().percent)

        if len(self.cpu_data) > 50:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)

        self.axs[0].cla()
        self.axs[0].plot(self.cpu_data, color='red', label="CPU Usage %")
        self.axs[0].set_ylim(0, 100)
        self.axs[0].legend(loc="upper right")
        
        self.axs[1].cla()
        self.axs[1].plot(self.memory_data, color='blue', label="Memory Usage %")
        self.axs[1].set_ylim(0, 100)
        self.axs[1].legend(loc="upper right")

        self.canvas.draw()
        self.root.after(3000, self.update_graphs)  # Update every 3 sec

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
