import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Configurações do banco de dados
DB_HOST = "www.thyagoquintas.com.br"
DB_PORT = 3306
DB_USER = "engenharia_25"
DB_PASSWORD = "caranguejoraposa"
DB_NAME = "engenharia_25"

class RHApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de RH - Colaboradores")
        self.geometry("1000x700") # Increased width and height for better spacing
        self.minsize(950, 600) # Minimum size to prevent layout issues

        # Configure grid for main window to be resizable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Styling ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam") # 'clam' is a good modern starting point

        # Customizing general styles
        self.style.configure("TFrame", background="#f0f0f0") # Light gray background for frames
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f0f0f0")
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 10))
        self.style.configure("TButton",
                             font=("Segoe UI", 10, "bold"),
                             padding=8,
                             background="#4CAF50", # A nice shade of green
                             foreground="white",
                             relief="flat", # Flat look for buttons
                             borderwidth=0)
        self.style.map("TButton",
                       background=[('active', '#45a049')], # Darker green on hover
                       foreground=[('pressed', 'white'), ('active', 'white')])

        # Treeview Styles
        self.style.configure("Treeview",
                             font=("Segoe UI", 10),
                             rowheight=28, # Slightly increased row height
                             background="white",
                             foreground="black",
                             fieldbackground="white",
                             borderwidth=1,
                             relief="solid") # Added a subtle border
        self.style.map("Treeview", background=[('selected', '#a8d1ff')]) # Light blue on selection

        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 11, "bold"),
                             background="#007acc", # Original blue heading
                             foreground="white",
                             relief="flat")
        self.style.map("Treeview.Heading",
                       background=[('active', '#005f99')])

        # --- Main Layout Frames ---
        # Top Frame for title or logo
        top_frame = ttk.Frame(self, padding="15 10")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(top_frame, text="Gestão de Colaboradores",
                  font=("Segoe UI", 18, "bold"), background="#f0f0f0").pack(pady=5)
        
        # Frame for the Treeview (list of data)
        tree_frame = ttk.Frame(self, padding="10 0 10 10")
        tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(1, weight=3) # Treeview takes more vertical space

        # Frame for Input Fields and Action Buttons
        input_button_frame = ttk.Frame(self, padding="10 10 10 15")
        input_button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.grid_rowconfigure(2, weight=1)

        # --- Treeview Setup ---
        self.tree = ttk.Treeview(tree_frame, columns=("matricula", "nome", "funcao", "escala", "horariocontratual", "encoding"), show="headings")
        
        # Define column headings and widths
        self.tree.heading("matricula", text="Matrícula", anchor="w")
        self.tree.column("matricula", width=80, minwidth=60, stretch=False)
        self.tree.heading("nome", text="Nome Completo", anchor="w")
        self.tree.column("nome", width=200, minwidth=150)
        self.tree.heading("funcao", text="Função", anchor="w")
        self.tree.column("funcao", width=150, minwidth=100)
        self.tree.heading("escala", text="Escala", anchor="w")
        self.tree.column("escala", width=120, minwidth=80)
        self.tree.heading("horariocontratual", text="Horário Contratual", anchor="w")
        self.tree.column("horariocontratual", width=130, minwidth=100)
        self.tree.heading("encoding", text="Encoding", anchor="w")
        self.tree.column("encoding", width=100, minwidth=80)
        
        self.tree.pack(fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.tag_configure('oddrow', background='#e8f2ff') # Lighter blue for odd rows
        self.tree.tag_configure('evenrow', background='white')

        # --- Input Fields Layout ---
        # Using a sub-frame for input fields to better manage their grid layout
        fields_frame = ttk.Frame(input_button_frame, padding="10")
        fields_frame.pack(side="left", fill="both", expand=True)

        # Labels and Entries
        labels = ["Matrícula:", "Nome:", "Função:", "Escala:", "Horário Contratual:", "Encoding:"]
        entries = []
        self.entry_matricula = ttk.Entry(fields_frame)
        self.entry_nome = ttk.Entry(fields_frame)
        self.entry_funcao = ttk.Entry(fields_frame)
        self.entry_escala = ttk.Entry(fields_frame)
        self.entry_horariocontratual = ttk.Entry(fields_frame)
        self.entry_encoding = ttk.Entry(fields_frame)
        
        self.entry_widgets = [self.entry_matricula, self.entry_nome, self.entry_funcao,
                              self.entry_escala, self.entry_horariocontratual, self.entry_encoding]

        for i, label_text in enumerate(labels):
            ttk.Label(fields_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            self.entry_widgets[i].grid(row=i, column=1, sticky="ew", padx=5, pady=3)
            fields_frame.grid_columnconfigure(1, weight=1) # Make entry column expandable

        # --- Buttons Layout ---
        # Using a sub-frame for buttons
        button_actions_frame = ttk.Frame(input_button_frame, padding="10")
        button_actions_frame.pack(side="right", fill="y")

        # Define buttons and their commands with a consistent style
        buttons_data = [
            ("Adicionar", self.adicionar_colaborador, "#4CAF50"), # Green for Add
            ("Editar", self.editar_colaborador, "#2196F3"),      # Blue for Edit
            ("Excluir", self.excluir_colaborador, "#f44336"),    # Red for Delete
            ("Atualizar Lista", self.carregar_colaboradores, "#FFC107"), # Amber for Refresh
            ("Ver Backup de Ponto", self.carregar_backup_ponto, "#9C27B0"), # Purple for Backup
            ("Voltar para Colaboradores", self.carregar_colaboradores_default, "#00BCD4") # Cyan for Back
        ]

        # Create buttons with distinct styles
        for text, command, color in buttons_data:
            btn_style_name = f"Custom.{color}.TButton"
            self.style.configure(btn_style_name,
                                 background=color,
                                 foreground="white",
                                 font=("Segoe UI", 10, "bold"),
                                 padding=8,
                                 relief="flat",
                                 borderwidth=0)
            self.style.map(btn_style_name,
                           background=[('active', self.darken_color(color, 20))], # Darken on hover
                           foreground=[('pressed', 'white'), ('active', 'white')])
            
            btn = ttk.Button(button_actions_frame, text=text, command=command, style=btn_style_name)
            btn.pack(fill="x", pady=5)


        # Initial setup
        self.conectar_banco()
        self.carregar_colaboradores()

        # Bind Treeview selection event
        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)

    def darken_color(self, hex_color, factor):
        """Darkens a hex color by a given factor (0-100)."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - int(c * factor / 100)) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

    def conectar_banco(self):
        try:
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset='utf8mb4'
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{e}")
            self.destroy()

    def carregar_backup_ponto(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT matricula, nome_colaborador, data_registro, horario_entrada, horario_saida, nome_departamento
                FROM BackupPontoCompleto
                ORDER BY data_registro DESC, horario_entrada DESC
            """)
            rows = cursor.fetchall()

            # Update Treeview columns for BackupPontoCompleto
            colunas = ["Matrícula", "Nome do Colaborador", "Data Registro", "Entrada", "Saída", "Departamento"]
            self.tree["columns"] = colunas
            for col_name, display_text in zip(colunas, ["Matrícula", "Nome do Colaborador", "Data Registro", "Entrada", "Saída", "Departamento"]):
                self.tree.heading(col_name, text=display_text, anchor="w")
                self.tree.column(col_name, width=100 if col_name in ["Matrícula", "Entrada", "Saída"] else 150)

            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(rows):
                tag = 'oddrow' if i % 2 else 'evenrow'
                self.tree.insert("", "end", values=row, tags=(tag,))

            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar backup de ponto:\n{e}")
        self.limpar_campos() # Clear fields when switching view

    def carregar_colaboradores_default(self):
        # Reset Treeview columns to original Colaborador columns
        colunas_colaborador = ("matricula", "nome", "funcao", "escala", "horariocontratual", "encoding")
        self.tree["columns"] = colunas_colaborador
        self.tree.heading("matricula", text="Matrícula")
        self.tree.column("matricula", width=80)
        self.tree.heading("nome", text="Nome")
        self.tree.column("nome", width=200)
        self.tree.heading("funcao", text="Função")
        self.tree.column("funcao", width=150)
        self.tree.heading("escala", text="Escala")
        self.tree.column("escala", width=120)
        self.tree.heading("horariocontratual", text="Horário Contratual")
        self.tree.column("horariocontratual", width=130)
        self.tree.heading("encoding", text="Encoding")
        self.tree.column("encoding", width=100)
        self.carregar_colaboradores()
        self.limpar_campos() # Clear fields when switching view

    def carregar_colaboradores(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT matricula, nome, funcao, escala, horariocontratual, encoding FROM Colaborador ORDER BY nome")
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(rows):
                tag = 'oddrow' if i % 2 else 'evenrow'
                self.tree.insert("", "end", values=row, tags=(tag,))
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar colaboradores:\n{e}")

    def adicionar_colaborador(self):
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        funcao = self.entry_funcao.get().strip()
        escala = self.entry_escala.get().strip()
        horariocontratual = self.entry_horariocontratual.get().strip()
        encoding = self.entry_encoding.get().strip()

        if not matricula or not nome:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha a **Matrícula** e o **Nome** do colaborador.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT matricula FROM Colaborador WHERE matricula = %s", (matricula,))
            if cursor.fetchone():
                messagebox.showwarning("Aviso", "Já existe um colaborador com esta **Matrícula**.")
            else:
                cursor.execute(
                    "INSERT INTO Colaborador (matricula, nome, funcao, escala, horariocontratual, encoding) VALUES (%s, %s, %s, %s, %s, %s)",
                    (matricula, nome, funcao, escala, horariocontratual, encoding)
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Colaborador adicionado com sucesso!")
                self.carregar_colaboradores()
                self.limpar_campos()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o colaborador:\n{e}")

    def excluir_colaborador(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Necessária", "Selecione um colaborador na lista para excluí-lo.")
            return

        matricula_to_delete = self.tree.item(selected_item[0])["values"][0]

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o colaborador com Matrícula **{matricula_to_delete}**?")
        if not confirm:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Colaborador WHERE matricula = %s", (matricula_to_delete,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Colaborador excluído com sucesso!")
            self.carregar_colaboradores()
            self.limpar_campos()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o colaborador:\n{e}")

    def editar_colaborador(self):
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        funcao = self.entry_funcao.get().strip()
        escala = self.entry_escala.get().strip()
        horariocontratual = self.entry_horariocontratual.get().strip()
        encoding = self.entry_encoding.get().strip()

        if not matricula:
            messagebox.showwarning("Matrícula Obrigatória", "A **Matrícula** é necessária para editar um colaborador.")
            return

        try:
            cursor = self.conn.cursor()
            update_fields = []
            params = []

            # Only add fields to update if they are not empty
            if nome:
                update_fields.append("nome = %s")
                params.append(nome)
            if funcao:
                update_fields.append("funcao = %s")
                params.append(funcao)
            if escala:
                update_fields.append("escala = %s")
                params.append(escala)
            if horariocontratual:
                update_fields.append("horariocontratual = %s")
                params.append(horariocontratual)
            if encoding:
                update_fields.append("encoding = %s")
                params.append(encoding)

            if not update_fields:
                messagebox.showwarning("Nenhuma Alteração", "Nenhum campo para atualizar foi preenchido.")
                cursor.close()
                return

            params.append(matricula)
            sql = f"UPDATE Colaborador SET {', '.join(update_fields)} WHERE matricula = %s"
            
            cursor.execute(sql, tuple(params))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Colaborador atualizado com sucesso!")
            self.carregar_colaboradores()
            self.limpar_campos()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar o colaborador:\n{e}")

    def preencher_campos(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Get selected values, handle potential IndexError if columns change
        try:
            values = self.tree.item(selected_item[0])["values"]
            if len(values) >= 6: # Check if it's the Colaborador view
                self.entry_matricula.delete(0, tk.END)
                self.entry_matricula.insert(0, values[0])
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, values[1])
                self.entry_funcao.delete(0, tk.END)
                self.entry_funcao.insert(0, values[2] if values[2] else "")
                self.entry_escala.delete(0, tk.END)
                self.entry_escala.insert(0, values[3] if values[3] else "")
                self.entry_horariocontratual.delete(0, tk.END)
                self.entry_horariocontratual.insert(0, values[4] if values[4] else "")
                self.entry_encoding.delete(0, tk.END)
                self.entry_encoding.insert(0, values[5] if values[5] else "")
            else: # Likely BackupPontoCompleto view, clear fields
                self.limpar_campos()
        except IndexError:
            self.limpar_campos() # Clear fields if selection is from a different table

    def limpar_campos(self):
        for entry in self.entry_widgets:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = RHApp()
    app.mainloop()