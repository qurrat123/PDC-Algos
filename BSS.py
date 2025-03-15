import numpy as np
import time
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class ProcessBSS:
    def __init__(self, id, num_processes, gui):
        """Initialize process with vector clock and buffer."""
        self.id = id
        self.num_processes = num_processes
        self.vector_clock = np.zeros(num_processes, dtype=int)  # Vector clock for this process
        self.buffer = []  # Buffer for out-of-order messages
        self.gui = gui  # Reference to GUI for updates

    def increment_clock(self):
        """Increment local clock before an event."""
        self.vector_clock[self.id] += 1

    def send_message(self, receiver, processes):
        """Send a message with a timestamp."""
        self.increment_clock()  # Update clock before sending
        timestamp = self.vector_clock.copy()

        message = {"sender": self.id, "timestamp": timestamp}
        self.gui.update_log(f"Process {self.id} SENT message to Process {receiver} with timestamp {timestamp}")

        # Simulating network delay
        time.sleep(1)

        # Deliver message to the receiver process
        processes[receiver].receive_message(message)
        self.gui.animate_message(self.id, receiver)  # Animate message flow

    def receive_message(self, message):
        """Receive a message and check if it can be delivered immediately."""
        sender = message["sender"]
        timestamp = message["timestamp"]

        self.gui.update_log(f"Process {self.id} RECEIVED message from Process {sender} with timestamp {timestamp}")

        # Causal Ordering Check
        if all(self.vector_clock[i] >= timestamp[i] for i in range(self.num_processes) if i != sender) and \
                self.vector_clock[sender] == timestamp[sender] - 1:
            self.deliver_message(message)
        else:
            self.buffer.append(message)
            self.gui.update_log(f"Process {self.id} BUFFERED message from Process {sender} due to missing dependencies.")

    def deliver_message(self, message):
        """Deliver a message and update vector clock."""
        sender = message["sender"]
        timestamp = message["timestamp"]

        # Merge vector clocks
        self.vector_clock = np.maximum(self.vector_clock, timestamp)
        self.gui.update_log(f"Process {self.id} DELIVERED message from Process {sender}. Updated vector clock: {self.vector_clock}")

        # Check and deliver buffered messages if dependencies are now met
        self.check_buffer()

    def check_buffer(self):
        """Check buffered messages and process them if dependencies are satisfied."""
        for message in self.buffer[:]:  # Iterate over a copy of the buffer
            sender = message["sender"]
            timestamp = message["timestamp"]

            if all(self.vector_clock[i] >= timestamp[i] for i in range(self.num_processes) if i != sender) and \
                    self.vector_clock[sender] == timestamp[sender] - 1:
                self.deliver_message(message)
                self.buffer.remove(message)  # Remove from buffer after delivery

class BSSGUI:
    def __init__(self, root):
        """Initialize the GUI and animation."""
        self.root = root
        self.root.title("BSS Algorithm - Causal Ordering Simulation")

        # Log display
        self.log_text = tk.Text(root, height=15, width=80)
        self.log_text.pack()

        self.processes = []
        self.num_processes = 3

        # Create processes
        for i in range(self.num_processes):
            self.processes.append(ProcessBSS(i, self.num_processes, self))

        # Create Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="P1 → P2 (M1)", command=lambda: self.processes[0].send_message(1, self.processes)).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="P2 → P3 (M2)", command=lambda: self.processes[1].send_message(2, self.processes)).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Out-of-Order P2 → P3 (M3)", command=lambda: self.processes[1].send_message(2, self.processes)).pack(side=tk.LEFT)

        # Create Matplotlib Figure for Animation
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Setup Process Lines
        self.process_lines = {0: "P1", 1: "P2", 2: "P3"}
        self.message_lines = []

        self.init_graph()

    def init_graph(self):
        """Initialize the graphical representation."""
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0, 1, 2])
        self.ax.set_yticklabels(["P1", "P2", "P3"])
        self.ax.set_title("Message Flow in BSS Algorithm")

        for i in range(3):
            self.ax.plot([0, 10], [i, i], "k--")  # Dashed lines for processes

        self.canvas.draw()

    def animate_message(self, sender, receiver):
        """Animate message movement."""
        x_data = [1, 2]
        y_data = [sender, receiver]

        line, = self.ax.plot(x_data, y_data, "bo-")  # Message path
        self.message_lines.append(line)

        self.canvas.draw()
        time.sleep(1)  # Pause before removing animation

        # Remove animation after delay
        line.remove()
        self.canvas.draw()

    def update_log(self, message):
        """Update the log output on the GUI."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BSSGUI(root)
    root.mainloop()
