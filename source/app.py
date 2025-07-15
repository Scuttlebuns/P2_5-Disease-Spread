import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
import pygame
from controls import create_controls
from simulation_canvas import SimulationCanvas
from graph import SIRGraph
from simulation_engine import SIRSimulation

class App:
    def __init__(self):
        # Set up root window, GUI, buttons, and music
        self._setup_root()
        self._setup_gui()
        self._bind_controls()
        self._init_music()
        
    def _setup_root(self):
        # Set up root window
        self.root = tk.Tk()
        self.root.title("SIR Infection Simulation")
        self.root.resizable(False, False) 
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)

    def _setup_gui(self):
        # Control Panel
        self.controls_frame, self.params, self.start_btn, self.pause_btn, self.reset_btn  = create_controls(self.root)
        self.controls_frame.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = (10, 5))

        # Main layout frame
        self.sim_and_graph = ttk.Frame(self.root, padding = 0)
        self.sim_and_graph.grid(row = 1, column = 0)
        self.sim_and_graph.grid_columnconfigure(0, weight = 1)
        self.sim_and_graph.grid_columnconfigure(1, weight = 1)
        self.sim_and_graph.grid_rowconfigure(0, weight = 1)

        # Canvas
        self.canvas_width = 275
        self.canvas_height = 700
        self.canvas_frame = ttk.Frame(self.sim_and_graph, width = self.canvas_width + 5, height = self.canvas_height + 5)
        self.canvas_frame.grid(row = 0, column = 0, sticky = "nsew", padx = (20,10))
        self.canvas_frame.grid_propagate(False)
        self.canvas = SimulationCanvas(self.canvas_frame)
        self.canvas.place(x = 0, y = 0, width= self.canvas_width, height= self.canvas_height)

        # Graph
        self.graph = SIRGraph(self.sim_and_graph)
        self.graph.grid(row = 0, column = 1, sticky = "nsew", padx = (10,20))

        # Status label
        self.status_label = tk.Label(self.root, text = "Time: 0 | S: 0 | I: 0 | R: 0", padx = 5)
        self.status_label.grid(row = 2, column = 0, sticky = "w", padx = 10)

        # Sim setup
        self.simulation = SIRSimulation(width = self.canvas_width, height = self.canvas_height)
        self.running = False
        self.time_step = 0
        self.loop_id = None

    def _bind_controls(self):
        # Button bindings
        self.start_btn.config(command = self.start)
        self.pause_btn.config(command = self.pause)
        self.reset_btn.config(command = self.reset)

    def _init_simulation(self):
        self.simulation.population_size = int(self.params["Population Size"].get())
        self.simulation.initial_infected = int(self.params["Initial Infected"].get())
        self.simulation.infection_rate = float(self.params["Infection Rate (%)"].get())
        # Convert to value between 0 and 1
        self.simulation.infection_rate = max(0.0, min(self.simulation.infection_rate / 100, 1.0))
        self.simulation.recovery_time = int(self.params["Recovery Time"].get())
        self.simulation.movement_speed = float(self.params["Movement Speed"].get())
        self.simulation.initialize_population()

    def _init_music(self):
        self.audio_ok = True
        try:
            pygame.mixer.init()
            # BG Music
            pygame.mixer.music.load("12a Athletic.mp3")
            # Success Sound
            self.sucess_sound = pygame.mixer.Sound("24 Course Clear.mp3")
        except pygame.error as e:
            print(f"[Audio Error] {e}")
            self.sucess_sound = None
            self.audio_ok = False


    def draw_agents(self):
        self.canvas.delete("agent")
        for agent in self.simulation.population:
            color = {"S": "blue", "I": "red", "R": "green"}[agent.state]
            radius = 3
            self.canvas.create_oval(
                agent.x - radius, agent.y - radius,
                agent.x + radius, agent.y + radius,
                fill = color, outline = "", tags = "agent"
            )

    def _update_status(self, s, i, r):
        self.status_label.config(text = f"Time: {self.time_step} | S: {s} | I: {i} | R: {r}")

    def _sim_complete(self, s, r):
        # Create pop-up window
        popup = Toplevel(self.root)
        popup.title("Simulation Complete")
        popup.geometry("320x250")
        popup.resizable(False, False)
        popup.grab_set()

        # Center the pop-up
        self.root.update_idletasks()  # Ensure window sizes are calculated
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_w = self.root.winfo_width()
        main_h = self.root.winfo_height()

        popup_w = 320
        popup_h = 250
        pos_x = main_x + (main_w // 2) - (popup_w // 2)
        pos_y = main_y + (main_h // 2) - (popup_h // 2)
        popup.geometry(f"{popup_w}x{popup_h}+{pos_x}+{pos_y}")

        # Summary message
        summary = (
                f"The epidemic has ended.\n\n"
                f"Total time steps: {self.time_step}\n"
                f"Susceptible: {s}\n"
                f"Infected: 0\n"
                f"Recovered: {r}\n\n"
                f"Congratulations\n"
                f"The population survived!"
            )
        
        # Buttons
        label = tk.Label(popup, text = summary, justify = "left", padx = 15, pady = 10)
        label.pack()
        export_btn = tk.Button(popup, text = "Export Graph", command = self.export_graph)
        export_btn.pack(pady = (5, 0))
        close_btn = tk.Button(popup, text = "Close", command = popup.destroy)
        close_btn.pack(pady = (5, 10))

    def update(self):
        self.simulation.update()
        self.draw_agents()
        s, i, r = self.simulation.count_states()
        self.graph.add_points(self.time_step, s, i, r)
        self._update_status(s, i, r)
        self.time_step += 1

        # Check for Epidemic Burnout
        if i == 0:
            # Stop sim
            self.running = False
            # Audio check
            if self.audio_ok:
                pygame.mixer.music.stop()
                self.sucess_sound.play()
            # Update status labels and activate pop up
            self.status_label.config(text = f"Simulation ended, final values: Time: {self.time_step} | S: {s} | I: 0 | R: {r}")
            # Finish updating status count and drawing final agents
            self.root.update_idletasks()    
            self._sim_complete(s, r)
            return

        self.loop_id = self.root.after(33, self.update)

    def start(self):
        if not self.running:
            if self.time_step == 0:
                self._init_simulation()
                self.draw_agents()
                if self.audio_ok:
                    pygame.mixer.music.play(-1)
            else:
                if self.audio_ok:
                    pygame.mixer.music.unpause()
            self.running = True
            self.update()

    def pause(self):
        if self.running and self.loop_id:
            self.root.after_cancel(self.loop_id)
            if self.audio_ok:
                pygame.mixer.music.pause()
            self.loop_id = None 
            self.running = False

    def reset(self):
        if self.running and self.loop_id:
            self.root.after_cancel(self.loop_id)
        self.running = False
        if self.audio_ok:
            pygame.mixer.music.stop()
        self.time_step = 0
        self.canvas.delete("all")
        self.graph.clear()
        self.status_label.config(text = "Time: 0 | S: 0 | I: 0 | R: 0")

    def export_graph(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".png",
            filetypes = [("PNG files", "*.png"), ("All files", "*.*")],
            title = "Save Graph As"
        )

        if file_path:
            self.graph.export(file_path)
            messagebox.showinfo("Export Complete", f"Graph saved as:\n{file_path}")

    def run(self):
        self.root.mainloop()
