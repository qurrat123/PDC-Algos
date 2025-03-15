# Distributed Systems - Causal Ordering Algorithms

This repository contains Python implementations for **causal message ordering algorithms** used in **distributed systems**. The implemented algorithms are:

- **BSS (Birman-Schiper-Stephenson) Algorithm**
- **SES (Schiper-Eggli-Sandoz) Algorithm**
- **Matrix Clock Algorithm**

Each algorithm maintains **causal ordering** in message-passing systems by ensuring **correct event sequencing** across multiple processes.

---

## 📌 **Algorithms Overview**

### **1️⃣ BSS Algorithm**
The **BSS (Birman-Schiper-Stephenson) Algorithm** uses **vector clocks** to track the causal order of events in a distributed system. Messages are **buffered** until all preceding messages are delivered.

### **2️⃣ SES Algorithm**
The **SES (Schiper-Eggli-Sandoz) Algorithm** improves upon the BSS algorithm by embedding vector timestamps in messages to **reduce buffering and dependencies**.

### **3️⃣ Matrix Clock Algorithm**
The **Matrix Clock Algorithm** extends vector clocks by maintaining a **full matrix of timestamps** across all processes, ensuring **stronger consistency**.

---

## 📌 **How to Run the Codes**
Each algorithm is implemented in **Python** and comes with both **GUI-based** and **Non-GUI** versions.

### **🔹 Prerequisites**
Ensure you have **Python 3.x** installed on your system. If running GUI-based versions, install `tkinter` (pre-installed with Python).

```sh
# Install required dependencies (if needed)
pip install numpy




Running BSS Algorithm
python BSS.py


Running SES Algorithm
python SES.py

Running Matrix Clock Algorithm
python Matric_Clock.py