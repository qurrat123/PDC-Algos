import copy

# Define Process Names
PROCESS_NAMES = ["P1", "P2", "P3"]

def initial_matrix():
    """Creates an initial matrix clock with all values set to 0."""
    return {p: {q: 0 for q in PROCESS_NAMES} for p in PROCESS_NAMES}

def matrix_to_string(mc):
    """Convert matrix clock (dict-of-dict) into a printable string format."""
    return "\n".join([f"{p}: {list(mc[p].values())}" for p in PROCESS_NAMES])

class Message:
    def __init__(self, msg_id, sender, matrix_snapshot):
        self.msg_id = msg_id
        self.sender = sender
        self.matrix = matrix_snapshot  # Copy of sender's matrix clock

def is_deliverable(process, message):
    """
    A message sent by process i is deliverable at process j if:
    - message.matrix[i][i] == process.matrix[i][i] + 1  (sender's diagonal entry)
    - for all k ≠ i, message.matrix[k][k] ≤ process.matrix[k][k]
    """
    sender = message.sender
    local_matrix = process.matrix
    
    # Check sender's diagonal entry
    if message.matrix[sender][sender] != local_matrix[sender][sender] + 1:
        return False
    
    # Check all other diagonal entries
    for p in PROCESS_NAMES:
        if p != sender and message.matrix[p][p] > local_matrix[p][p]:
            return False
    
    return True

class Process:
    def __init__(self, name):
        self.name = name
        self.matrix = initial_matrix()  # Initialize matrix clock
        self.delivered = []
        self.pending = []  # Buffered messages for later delivery

    def send_message(self, receiver, message_id):
        """
        When a process sends a message:
        - It increments its own diagonal entry in the matrix.
        - The message carries a snapshot of the sender's current matrix clock.
        """
        self.matrix[self.name][self.name] += 1  # Increment self diagonal
        snapshot = copy.deepcopy(self.matrix)
        print(f"{self.name} sends {message_id} to {receiver}, Matrix before send:")
        print(matrix_to_string(self.matrix), "\n")
        return Message(message_id, self.name, snapshot)

    def receive_message(self, message):
        """
        When a message is received:
        - If it's causally deliverable, merge clocks and update the matrix.
        - Otherwise, buffer the message until it becomes deliverable.
        """
        print(f"{self.name} receives {message.msg_id} from {message.sender}, Matrix before receive:")
        print(matrix_to_string(self.matrix), "\n")
        
        if is_deliverable(self, message):
            self.deliver_message(message)
            self.try_deliver_pending()
        else:
            print(f"{self.name} buffers {message.msg_id} (waiting for causal order)\n")
            self.pending.append(message)

    def deliver_message(self, message):
        """
        Delivers a message:
        - Merge the received matrix with the local matrix (component-wise max).
        - Increment the receiver's diagonal entry.
        """
        self.delivered.append(message.msg_id)

        # Merge matrices (element-wise max)
        for p in PROCESS_NAMES:
            for q in PROCESS_NAMES:
                self.matrix[p][q] = max(self.matrix[p][q], message.matrix[p][q])
        
        # Increment own diagonal entry
        self.matrix[self.name][self.name] += 1

        print(f"{self.name} delivers {message.msg_id}, Updated Matrix:")
        print(matrix_to_string(self.matrix), "\n")

    def try_deliver_pending(self):
        """
        Try delivering any buffered messages that can now be delivered.
        This process continues until no more messages can be delivered.
        """
        delivered_now = True
        while delivered_now:
            delivered_now = False
            for msg in self.pending[:]:  # Iterate over buffered messages
                if is_deliverable(self, msg):
                    self.pending.remove(msg)
                    self.deliver_message(msg)
                    delivered_now = True  # Continue checking after delivery

# Simulation of Matrix Clock with Message Passing
def run_simulation():
    print("\n====== Matrix Clock Simulation ======\n")

    # Create processes
    P1, P2, P3 = Process("P1"), Process("P2"), Process("P3")

    # Send Messages
    m1 = P1.send_message("P2", "M1")
    m2 = P1.send_message("P3", "M2")

    # P2 receives M1 first
    print("P2 receives M1:")
    P2.receive_message(m1)

    # P3 receives M2 first
    print("P3 receives M2:")
    P3.receive_message(m2)

    # P2 sends M3 to P3
    m3 = P2.send_message("P3", "M3")
    
    # P3 receives M3
    print("P3 receives M3:")
    P3.receive_message(m3)

    # P3 sends M4 to P1
    m4 = P3.send_message("P1", "M4")
    
    # P1 receives M4
    print("P1 receives M4:")
    P1.receive_message(m4)

    # P1 sends M5 to P2
    m5 = P1.send_message("P2", "M5")
    
    # P2 receives M5
    print("P2 receives M5:")
    P2.receive_message(m5)

    # Final Matrix Clocks
    print("\n===== Final Matrix Clocks =====")
    print("P1:\n", matrix_to_string(P1.matrix), "\n")
    print("P2:\n", matrix_to_string(P2.matrix), "\n")
    print("P3:\n", matrix_to_string(P3.matrix), "\n")

# Run the simulation
run_simulation()
