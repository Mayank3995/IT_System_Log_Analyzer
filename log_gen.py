import time
import random
from datetime import datetime

levels = ["INFO", "WARNING", "ERROR"]
messages = [
    "User login attempt successful",
    "High CPU usage detected",
    "Database connection timeout",
    "Firewall blocked suspicious IP",
    "Unauthorized access attempt",
    "System backup completed",
    "Memory leak in service 'auth'",
    "New device connected to network"
]

print("Log Generator Shuru ho gaya hai... (Band karne ke liye Ctrl+C dabayein)")

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choices(levels, weights=[70, 20, 10])[0] # Zyada INFO, kam ERROR
    msg = random.choice(messages)
    
    log_line = f"{now} {level} {msg}\n"
    
    with open("sample.log", "a") as f:
        f.write(log_line)
        print(f"Naya Log: {log_line.strip()}")
    
    time.sleep(2) # Har 2 second me naya data