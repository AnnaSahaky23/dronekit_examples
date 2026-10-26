import tkinter as tk
from tkinter import messagebox
from dronekit import connect, VehicleMode


class GroundControlStation:
    def __init__(self, root):
        self.root = root
        self.root.title("Ground Control Station")
        self.root.geometry("380x460")
        self.root.configure(bg="#252A27")
        self.vehicle = None

        self.create_widgets()

    def create_widgets(self):
        conn_frame = tk.LabelFrame(self.root, text="Connection Settings", padx=10, pady=10, bg="#252A27", fg="white")
        conn_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(conn_frame, text="Connection String:", bg="#252A27", fg="white").pack(anchor="w")

        self.conn_entry = tk.Entry(conn_frame)
        self.conn_entry.insert(0, "tcp:host.docker.internal:5763")
        self.conn_entry.pack(fill="x", pady=5)

        btn_frame = tk.Frame(conn_frame, bg="#252A27")
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="Connect", command=self.connect_vehicle, bg="#C8E6C9", fg="#1B4332"
                  ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        tk.Button(btn_frame, text="Close Connection", command=self.close_connection, bg="#2D6A4F", fg="white"
                  ).pack(side="right", expand=True, fill="x", padx=(5, 0))

        control_frame = tk.LabelFrame(self.root, text="Flight Controls", padx=10, pady=10, bg="#252A27", fg="white")
        control_frame.pack(fill="x", padx=15, pady=5)

        tk.Button(control_frame, text="Arm", command=self.arm_vehicle, bg="#FFF0B3", fg="#5D4E00"
                  ).pack(fill="x", pady=5)

        tk.Label(control_frame, text="Flight Modes:", bg="#252A27", fg="white").pack(anchor="w", pady=5)

        modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]

        for mode in modes:
            tk.Button(control_frame, text=mode, command=lambda m=mode: self.change_mode(m), bg="#E8ECE9", fg="#333333"
                      ).pack(fill="x", pady=2)

        self.status_label = tk.Label(self.root, text="Status: Disconnected", bg="#252A27", fg="white", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def connect_vehicle(self):
        try:
            conn_string = self.conn_entry.get().strip()
            self.status_label.config(text="Connecting...")
            self.root.update()

            self.vehicle = connect(conn_string, wait_ready=True, timeout=30)
            self.status_label.config(text="Status: Connected")
        except Exception as e:
            self.status_label.config(text="Status: Connection Failed")
            messagebox.showerror("Error", str(e))

    def close_connection(self):
        if self.vehicle is not None:
            try:
                self.vehicle.close()
                self.vehicle = None
                self.status_label.config(text="Status: Disconnected")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "No active connection")

    def arm_vehicle(self):
        if self.vehicle is None:
            messagebox.showwarning("Warning", "Connect first!")
            return

        try:
            self.vehicle.armed = True
            self.status_label.config(text="Status: Arming...")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_mode(self, mode):
        if self.vehicle is None:
            messagebox.showwarning("Warning", "Connect first!")
            return

        try:
            self.vehicle.mode = VehicleMode(mode)
            self.status_label.config(text=f"Status: Mode -> {mode}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = GroundControlStation(root)
    root.mainloop()