import psutil
import time
import os
from prettytable import PrettyTable

def clear_console():
    """Clear the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_memory(mem_bytes):
    """Format memory size to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if mem_bytes < 1024:
            return f"{mem_bytes:.2f} {unit}"
        mem_bytes /= 1024
    return f"{mem_bytes:.2f} PB"

def display_process_info():
    """Display real-time process information."""
    while True:
        clear_console()
        table = PrettyTable(['PID', 'Name', 'CPU %', 'Memory Usage', 'Status', 'Threads'])
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'num_threads']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                memory = format_memory(proc.info['memory_info'].rss)
                status = proc.info['status']
                threads = proc.info['num_threads']

                table.add_row([pid, name, cpu, memory, status, threads])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print("Real-Time Process Monitoring Dashboard")
        print(table)
        print("Press Ctrl+C to exit.")
        time.sleep(1)

if __name__ == "__main__":
    display_process_info()




# import psutil
# import tkinter as tk
# from tkinter import ttk
# import threading
# import time
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class ProcessMonitorApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("🔍 Real-Time Process Monitor")
#         self.root.geometry("900x600")
#         self.root.configure(bg="#2C3E50")

#         # Title
#         title_label = tk.Label(root, text="⚡ Real-Time Process Monitor", font=("Arial", 16, "bold"), fg="white", bg="#34495E")
#         title_label.pack(fill=tk.X, pady=10)

#         # Table for process details
#         self.tree = ttk.Treeview(root, columns=("PID", "Name", "CPU %", "Memory %"), show="headings")
#         for col in ("PID", "Name", "CPU %", "Memory %"):
#             self.tree.heading(col, text=col)
#             self.tree.column(col, anchor=tk.CENTER)

#         self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

#         # Graphs for CPU & Memory Usage
#         self.fig, self.axs = plt.subplots(2, 1, figsize=(5, 4), dpi=100)
#         self.cpu_data = []
#         self.memory_data = []
        
#         self.canvas = FigureCanvasTkAgg(self.fig, master=root)
#         self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#         self.update_processes()
#         self.update_graphs()

#     def update_processes(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)

#         for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
#             try:
#                 self.tree.insert("", tk.END, values=(proc.info["pid"], proc.info["name"], f'{proc.info["cpu_percent"]:.1f}%', f'{proc.info["memory_percent"]:.1f}%'))
#             except psutil.NoSuchProcess:
#                 continue  

#         self.root.after(3000, self.update_processes)  # Auto-refresh every 3 sec

#     def update_graphs(self):
#         self.cpu_data.append(psutil.cpu_percent())
#         self.memory_data.append(psutil.virtual_memory().percent)

#         if len(self.cpu_data) > 50:
#             self.cpu_data.pop(0)
#             self.memory_data.pop(0)

#         self.axs[0].cla()
#         self.axs[0].plot(self.cpu_data, color='red', label="CPU Usage %")
#         self.axs[0].set_ylim(0, 100)
#         self.axs[0].legend(loc="upper right")
        
#         self.axs[1].cla()
#         self.axs[1].plot(self.memory_data, color='blue', label="Memory Usage %")
#         self.axs[1].set_ylim(0, 100)
#         self.axs[1].legend(loc="upper right")

#         self.canvas.draw()
#         self.root.after(3000, self.update_graphs)  # Update graphs every 3 sec

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ProcessMonitorApp(root)
#     root.mainloop()
