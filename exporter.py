import csv
from tkinter import messagebox

def export_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Table ki heading
            writer.writerow(["Timestamp", "Severity", "Message"]) 
            # Saara data likhna
            writer.writerows(data)
        messagebox.showinfo("Success", "File Excel (CSV) me save ho gayi hai!")
    except Exception as e:
        messagebox.showerror("Error", f"File save nahi ho payi: {e}")