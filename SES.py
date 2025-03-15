import numpy as np
import time
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class ProcessSES:
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

    def send_message(self, receiver, processes, message_label):
        """Send a message with a timestamp."""
        self.increment_clock()
        timestamp = self.vector_clock.copy()

        message = {"sender": self.id, "receiver": receiver, "timestamp": timestamp, "label": message_label}
        self.gui.update_log(f"Process {self.id} SENT message {message_label} to Process {receiver} with timestamp {timestamp}")

        # Simulating network delay
        time.sleep(1)

        # Deliver message to the receiver process
        processes[receiver].receive_message(message)
        self.gui.animate_message(self.id, receiver, message_label, timestamp)  # Animate message flow

    def receive_message(self, message):
        """Receive a message and check if it can be delivered immediately."""
        sender = message["sender"]
        timestamp = message["timestamp"]
        message_label = message["label"]

        self.gui.update_log(f"Process {self.id} RECEIVED message {message_label} from Process {sender} with timestamp {timestamp}")

        # SES only checks the dependency on the sender
        if self.vector_clock[sender] == timestamp[sender] - 1:
            self.deliver_message(message)
        else:
            self.buffer.append(message)
            self.gui.update_log(f"Process {self.id} BUFFERED message {message_label} from Process {sender} due to missing dependencies.")

    def deliver_message(self, message):
        """Deliver a message and update vector clock."""
        sender = message["sender"]
        timestamp = message["timestamp"]
        message_label = message["label"]

        # Merge vector clocks
        self.vector_clock = np.maximum(self.vector_clock, timestamp)
        self.gui.update_log(f"Process {self.id} DELIVERED message {message_label} from Process {sender}. Updated clock: {self.vector_clock}")

        # Check and deliver buffered messages if dependencies are now met
        self.check_buffer()

    def check_buffer(self):
        """Check buffered messages and process them if dependencies are satisfied."""
        for message in self.buffer[:]:  # Iterate over a copy of the buffer
            sender = message["sender"]
            timestamp = message["timestamp"]
            message_label = message["label"]

            if self.vector_clock[sender] == timestamp[sender] - 1:
                self.deliver_message(message)
                self.buffer.remove(message)  # Remove from buffer after delivery

class SESGUI:
    def __init__(self, root):
        """Initialize the GUI and animation."""
        self.root = root
        self.root.title("SES Algorithm - Causal Ordering Simulation")

        # Log display
        self.log_text = tk.Text(root, height=12, width=80, bg="black", fg="white")
        self.log_text.pack()

        self.processes = []
        self.num_processes = 3

        # Create processes
        for i in range(self.num_processes):
            self.processes.append(ProcessSES(i, self.num_processes, self))

        # Create Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="P1 → P3 (m0)", command=lambda: self.processes[0].send_message(2, self.processes, "m0")).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="P1 → P2 (m1)", command=lambda: self.processes[0].send_message(1, self.processes, "m1")).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Out-of-Order P2 → P3 (m2)", command=lambda: self.processes[1].send_message(2, self.processes, "m2")).pack(side=tk.LEFT)

        # Create Matplotlib Figure for Animation
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Setup Process Lines
        self.process_lines = {0: "P1", 1: "P2", 2: "P3"}
        self.message_points = []

        self.init_graph()

    def init_graph(self):
        """Initialize the graphical representation."""
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0, 1, 2])
        self.ax.set_yticklabels(["P1", "P2", "P3"])
        self.ax.set_title("Message Flow in SES Algorithm")

        # Draw process timelines
        for i in range(3):
            self.ax.plot([0, 10], [i, i], "k--")  # Dashed lines for processes

        self.canvas.draw()

    def animate_message(self, sender, receiver, message_label, timestamp):
        """Animate message movement and show labels on process lines."""
        x_data = [1, 2]
        y_data = [sender, receiver]

        # Plot message movement
        line, = self.ax.plot(x_data, y_data, "ro-", markersize=8, linewidth=2)  # Message path (red)
        self.message_points.append(line)

        # Label messages at endpoints
        self.ax.text(1, sender, f"{message_label}({timestamp})", fontsize=10, color="blue", verticalalignment='bottom', horizontalalignment='right')
        self.ax.text(2, receiver, f"{message_label}", fontsize=10, color="green", verticalalignment='bottom', horizontalalignment='left')

        self.canvas.draw()
        time.sleep(1)  # Pause before removing animation

    def update_log(self, message):
        """Update the log output on the GUI."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SESGUI(root)
    root.mainloop()
