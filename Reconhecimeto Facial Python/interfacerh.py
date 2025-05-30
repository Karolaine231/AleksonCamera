import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Configurações do banco de dados
DB_HOST = ""
DB_PORT = 
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

class RHApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de RH - Colaboradores")
        self.geometry("1100x750")  # Increased width and height for better spacing
        self.minsize(1000, 700)    # Minimum size to prevent layout issues

        # Configure grid for main window to be resizable
        self.grid_rowconfigure(0, weight=0) # Top frame fixed height
        self.grid_rowconfigure(1, weight=3) # Treeview takes more vertical space
        self.grid_rowconfigure(2, weight=1) # Input/button frame
        self.grid_columnconfigure(0, weight=1)

        self._sort_column = "nome"  # Default sort column for colaboradores
        self._sort_direction = "ASC" # Default sort direction

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
        top_frame.grid(row=0, column=0, sticky="ew")
        ttk.Label(top_frame, text="Gestão de Colaboradores",
                  font=("Segoe UI", 18, "bold"), background="#f0f0f0").pack(pady=5)
        
        # Frame for the Treeview (list of data)
        tree_frame = ttk.Frame(self, padding="10 0 10 10")
        tree_frame.grid(row=1, column=0, sticky="nsew")

        # Frame for Input Fields and Action Buttons
        input_button_frame = ttk.Frame(self, padding="10 10 10 15")
        input_button_frame.grid(row=2, column=0, sticky="ew")
        input_button_frame.grid_columnconfigure(0, weight=1) # Fields frame
        input_button_frame.grid_columnconfigure(1, weight=0) # Buttons frame

        # --- Search Bar ---
        search_frame = ttk.Frame(input_button_frame, padding="5")
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1) # Make search entry expandable

        ttk.Label(search_frame, text="Buscar:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.search_entry.bind("<KeyRelease>", self.filtrar_dados) # Filters on key release
        
        ttk.Button(search_frame, text="Limpar Busca", command=lambda: [self.search_entry.delete(0, tk.END), self.carregar_colaboradores()], style="TButton").grid(row=0, column=2, padx=5)

        # --- Treeview Setup ---
        self.tree = ttk.Treeview(tree_frame, show="headings") # Columns are defined dynamically
        
        self.tree.pack(fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.tag_configure('oddrow', background='#e8f2ff') # Lighter blue for odd rows
        self.tree.tag_configure('evenrow', background='white')

        # Bind Treeview selection event and heading click for sorting
        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)
        self.tree.bind("<Button-1>", self.on_treeview_heading_click)

        # --- Input Fields Layout ---
        fields_frame = ttk.Frame(input_button_frame, padding="10")
        fields_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        fields_frame.grid_columnconfigure(1, weight=1) # Make entry column expandable

        # Labels and Entries
        labels = ["Matrícula:", "Nome:", "Função:", "Escala:", "Horário Contratual:"]
        self.entry_matricula = ttk.Entry(fields_frame)
        self.entry_nome = ttk.Entry(fields_frame)
        self.entry_funcao = ttk.Entry(fields_frame)
        self.entry_escala = ttk.Entry(fields_frame)
        self.entry_horariocontratual = ttk.Entry(fields_frame)
        
        self.entry_widgets = [self.entry_matricula, self.entry_nome, self.entry_funcao,
                              self.entry_escala, self.entry_horariocontratual]

        for i, label_text in enumerate(labels):
            ttk.Label(fields_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            self.entry_widgets[i].grid(row=i, column=1, sticky="ew", padx=5, pady=3)

        # --- Buttons Layout ---
        button_actions_frame = ttk.Frame(input_button_frame, padding="10")
        button_actions_frame.grid(row=1, column=1, sticky="nswe", padx=5, pady=5)

        # Define buttons and their commands with a consistent style
        buttons_data = [
            ("Adicionar", self.adicionar_colaborador, "#4CAF50"), # Green for Add
            ("Editar", self.editar_colaborador, "#2196F3"),      # Blue for Edit
            ("Excluir", self.excluir_colaborador, "#f44336"),     # Red for Delete
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
        self.carregar_colaboradores() # Load default view initially

    def darken_color(self, hex_color, factor):
        """Darkens a hex color by a given factor (0-100)."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - int(c * factor / 100)) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

    def conectar_banco(self):
        """Tries to connect to the MySQL database."""
        try:
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset='utf8mb4'
            )
            messagebox.showinfo("Conexão", "Conectado ao banco de dados com sucesso!")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{e}")
            self.destroy() # Close application if connection fails

    def on_treeview_heading_click(self, event):
        """Handles clicks on Treeview column headings for sorting."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column_id = self.tree.identify_column(event.x) # Returns #1, #2, etc.
            column_name = self.tree.heading(column_id, "text") # Get the displayed text of the heading

            # Map display names to actual database column names
            column_map_colaboradores = {
                "Matrícula": "matricula",
                "Nome Completo": "nome",
                "Função": "funcao",
                "Escala": "escala",
                "Horário Contratual": "horariocontratual"
            }
            column_map_backup_ponto = {
                "Matrícula": "matricula",
                "Nome do Colaborador": "nome_colaborador",
                "Data Registro": "data_registro",
                "Entrada": "horario_entrada",
                "Saída": "horario_saida",
                "Departamento": "nome_departamento"
            }
            
            # Determine which mapping to use based on current Treeview columns
            if "Data Registro" in self.tree["columns"]: # Check if it's the BackupPontoCompleto view
                db_column = column_map_backup_ponto.get(column_name)
            else: # Assume Colaboradores view
                db_column = column_map_colaboradores.get(column_name)

            if db_column:
                # Toggle direction if the same column is clicked again
                if hasattr(self, '_sort_column') and self._sort_column == db_column:
                    self._sort_direction = "DESC" if self._sort_direction == "ASC" else "ASC"
                else:
                    self._sort_column = db_column
                    self._sort_direction = "ASC"
                
                self.filtrar_dados() # Re-load data with new sort order

    def carregar_backup_ponto(self):
        """Loads and displays data from the BackupPontoCompleto view."""
        try:
            cursor = self.conn.cursor()

            # Update Treeview columns for BackupPontoCompleto
            colunas = ("Matrícula", "Nome do Colaborador", "Data Registro", "Entrada", "Saída", "Departamento")
            self.tree["columns"] = colunas
            for col_name in colunas:
                self.tree.heading(col_name, text=col_name, anchor="w")
                if col_name in ["Matrícula", "Entrada", "Saída"]:
                    self.tree.column(col_name, width=100, minwidth=60, stretch=False)
                else:
                    self.tree.column(col_name, width=150, minwidth=100)

            # Set default sorting for backup view
            self._sort_column = "data_registro"
            self._sort_direction = "DESC"

            self.filtrar_dados() # Use filter to load with new columns and sort
            self.limpar_campos() # Clear fields when switching view

        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar backup de ponto:\n{e}")

    def carregar_colaboradores_default(self):
        """Resets Treeview columns to original Colaborador columns and reloads."""
        # Reset Treeview columns to original Colaborador columns
        colunas_colaborador = ("matricula", "nome", "funcao", "escala", "horariocontratual")
        self.tree["columns"] = colunas_colaborador
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
        
        # Set default sorting for collaborators view
        self._sort_column = "nome"
        self._sort_direction = "ASC"
        
        self.filtrar_dados() # Use filter to load with new columns and sort
        self.limpar_campos() # Clear fields when switching view

    def carregar_colaboradores(self):
        """Loads and displays all collaborators (default view)."""
        # This function is now mostly a wrapper to call carregar_colaboradores_default
        # as it also sets up the columns and sorting defaults.
        self.carregar_colaboradores_default()

    def filtrar_dados(self, event=None):
        """Filters and sorts data in the Treeview based on search term and current sort order."""
        search_term = self.search_entry.get().strip()
        
        # Clear the Treeview first
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = self.conn.cursor()
            
            # Determine which table/view to query based on current Treeview columns
            is_backup_ponto_view = "Data Registro" in self.tree["columns"]

            if is_backup_ponto_view:
                query = f"""
                    SELECT matricula, nome_colaborador, data_registro, horario_entrada, horario_saida, nome_departamento
                    FROM BackupPontoCompleto
                    WHERE matricula LIKE %s OR nome_colaborador LIKE %s OR nome_departamento LIKE %s
                    ORDER BY {self._sort_column} {self._sort_direction}
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                
            else: # Colaboradores view
                query = f"""
                    SELECT matricula, nome, funcao, escala, horariocontratual 
                    FROM Colaborador 
                    WHERE matricula LIKE %s OR nome LIKE %s OR funcao LIKE %s OR escala LIKE %s
                    ORDER BY {self._sort_column} {self._sort_direction}
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            for i, row in enumerate(rows):
                tag = 'oddrow' if i % 2 else 'evenrow'
                self.tree.insert("", "end", values=row, tags=(tag,))
            
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Busca/Carregamento", f"Erro ao filtrar ou carregar dados:\n{e}")

    def adicionar_colaborador(self):
        """Adds a new collaborator to the database."""
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        funcao = self.entry_funcao.get().strip()
        escala = self.entry_escala.get().strip()
        horariocontratual = self.entry_horariocontratual.get().strip()

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
                    "INSERT INTO Colaborador (matricula, nome, funcao, escala, horariocontratual) VALUES (%s, %s, %s, %s, %s)",
                    (matricula, nome, funcao, escala, horariocontratual)
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Colaborador adicionado com sucesso!")
                self.carregar_colaboradores()
                self.limpar_campos()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o colaborador:\n{e}")

    def excluir_colaborador(self):
        """Deletes a selected collaborator from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Necessária", "Selecione um colaborador na lista para excluí-lo.")
            return

        # Ensure we are in the Colaborador view before attempting to delete
        if "Data Registro" in self.tree["columns"]:
            messagebox.showwarning("Operação Não Permitida", "Exclusão não disponível na visualização de Backup de Ponto. Volte para a lista de Colaboradores.")
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
        """Edits selected collaborator's details in the database."""
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        funcao = self.entry_funcao.get().strip()
        escala = self.entry_escala.get().strip()
        horariocontratual = self.entry_horariocontratual.get().strip()

        if not matricula:
            messagebox.showwarning("Matrícula Obrigatória", "A **Matrícula** é necessária para editar um colaborador. Por favor, selecione um colaborador na lista ou insira a matrícula.")
            return

        # Ensure we are in the Colaborador view before attempting to edit
        if "Data Registro" in self.tree["columns"]:
            messagebox.showwarning("Operação Não Permitida", "Edição não disponível na visualização de Backup de Ponto. Volte para a lista de Colaboradores.")
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

            if not update_fields:
                messagebox.showwarning("Nenhuma Alteração", "Nenhum campo para atualizar foi preenchido.")
                cursor.close()
                return

            params.append(matricula)
            sql = f"UPDATE Colaborador SET {', '.join(update_fields)} WHERE matricula = %s"
            
            cursor.execute(sql, tuple(params))
            self.conn.commit()
            
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", f"Nenhum colaborador encontrado com a matrícula {matricula} para editar.")
            else:
                messagebox.showinfo("Sucesso", "Colaborador atualizado com sucesso!")
            
            self.carregar_colaboradores()
            self.limpar_campos()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar o colaborador:\n{e}")

    def preencher_campos(self, event):
        """Fills input fields when a Treeview item is selected."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.limpar_campos() # Clear fields if nothing is selected or selection is cleared
            return
        
        # Get selected values, handle potential IndexError if columns change
        try:
            values = self.tree.item(selected_item[0])["values"]
            
            # Check if it's the Colaborador view (based on the number of expected fields)
            # This is a simple heuristic; a more robust way is to check self.tree["columns"]
            current_columns_tuple = self.tree["columns"]
            
            if "matricula" in current_columns_tuple and len(values) >= 5: # Colaborador view
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
            else: # Likely BackupPontoCompleto view or other, clear fields
                self.limpar_campos()
        except IndexError:
            self.limpar_campos() # Clear fields if selection causes an index error (e.g., mismatched columns)

    def limpar_campos(self):
        """Clears all input fields."""
        for entry in self.entry_widgets:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = RHApp()
    app.mainloop()
