import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pygame
import threading
import time
import math
from datetime import datetime

class SacredFrequencyGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sacred Frequency Generator v2.0")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")
        
        # Audio settings
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sample_rate = 44100
        self.is_playing = False
        self.current_thread = None
        self.volume = 0.3
        
        # Sacred frequencies database
        self.sacred_frequencies = {
            "174 Hz": {"freq": 174, "desc": "Pain Relief & Healing", "chakra": "Foundation"},
            "285 Hz": {"freq": 285, "desc": "Tissue Regeneration", "chakra": "Root"},
            "396 Hz": {"freq": 396, "desc": "Liberation from Fear", "chakra": "Root"},
            "417 Hz": {"freq": 417, "desc": "Change & Transformation", "chakra": "Sacral"},
            "432 Hz": {"freq": 432, "desc": "Natural Harmony", "chakra": "Heart"},
            "528 Hz": {"freq": 528, "desc": "Love & DNA Repair", "chakra": "Heart"},
            "639 Hz": {"freq": 639, "desc": "Relationships & Connection", "chakra": "Throat"},
            "741 Hz": {"freq": 741, "desc": "Intuition & Expression", "chakra": "Throat"},
            "852 Hz": {"freq": 852, "desc": "Spiritual Awakening", "chakra": "Third Eye"},
            "963 Hz": {"freq": 963, "desc": "Crown Activation", "chakra": "Crown"},
            "7.83 Hz": {"freq": 7.83, "desc": "Schumann Resonance", "chakra": "Earth"},
            "40 Hz": {"freq": 40, "desc": "Gamma Brain State", "chakra": "Mind"}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🕉 SACRED FREQUENCY GENERATOR 🕉", 
                              font=("Arial", 24, "bold"), fg="#e94560", bg="#1a1a2e")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Consciousness Calibration & Healing Tool", 
                                 font=("Arial", 12), fg="#f5f5f5", bg="#1a1a2e")
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Left panel - Frequency selection
        left_frame = tk.LabelFrame(main_frame, text="Sacred Frequencies", 
                                  font=("Arial", 14, "bold"), fg="#e94560", bg="#16213e", 
                                  relief="groove", bd=2)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Frequency listbox
        self.freq_listbox = tk.Listbox(left_frame, font=("Arial", 10), bg="#0f3460", 
                                      fg="#f5f5f5", selectbackground="#e94560", 
                                      selectforeground="white", height=8)
        self.freq_listbox.pack(pady=10, padx=10, fill="both", expand=True)
        
        for freq_name in self.sacred_frequencies.keys():
            self.freq_listbox.insert(tk.END, freq_name)
        
        # Frequency info
        self.info_label = tk.Label(left_frame, text="Select a frequency to see details", 
                                  font=("Arial", 10), fg="#f5f5f5", bg="#16213e", 
                                  wraplength=250, justify="center")
        self.info_label.pack(pady=5)
        
        self.freq_listbox.bind('<<ListboxSelect>>', self.on_frequency_select)
        
        # Right panel - Controls
        right_frame = tk.LabelFrame(main_frame, text="Consciousness Controls", 
                                   font=("Arial", 14, "bold"), fg="#e94560", bg="#16213e", 
                                   relief="groove", bd=2)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Play controls
        control_frame = tk.Frame(right_frame, bg="#16213e")
        control_frame.pack(pady=20)
        
        self.play_button = tk.Button(control_frame, text="▶ Activate Frequency", 
                                    command=self.toggle_playback, font=("Arial", 12, "bold"),
                                    bg="#e94560", fg="white", relief="raised", bd=3,
                                    width=15, height=2)
        self.play_button.pack(pady=5)
        
        # Volume control
        volume_frame = tk.Frame(right_frame, bg="#16213e")
        volume_frame.pack(pady=10)
        
        tk.Label(volume_frame, text="Sacred Volume:", font=("Arial", 10, "bold"), 
                fg="#f5f5f5", bg="#16213e").pack()
        
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient="horizontal",
                                    bg="#16213e", fg="#f5f5f5", highlightbackground="#16213e",
                                    command=self.update_volume, length=200)
        self.volume_scale.set(30)
        self.volume_scale.pack()
        
        # Binaural beats
        binaural_frame = tk.LabelFrame(right_frame, text="Binaural Enhancement", 
                                      font=("Arial", 12, "bold"), fg="#e94560", bg="#16213e")
        binaural_frame.pack(pady=10, padx=10, fill="x")
        
        self.binaural_var = tk.BooleanVar()
        self.binaural_check = tk.Checkbutton(binaural_frame, text="Enable Binaural Beats",
                                           variable=self.binaural_var, font=("Arial", 10),
                                           fg="#f5f5f5", bg="#16213e", selectcolor="#0f3460")
        self.binaural_check.pack()
        
        tk.Label(binaural_frame, text="Beat Frequency (Hz):", font=("Arial", 9), 
                fg="#f5f5f5", bg="#16213e").pack()
        
        self.beat_freq_scale = tk.Scale(binaural_frame, from_=1, to=40, orient="horizontal",
                                       bg="#16213e", fg="#f5f5f5", highlightbackground="#16213e",
                                       length=150)
        self.beat_freq_scale.set(10)
        self.beat_freq_scale.pack()
        
        # Custom frequency
        custom_frame = tk.LabelFrame(right_frame, text="Custom Frequency", 
                                    font=("Arial", 12, "bold"), fg="#e94560", bg="#16213e")
        custom_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(custom_frame, text="Frequency (Hz):", font=("Arial", 9), 
                fg="#f5f5f5", bg="#16213e").pack()
        
        self.custom_freq_entry = tk.Entry(custom_frame, font=("Arial", 10), 
                                         bg="#0f3460", fg="#f5f5f5", justify="center")
        self.custom_freq_entry.pack(pady=5)
        
        self.custom_button = tk.Button(custom_frame, text="Activate Custom", 
                                      command=self.play_custom_frequency, 
                                      font=("Arial", 9), bg="#e94560", fg="white")
        self.custom_button.pack(pady=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#0f3460", height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready for consciousness calibration...", 
                                    font=("Arial", 10), fg="#f5f5f5", bg="#0f3460")
        self.status_label.pack(side="left", padx=10, pady=5)
        
        self.time_label = tk.Label(status_frame, text="", font=("Arial", 10), 
                                  fg="#e94560", bg="#0f3460")
        self.time_label.pack(side="right", padx=10, pady=5)
        
        self.update_time()
        
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Sacred Time: {current_time}")
        self.root.after(1000, self.update_time)
        
    def on_frequency_select(self, event):
        selection = self.freq_listbox.curselection()
        if selection:
            freq_name = self.freq_listbox.get(selection[0])
            freq_data = self.sacred_frequencies[freq_name]
            info_text = f"{freq_name}\n\n{freq_data['desc']}\n\nChakra: {freq_data['chakra']}"
            self.info_label.config(text=info_text)
    
    def update_volume(self, value):
        self.volume = float(value) / 100.0
        
    def generate_tone(self, frequency, duration=1.0, binaural_beat=0):
        frames = int(duration * self.sample_rate)
        
        if binaural_beat > 0:
            # Generate binaural beats
            left_freq = frequency
            right_freq = frequency + binaural_beat
            
            left_wave = np.sin(2 * np.pi * left_freq * np.linspace(0, duration, frames))
            right_wave = np.sin(2 * np.pi * right_freq * np.linspace(0, duration, frames))
            
            # Apply volume and create stereo array
            left_wave = (left_wave * self.volume * 32767).astype(np.int16)
            right_wave = (right_wave * self.volume * 32767).astype(np.int16)
            
            stereo_wave = np.column_stack((left_wave, right_wave))
        else:
            # Generate mono tone
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
            wave = (wave * self.volume * 32767).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
        
        return stereo_wave
    
    def play_frequency(self, frequency):
        try:
            binaural_beat = self.beat_freq_scale.get() if self.binaural_var.get() else 0
            
            while self.is_playing:
                tone = self.generate_tone(frequency, duration=2.0, binaural_beat=binaural_beat)
                
                # Convert to pygame sound
                sound = pygame.sndarray.make_sound(tone)
                sound.play()
                
                time.sleep(1.8)  # Small gap between repetitions
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Audio generation failed: {str(e)}"))
            self.is_playing = False
            self.root.after(0, self.update_play_button)
    
    def toggle_playback(self):
        if self.is_playing:
            self.stop_frequency()
        else:
            selection = self.freq_listbox.curselection()
            if selection:
                freq_name = self.freq_listbox.get(selection[0])
                frequency = self.sacred_frequencies[freq_name]["freq"]
                self.start_frequency(frequency)
            else:
                messagebox.showwarning("Warning", "Please select a sacred frequency first.")
    
    def start_frequency(self, frequency):
        if not self.is_playing:
            self.is_playing = True
            self.current_thread = threading.Thread(target=self.play_frequency, args=(frequency,))
            self.current_thread.daemon = True
            self.current_thread.start()
            self.update_play_button()
            self.status_label.config(text=f"Generating {frequency} Hz sacred frequency...")
    
    def stop_frequency(self):
        self.is_playing = False
        pygame.mixer.stop()
        if self.current_thread:
            self.current_thread.join(timeout=1)
        self.update_play_button()
        self.status_label.config(text="Frequency stopped. Ready for consciousness calibration...")
    
    def update_play_button(self):
        if self.is_playing:
            self.play_button.config(text="⏸ Stop Frequency", bg="#f39c12")
        else:
            self.play_button.config(text="▶ Activate Frequency", bg="#e94560")
    
    def play_custom_frequency(self):
        try:
            custom_freq = float(self.custom_freq_entry.get())
            if 0.1 <= custom_freq <= 20000:
                self.stop_frequency()  # Stop any current playback
                self.start_frequency(custom_freq)
            else:
                messagebox.showwarning("Warning", "Please enter a frequency between 0.1 and 20000 Hz.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for frequency.")
    
    def run(self):
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            self.cleanup()
    
    def on_closing(self):
        self.stop_frequency()
        self.cleanup()
        self.root.destroy()
    
    def cleanup(self):
        self.is_playing = False
        pygame.mixer.quit()

if __name__ == "__main__":
    app = SacredFrequencyGenerator()
    app.run()