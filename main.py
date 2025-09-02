import tkinter as tk
from tkinter import ttk
from itertools import permutations
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# ---------- Probability code ----------

def final_distribution(n):
    results = defaultdict(float)
    def recurse(i, remaining, assigned, prob):
        if i < n-1:
            possible = [r for r in remaining if r != i]
            if not possible:
                return
            p = 1.0 / len(possible)
            for pick in possible:
                new_remaining = list(remaining)
                new_remaining.remove(pick)
                new_assigned = assigned.copy()
                new_assigned[i] = pick
                recurse(i+1, tuple(new_remaining), new_assigned, prob * p)
        else:
            last_slip = remaining[0]
            if last_slip != i:
                final = assigned.copy()
                final[i] = last_slip
                perm = tuple(final[j] for j in range(n))
                results[perm] += prob
            else:
                for j in range(n-1):
                    final = assigned.copy()
                    swapped_with = final[j]
                    final[j] = i
                    final[i] = swapped_with
                    perm = tuple(final[k] for k in range(n))
                    results[perm] += prob * (1.0 / (n-1))
    recurse(0, tuple(range(n)), {}, 1.0)
    return results

def exact_ordered_distribution(n):
    results = defaultdict(float)

    def recurse(i, remaining, assigned, prob):
        if i == n:
            # All assigned
            perm = tuple(assigned)
            results[perm] += prob
            return

        # Person i picks
        possible = [r for r in remaining if r != i]
        for pick in possible:
            new_remaining = remaining.copy()
            new_remaining.remove(pick)
            new_assigned = assigned + [pick]
            recurse(i+1, new_remaining, new_assigned, prob / len(possible))

    recurse(0, list(range(n)), [], 1.0)
    return results

import random

def probability_matrix(n, monte_carlo_trials=100000):
    if n < 10:
        # Exact recursive calculation
        dist = exact_ordered_distribution(n)
        matrix = [[0.0]*n for _ in range(n)]
        total_prob = sum(dist.values())
        for perm, p in dist.items():
            for i in range(n):
                matrix[i][perm[i]] += p / total_prob
        return matrix
    else:
        # Monte Carlo simulation for larger groups
        counts = [[0]*n for _ in range(n)]
        for _ in range(monte_carlo_trials):
            remaining = list(range(n))
            assigned = [-1]*n
            for i in range(n):
                options = [x for x in remaining if x != i]
                if not options:
                    # swap with someone already assigned
                    swap_with = random.choice(range(i))
                    assigned[i] = assigned[swap_with]
                    assigned[swap_with] = i
                    break
                pick = random.choice(options)
                assigned[i] = pick
                remaining.remove(pick)
            for i, p in enumerate(assigned):
                counts[i][p] += 1
        # Normalize to probabilities
        matrix = [[c/monte_carlo_trials for c in row] for row in counts]
        return matrix

# ---------- GUI code ----------

class SecretSantaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Santa Probability Matrix")

        # Controls
        tk.Label(root, text="Group size (n):").grid(row=0, column=0, sticky="w")
        self.n_var = tk.IntVar(value=4)
        tk.Entry(root, textvariable=self.n_var, width=5).grid(row=0, column=1, sticky="w")
        tk.Button(root, text="Compute Matrix", command=self.update_matrix).grid(row=0, column=2, padx=5)

        tk.Label(root, text="Isolate Person:").grid(row=1, column=0, sticky="w")
        self.person_var = tk.StringVar(value="")
        self.person_combo = ttk.Combobox(root, textvariable=self.person_var, state="readonly")
        self.person_combo.grid(row=1, column=1, sticky="w")
        tk.Button(root, text="Show Person Probabilities", command=self.show_person).grid(row=1, column=2, padx=5)

        # Text matrix display
        self.text = tk.Text(root, width=60, height=20)
        self.text.grid(row=2, column=0, columnspan=3, pady=10)

        # Matplotlib canvas for heatmap
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=2, column=3, padx=10)

        self.matrix = []
        self.names = []

    def update_matrix(self):
        n = self.n_var.get()
        if n < 2:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, "Group size must be at least 2.")
            return

        self.matrix = probability_matrix(n)
        self.names = [chr(ord('A')+i) for i in range(n)]
        self.person_combo['values'] = self.names
        self.person_var.set("")

        # Update text matrix
        self.text.delete("1.0", tk.END)
        header = "     " + " ".join(f"{name:>6}" for name in self.names)
        self.text.insert(tk.END, header + "\n")
        for i in range(n):
            row = f"{self.names[i]} |" + " ".join(f"{self.matrix[i][j]:6.3f}" for j in range(n))
            self.text.insert(tk.END, row + "\n")

        # Update heatmap
        self.show_heatmap(self.matrix)

    def show_person(self):
        person = self.person_var.get()
        if not person:
            return
        idx = self.names.index(person)

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"Probabilities for {person}:\n")
        isolated = [[0 for _ in range(len(self.names))] for _ in range(len(self.names))]
        for j, name in enumerate(self.names):
            self.text.insert(tk.END, f"{name}: {self.matrix[idx][j]:.3f}\n")
            isolated[idx][j] = self.matrix[idx][j]

        self.show_heatmap(isolated)

    def show_heatmap(self, matrix_data):
        # If a previous canvas exists, destroy it
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        # Create new figure and axes
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        cax = self.ax.matshow(matrix_data, cmap='viridis')
        self.ax.set_xticks(range(len(self.names)))
        self.ax.set_yticks(range(len(self.names)))
        self.ax.set_xticklabels(self.names)
        self.ax.set_yticklabels(self.names)

        # Add colorbar
        self.cbar = self.fig.colorbar(cax, ax=self.ax)

        # Create new Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=2, column=3, padx=10)
        self.canvas.draw()

# ---------- Run GUI ----------

root = tk.Tk()
app = SecretSantaGUI(root)
root.mainloop()
