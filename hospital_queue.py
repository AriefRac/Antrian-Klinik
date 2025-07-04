import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class KlinikQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Sistem Antrian Klinik Kurniawan")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Data antrian
        self.queue_data = {
            'Umum': [],
            'Poli Gigi': [],
        }
        
        self.queue_counters = {
            'Umum': 1,
            'Poli Gigi': 1
        }
        
        self.current_queue = {
            'Umum': 0,
            'Poli Gigi': 0
        }
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#40C9FF', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🏥 Sistem Antrian Klinik Kurniawan", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#40C9FF')
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Form input
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 10), pady=0, ipadx=20, ipady=20)
        
        tk.Label(left_frame, text="📝 PENDAFTARAN ANTRIAN", 
                font=('Arial', 16, 'bold'), bg='white', fg='#40C9FF').pack(pady=(0, 20))
        
        # Form fields
        tk.Label(left_frame, text="Nama Pasien:", font=('Arial', 12), bg='white').pack(anchor='w')
        self.name_entry = tk.Entry(left_frame, font=('Arial', 12), width=25, relief='solid', bd=1)
        self.name_entry.pack(pady=(5, 15), ipady=5)
        
        tk.Label(left_frame, text="No. Identitas (KTP/SIM):", font=('Arial', 12), bg='white').pack(anchor='w')
        self.id_entry = tk.Entry(left_frame, font=('Arial', 12), width=25, relief='solid', bd=1)
        self.id_entry.pack(pady=(5, 15), ipady=5)
        
        tk.Label(left_frame, text="Pilih Layanan:", font=('Arial', 12), bg='white').pack(anchor='w')
        self.service_var = tk.StringVar(value='Umum')
        service_combo = ttk.Combobox(left_frame, textvariable=self.service_var, 
                                   values=list(self.queue_data.keys()), 
                                   state='readonly', font=('Arial', 12), width=22)
        service_combo.pack(pady=(5, 15), ipady=5)
        
        tk.Label(left_frame, text="Keluhan/Catatan:", font=('Arial', 12), bg='white').pack(anchor='w')
        self.complaint_text = tk.Text(left_frame, height=4, width=25, font=('Arial', 10), 
                                    relief='solid', bd=1, wrap='word')
        self.complaint_text.pack(pady=(5, 20))
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=10)
        
        add_btn = tk.Button(btn_frame, text="➕ Daftar Antrian", 
                          command=self.add_to_queue, bg='#48bb78', fg='white',
                          font=('Arial', 12, 'bold'), relief='flat', pady=10)
        add_btn.pack(fill='x', pady=(0, 10))
        
        next_btn = tk.Button(btn_frame, text="▶️ Panggil Berikutnya", 
                           command=self.call_next, bg='#165ACD', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', pady=10)
        next_btn.pack(fill='x', pady=(0, 10))
        
        reset_btn = tk.Button(btn_frame, text="🔄 Reset Antrian", 
                            command=self.reset_queue, bg='#f56565', fg='white',
                            font=('Arial', 12, 'bold'), relief='flat', pady=10)
        reset_btn.pack(fill='x')
        
        # Right panel - Display
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=0, pady=0)
        
        # Display header
        display_header = tk.Frame(right_frame, bg='#40C9FF', height=60)
        display_header.pack(fill='x')
        display_header.pack_propagate(False)
        
        tk.Label(display_header, text="📊 STATUS ANTRIAN SAAT INI", 
                font=('Arial', 18, 'bold'), fg='white', bg='#40C9FF').pack(pady=15)
        
        # Current patient display
        self.current_frame = tk.Frame(right_frame, bg='#e6fffa', relief='solid', bd=2)
        self.current_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(self.current_frame, text="🔔 SEKARANG DILAYANI", 
                font=('Arial', 14, 'bold'), bg='#e6fffa', fg='#40C9FF').pack(pady=10)
        
        self.current_label = tk.Label(self.current_frame, text="Belum ada antrian", 
                                    font=('Arial', 20, 'bold'), bg='#e6fffa', fg='#d53f8c')
        self.current_label.pack(pady=10)
        
        # Queue display
        queue_container = tk.Frame(right_frame, bg='white')
        queue_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(queue_container, bg='white')
        scrollbar = ttk.Scrollbar(queue_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Siap menerima pendaftaran", 
                                 relief='sunken', anchor='w', bg='#e2e8f0', 
                                 font=('Arial', 10))
        self.status_bar.pack(side='bottom', fill='x')
        
    def add_to_queue(self):
        name = self.name_entry.get().strip()
        id_num = self.id_entry.get().strip()
        service = self.service_var.get()
        complaint = self.complaint_text.get("1.0", tk.END).strip()
        
        if not name or not id_num:
            messagebox.showerror("Error", "Nama dan No. Identitas harus diisi!")
            return
        
        # Generate queue number
        if service == "Umum":
            queue_num = f"U{self.queue_counters[service]:03d}"
        else:
            queue_num = f"G{self.queue_counters[service]:03d}"
        
        patient_data = {
            'queue_number': queue_num,
            'name': name,
            'id_number': id_num,
            'service': service,
            'complaint': complaint,
            'time_registered': datetime.now().strftime("%H:%M:%S"),
            'status': 'Menunggu'
        }
        
        self.queue_data[service].append(patient_data)
        self.queue_counters[service] += 1
        
        # Clear form
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.complaint_text.delete("1.0", tk.END)
        
        self.update_display()
        
        messagebox.showinfo("Berhasil", f"Antrian berhasil didaftarkan!\nNomor antrian: {queue_num}")
        self.status_bar.config(text=f"Pasien {name} berhasil didaftarkan dengan nomor {queue_num}")
        
    def call_next(self):
        service = self.service_var.get()
        
        if not self.queue_data[service]:
            messagebox.showwarning("Peringatan", f"Tidak ada antrian untuk {service}")
            return
        
        if self.current_queue[service] >= len(self.queue_data[service]):
            messagebox.showinfo("Info", f"Semua antrian {service} sudah dipanggil")
            return
        
        if self.current_queue[service] > 0:
            previous_patient = self.queue_data[service][self.current_queue[service] - 1]
            previous_patient['status'] = 'Selesai'
            previous_patient['time_finished'] = datetime.now().strftime("%H:%M:%S")
        
        # Panggil antrian berikutnya
        current_patient = self.queue_data[service][self.current_queue[service]]
        current_patient['status'] = 'Sedang Dilayani'
        current_patient['time_called'] = datetime.now().strftime("%H:%M:%S")
        self.current_queue[service] += 1
        
        self.update_display()
        
        messagebox.showinfo("Panggilan", 
                          f"Memanggil:\n{current_patient['queue_number']} - {current_patient['name']}\n"
                          f"Layanan: {service}")
        
        self.status_bar.config(text=f"Memanggil {current_patient['queue_number']} - {current_patient['name']}")
        
    def reset_queue(self):
        if messagebox.askyesno("Konfirmasi", "Reset semua antrian? Data akan hilang!"):
            for service in self.queue_data:
                self.queue_data[service] = []
                self.queue_counters[service] = 1
                self.current_queue[service] = 0
            
            self.update_display()
            messagebox.showinfo("Berhasil", "Semua antrian telah direset")
            self.status_bar.config(text="Semua antrian telah direset")
    
    def update_display(self):
        # Clear scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Update current patient display
        current_text = "Belum ada antrian aktif"
        for service in self.queue_data:
            if self.current_queue[service] > 0 and self.current_queue[service] <= len(self.queue_data[service]):
                patient = self.queue_data[service][self.current_queue[service] - 1]
                if patient['status'] == 'Sedang Dilayani':
                    current_text = f"{patient['queue_number']} - {patient['name']}\n{service}"
                    break
        
        self.current_label.config(text=current_text)
        
        # Display all queues
        row = 0
        for service, patients in self.queue_data.items():
            if not patients:
                continue
                
            # Service header
            service_frame = tk.Frame(self.scrollable_frame, bg='#4a5568', relief='raised', bd=1)
            service_frame.grid(row=row, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            
            tk.Label(service_frame, text=f"🏥 {service}", 
                    font=('Arial', 14, 'bold'), fg='white', bg='#4a5568').pack(pady=8)
            row += 1
            
            # Column headers
            headers = ["No. Antrian", "Nama", "Waktu Daftar", "Status"]
            for col, header in enumerate(headers):
                tk.Label(self.scrollable_frame, text=header, font=('Arial', 11, 'bold'), 
                        bg='#e2e8f0', relief='solid', bd=1).grid(
                        row=row, column=col, sticky='ew', padx=1, pady=1, ipady=5)
            row += 1
            
            # Patient data
            for patient in patients:
                if patient['status'] == 'Sedang Dilayani':
                    bg_color = '#fff5f5'
                elif patient['status'] == 'Selesai':
                    bg_color = '#f0fff4'
                else:
                    bg_color = '#f7fafc'
                
                tk.Label(self.scrollable_frame, text=patient['queue_number'], 
                        bg=bg_color, relief='solid', bd=1, font=('Arial', 10)).grid(
                        row=row, column=0, sticky='ew', padx=1, pady=1, ipady=8)
                
                tk.Label(self.scrollable_frame, text=patient['name'], 
                        bg=bg_color, relief='solid', bd=1, font=('Arial', 10)).grid(
                        row=row, column=1, sticky='ew', padx=1, pady=1, ipady=8)
                
                tk.Label(self.scrollable_frame, text=patient['time_registered'], 
                        bg=bg_color, relief='solid', bd=1, font=('Arial', 10)).grid(
                        row=row, column=2, sticky='ew', padx=1, pady=1, ipady=8)
                
                if patient['status'] == 'Sedang Dilayani':
                    status_color = '#e53e3e'
                elif patient['status'] == 'Selesai':
                    status_color = '#38a169'
                else:
                    status_color = '#718096'
                    
                tk.Label(self.scrollable_frame, text=patient['status'], 
                        bg=bg_color, fg=status_color, relief='solid', bd=1, 
                        font=('Arial', 10, 'bold')).grid(
                        row=row, column=3, sticky='ew', padx=1, pady=1, ipady=8)
                
                row += 1
            
            # Add spacing between services
            tk.Frame(self.scrollable_frame, height=10, bg='white').grid(row=row, column=0, columnspan=4)
            row += 1
        
        # Configure column weights
        for col in range(4):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)

def main():
    root = tk.Tk()
    app = KlinikQueueApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()