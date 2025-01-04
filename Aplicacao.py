import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, PhotoImage
import pyodbc


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Covilhã Mobilidade")

        self.conn = None
        self.cursor = None

        self.setup_home_page()

    def setup_home_page(self):
        # Frame inicial
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill="both", expand=True)
        self.root.geometry("1920x1080")

        # Adicionar imagem
        try:
            # Substitua 'image.png' pelo caminho da sua imagem
<<<<<<< Updated upstream
            self.image = PhotoImage(file="pp.png")
=======
            self.image = PhotoImage(file="BD.png")
>>>>>>> Stashed changes
            image_label = tk.Label(self.home_frame, image=self.image)
            #put the image in 1920x1080
            image_label.place(relwidth=1, relheight=1)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao carregar a imagem: {e}")

        root.attributes("-fullscreen", True)

        def exit_fullscreen(event):
            root.attributes("-fullscreen", False)
            

        # Vincular a tecla Esc para sair do fullscreen
        root.bind("<Escape>", exit_fullscreen)

        # Botão para ir à página de conexão
        style = ttk.Style()
        style.configure("MainButton.TButton",
                        font=("Times New Roman", 16, "bold"),
                        padding=15,
                        width=30,
                        anchor="center",
                        background="#33CCFF",
                        foreground="black",
                        borderwidth=3)
        connect_button = ttk.Button(self.home_frame, text="Ligar à Base de Dados", command=self.show_connect_page,
                                     style="MainButton.TButton")
        connect_button.place(relx=0.89, rely=0.83, anchor="center")

    def show_connect_page(self):
        # Criar uma nova janela
        self.connect_window = tk.Toplevel(self.root)
        self.connect_window.title("Conexão à Base de Dados")
        self.connect_window.geometry("300x225")

        # Adicionar campos e botões na nova janela
        tk.Label(self.connect_window, text="IP do Servidor:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.ip_entry = tk.Entry(self.connect_window)
        self.ip_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self.connect_window, text="Nome do Utilizador:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.user_entry = tk.Entry(self.connect_window)
        self.user_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.connect_window, text="Password:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.pass_entry = tk.Entry(self.connect_window, show="*")
        self.pass_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self.connect_window, text="Nome da Base de Dados:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.db_entry = tk.Entry(self.connect_window)
        self.db_entry.grid(row=3, column=1, pady=5, padx=5)

        # Botões na nova janela
        connect_button = ttk.Button(self.connect_window, text="Conectar", command=self.connect_to_db)
        connect_button.grid(row=4, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self.connect_window, text="Voltar", command=self.connect_window.destroy)
        back_button.grid(row=5, column=0, columnspan=2, pady=10)

    def show_menu_page(self):
        # Ocultar a interface inicial
        self.home_frame.pack_forget()


        # Frame do menu principal
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)

        # Adicionar título
        ttk.Label(self.menu_frame, text="Menu Principal", style='primary.Inverse.TLabel', font=("Times New Roman", 20)).pack(pady=20)

        # Botões do menu
        buttons_frame = tk.Frame(self.menu_frame)
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

        style = ttk.Style()
        style.configure("MenuButton.TButton",
                        font=("Times New Roman", 12, "bold"),
                        padding=20,
                        width=15,
                        anchor="center",
                        background="#1E1E1E",
                        foreground="Black",
                        borderwidth=3)

        style.map("MenuButton.TButton",
                  background=[("active", "#1e1e1e")])


        add_button = ttk.Button(buttons_frame, text="Inserir Dados", command=self.add_data, style="MenuButton.TButton")
        add_button.pack(side="left", pady=20)  # Usar "top" e espaçamento para organizar

        delete_button = ttk.Button(buttons_frame, text="Remover Dados", command=self.delete_data,
                                   style="MenuButton.TButton")
        delete_button.pack(side="left", pady=20)

        view_button = ttk.Button(buttons_frame, text="Visualizar Dados", command=self.view_data,
                                 style="MenuButton.TButton")
        view_button.pack(side="left", pady=20)

        update_button = ttk.Button(buttons_frame, text="Atualizar Dados", command=self.update_data,
                                   style="MenuButton.TButton")
        update_button.pack(side="left", pady=20)

        disconnect_button = ttk.Button(buttons_frame, text="Desconectar", command=self.disconnect_db,
                                       style="MenuButton.TButton")
        disconnect_button.pack(expand=True, side="left", pady=20)

    def connect_to_db(self):
        try:
            ip = self.ip_entry.get()
            user = self.user_entry.get()
            password = self.pass_entry.get()
            database = self.db_entry.get()

            self.conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={ip};DATABASE={database};UID={user};PWD={password}")
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Sucesso", "Ligação efetuada com sucesso!")
            self.connect_window.destroy()
            self.show_menu_page()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar: {e}")

    def disconnect_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            messagebox.showinfo("Desconectado", "Conexão encerrada.")
        self.menu_frame.pack_forget()
        self.setup_home_page()

    def add_data(self):

        if self.cursor:
            try:
                # Obter tabelas do banco de dados
                self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                tables = [row.TABLE_NAME for row in self.cursor.fetchall()]

                def fetch_columns():
                    # Obter a tabela selecionada
                    selected_table = table_dropdown.get()
                    if selected_table:
                        try:
                            # Obter colunas da tabela selecionada
                            self.cursor.execute(
                                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}'")
                            columns = [row.COLUMN_NAME for row in self.cursor.fetchall()]

                            # Limpar entradas anteriores
                            for widget in input_frame.winfo_children():
                                widget.destroy()

                            # Criar campos de entrada para cada coluna
                            entries = {}
                            for col in columns:
                                tk.Label(input_frame, text=col).pack()
                                entry = tk.Entry(input_frame)
                                entry.pack(pady=2)
                                entries[col] = entry

                            # Botão para inserir dados
                            def insert_data():
                                values = {col: entries[col].get() for col in columns}
                                try:
                                    # Gerar e executar query SQL
                                    cols = ", ".join(values.keys())
                                    vals = ", ".join(f"'{v}'" for v in values.values())
                                    self.cursor.execute(f"INSERT INTO {selected_table} ({cols}) VALUES ({vals})")
                                    self.conn.commit()
                                    messagebox.showinfo("Sucesso", "Dados adicionados com sucesso!")
                                    add_window.destroy()
                                except Exception as e:
                                    messagebox.showerror("Erro", f"Erro ao adicionar dados: {e}")

                            # Botão para salvar dados
                            save_button = ttk.Button(input_frame, text="Salvar", command=insert_data)
                            save_button.pack(pady=10)

                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao obter colunas: {e}")
                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Criar janela para adicionar dados
                add_window = tk.Toplevel(self.root)
                add_window.title("Adicionar Dados")
                add_window.geometry("300x225")

                # Dropdown para selecionar tabela
                table_dropdown = ttk.Combobox(add_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Botão para carregar colunas
                load_button = ttk.Button(add_window, text="Carregar Colunas", command=fetch_columns)
                load_button.pack(pady=5)

                # Frame para entradas dinâmicas
                input_frame = tk.Frame(add_window)
                input_frame.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao obter tabelas: {e}")
        else:
            messagebox.showwarning("Aviso", "Ligue-se à base de dados primeiro.")

    def delete_data(self):
        if self.cursor:
            try:
                # Obter tabelas do banco de dados
                self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                tables = [row.TABLE_NAME for row in self.cursor.fetchall()]

                def fetch_columns():
                    # Obter a tabela selecionada
                    selected_table = table_dropdown.get()
                    if selected_table:
                        # Obter colunas da tabela selecionada
                        self.cursor.execute(
                            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}'")
                        columns = [row.COLUMN_NAME for row in self.cursor.fetchall()]

                        if columns:
                            # Limpar entradas anteriores
                            for widget in input_frame.winfo_children():
                                widget.destroy()

                            tk.Label(input_frame, text="Preencha os valores dos atributos para exclusão:").pack(pady=5)

                            # Dicionário para armazenar os campos de entrada
                            entries = {}

                            for column in columns:
                                tk.Label(input_frame, text=f"{column}:").pack()
                                entry = tk.Entry(input_frame)
                                entry.pack(pady=2)
                                entries[column] = entry

                            # Botão para executar exclusão
                            def execute_delete():
                                # Construir cláusula WHERE
                                where_clauses = []
                                for column, entry in entries.items():
                                    value = entry.get()
                                    if value:
                                        where_clauses.append(f"{column} = '{value}'")

                                if where_clauses:
                                    where_clause = " AND ".join(where_clauses)
                                    query = f"DELETE FROM {selected_table} WHERE {where_clause}"
                                    try:
                                        self.cursor.execute(query)
                                        self.conn.commit()
                                        messagebox.showinfo("Sucesso", "Dados apagados com sucesso!")
                                        delete_window.destroy()
                                    except Exception as e:
                                        messagebox.showerror("Erro", f"Erro ao apagar dados: {e}")
                                else:
                                    messagebox.showwarning("Aviso", "Nenhum critério especificado para exclusão.")

                            # Botão para confirmar exclusão
                            delete_button = ttk.Button(input_frame, text="Apagar Dados", command=execute_delete)
                            delete_button.pack(pady=10)
                        else:
                            messagebox.showwarning("Aviso", "A tabela selecionada não possui colunas.")

                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Criar janela para apagar dados
                delete_window = tk.Toplevel(self.root)
                delete_window.title("Apagar Dados")
                delete_window.geometry("500x400")

                # Dropdown para selecionar tabela
                tk.Label(delete_window, text="Selecione uma tabela:").pack(pady=5)
                table_dropdown = ttk.Combobox(delete_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Botão para carregar colunas
                load_button = ttk.Button(delete_window, text="Carregar Atributos", command=fetch_columns)
                load_button.pack(pady=5)

                # Frame para entradas dinâmicas
                input_frame = tk.Frame(delete_window)
                input_frame.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao obter tabelas: {e}")
        else:
            messagebox.showwarning("Aviso", "Ligue-se à base de dados primeiro.")

    def view_data(self):
        if self.cursor:
            try:
                self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                tables = [row.TABLE_NAME for row in self.cursor.fetchall()]

                def fetch_table_data():
                    selected_table = table_dropdown.get()
                    if selected_table:
                        self.cursor.execute(f"SELECT * FROM {selected_table}")
                        columns = [desc[0] for desc in self.cursor.description]
                        rows = self.cursor.fetchall()

                        # Limpar a Treeview
                        tree.delete(*tree.get_children())

                        # Configurar colunas
                        tree["columns"] = columns
                        tree["show"] = "headings"
                        for col in columns:
                            tree.heading(col, text=col)
                            tree.column(col, width=100, anchor="w")  # Ajustar largura inicial

                        # Inserir dados formatados na tabela
                        for row in rows:
                            tree.insert("", "end", values=[str(value).strip("'") for value in row])

                        # Ajustar automaticamente a largura das colunas
                        font = tkFont.Font()
                        for col in columns:
                            max_width = max(
                                font.measure(value) for value in [col] + [str(row[columns.index(col)]) for row in rows])
                            tree.column(col, width=max_width)

                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Criar janela para exibir dados
                view_window = tk.Toplevel(self.root)
                view_window.title("Visualizar Tabela")

                # Dropdown para selecionar tabela
                table_dropdown = ttk.Combobox(view_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Botão para carregar dados
                view_button = ttk.Button(view_window, text="Visualizar", command=fetch_table_data)
                view_button.pack(pady=5)

                # Criar Treeview para exibir dados
                tree = ttk.Treeview(view_window, height=20)
                tree.pack(fill="both", expand=True)

                # Adicionar barras de rolagem
                scroll_y = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
                scroll_x = ttk.Scrollbar(view_window, orient="horizontal", command=tree.xview)
                tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
                scroll_y.pack(side="right", fill="y")
                scroll_x.pack(side="bottom", fill="x")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao obter tabelas: {e}")
        else:
            messagebox.showwarning("Aviso", "Ligue-se à base de dados primeiro.")

    def update_data(self):
        if self.cursor:
            try:
                # Fetch tables from the database
                self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                tables = [row.TABLE_NAME for row in self.cursor.fetchall()]

                def fetch_columns():
                    selected_table = table_dropdown.get()
                    if selected_table:
                        try:
                            # Fetch columns of the selected table, excluding those starting with 'id'
                            self.cursor.execute(
                                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}'")
                            columns = [row.COLUMN_NAME for row in self.cursor.fetchall() if
                                       not row.COLUMN_NAME.lower().startswith('id')]

                            # Clear previous widgets
                            for widget in input_frame.winfo_children():
                                widget.destroy()

                            # Create input fields for WHERE clause and updated values
                            entries_where = {}
                            entries_update = {}

                            tk.Label(input_frame,
                                     text="Especifique os critérios para selecionar registros (WHERE):").pack(pady=5)
                            for col in columns:
                                tk.Label(input_frame, text=f"{col} (WHERE):").pack()
                                entry = tk.Entry(input_frame)
                                entry.pack(pady=2)
                                entries_where[col] = entry

                            tk.Label(input_frame, text="Atualize os valores para as colunas desejadas:").pack(pady=10)
                            for col in columns:
                                tk.Label(input_frame, text=f"{col} (SET):").pack()
                                entry = tk.Entry(input_frame)
                                entry.pack(pady=2)
                                entries_update[col] = entry

                            def execute_update():
                                # Build WHERE clause
                                where_clauses = []
                                for column, entry in entries_where.items():
                                    value = entry.get()
                                    if value:
                                        where_clauses.append(f"{column} = '{value}'")

                                # Build SET clause
                                set_clauses = []
                                for column, entry in entries_update.items():
                                    value = entry.get()
                                    if value:
                                        set_clauses.append(f"{column} = '{value}'")

                                if where_clauses and set_clauses:
                                    where_clause = " AND ".join(where_clauses)
                                    set_clause = ", ".join(set_clauses)
                                    query = f"UPDATE {selected_table} SET {set_clause} WHERE {where_clause}"
                                    try:
                                        self.cursor.execute(query)
                                        self.conn.commit()
                                        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                                        update_window.destroy()
                                    except Exception as e:
                                        messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")
                                else:
                                    messagebox.showwarning("Aviso",
                                                           "Especifique critérios para WHERE e valores para SET.")

                            # Button to execute the update query
                            update_button = ttk.Button(input_frame, text="Atualizar Dados", command=execute_update)
                            update_button.pack(pady=10)

                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao obter colunas: {e}")
                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Create update data window
                update_window = tk.Toplevel(self.root)
                update_window.title("Atualizar Dados")
                update_window.geometry("500x500")

                # Dropdown to select table
                tk.Label(update_window, text="Selecione uma tabela:").pack(pady=5)
                table_dropdown = ttk.Combobox(update_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Button to load columns
                load_button = ttk.Button(update_window, text="Carregar Colunas", command=fetch_columns)
                load_button.pack(pady=5)

                # Frame for dynamic inputs
                input_frame = tk.Frame(update_window)
                input_frame.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao obter tabelas: {e}")
        else:
            messagebox.showwarning("Aviso", "Ligue-se à base de dados primeiro.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
