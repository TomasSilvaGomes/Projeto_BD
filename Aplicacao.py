import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import pyodbc
import tkinter.font as tkFont


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação")

        self.conn = None
        self.cursor = None

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # Menu de Conexão
        db_menu = tk.Menu(menu_bar, tearoff=0)
        db_menu.add_command(label="Ligar à Base de Dados", command=self.connect_to_db)
        db_menu.add_separator()
        db_menu.add_command(label="Sair", command=self.root.quit)
        menu_bar.add_cascade(label="Início", menu=db_menu)

        # Menu CRUD
        crud_menu = tk.Menu(menu_bar, tearoff=0)
        crud_menu.add_command(label="Adicionar Dados", command=self.add_data)
        crud_menu.add_command(label="Atualizar Dados", command=self.update_data)
        crud_menu.add_command(label="Apagar Dados", command=self.delete_data)
        crud_menu.add_command(label="Visualizar Dados", command=self.view_data)
        crud_menu.add_command(label="Query Genérica", command=self.generic_query)
        menu_bar.add_cascade(label="Operações CRUD", menu=crud_menu)

        # Menu About
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="Sobre",
                               command=lambda: messagebox.showinfo("Sobre", "Aplicação CRUD com Tkinter e PyODBC"))
        menu_bar.add_cascade(label="Ajuda", menu=about_menu)

        self.root.config(menu=menu_bar)

    def connect_to_db(self):
        try:
            ip = simpledialog.askstring("Ligação", "Insira o IP do servidor:")
            user = simpledialog.askstring("Ligação", "Insira o utilizador:")
            password = simpledialog.askstring("Ligação", "Insira a password:", show="*")
            database = simpledialog.askstring("Ligação", "Insira o nome da base de dados:")

            self.conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={ip};DATABASE={database};UID={user};PWD={password}")
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Sucesso", "Ligação efetuada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro na ligação", f"Erro no acesso à base de dados: {e}")

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

    def update_data(self):
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
                            set_entries = {}
                            for col in columns:
                                tk.Label(input_frame, text=f"Atualizar {col} (deixe vazio para ignorar):").pack()
                                entry = tk.Entry(input_frame)
                                entry.pack(pady=2)
                                set_entries[col] = entry

                            # Campo para condição WHERE
                            tk.Label(input_frame, text="Condição (WHERE):").pack()
                            where_entry = tk.Entry(input_frame)
                            where_entry.pack(pady=5)

                            # Botão para atualizar dados
                            def execute_update():
                                set_clause = ", ".join(
                                    f"{col}='{set_entries[col].get()}'" for col in columns if set_entries[col].get())
                                where_clause = where_entry.get()

                                if not set_clause:
                                    messagebox.showwarning("Aviso", "Insira pelo menos um valor para atualizar.")
                                    return

                                query = f"UPDATE {selected_table} SET {set_clause}"
                                if where_clause:
                                    query += f" WHERE {where_clause}"
                                try:
                                    self.cursor.execute(query)
                                    self.conn.commit()
                                    messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                                    update_window.destroy()
                                except Exception as e:
                                    messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")

                            # Botão para salvar
                            update_button = ttk.Button(input_frame, text="Salvar Alterações", command=execute_update)
                            update_button.pack(pady=10)

                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao obter colunas: {e}")
                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Criar janela para atualizar dados
                update_window = tk.Toplevel(self.root)
                update_window.title("Atualizar Dados")

                # Dropdown para selecionar tabela
                table_dropdown = ttk.Combobox(update_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Botão para carregar colunas
                load_button = ttk.Button(update_window, text="Carregar Colunas", command=fetch_columns)
                load_button.pack(pady=5)

                # Frame para entradas dinâmicas
                input_frame = tk.Frame(update_window)
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
                        # Limpar entradas anteriores
                        for widget in input_frame.winfo_children():
                            widget.destroy()

                        # Campo para condição WHERE
                        tk.Label(input_frame, text="Condição (WHERE):").pack()
                        where_entry = tk.Entry(input_frame)
                        where_entry.pack(pady=5)

                        # Botão para excluir dados
                        def execute_delete():
                            where_clause = where_entry.get()
                            query = f"DELETE FROM {selected_table}"
                            if where_clause:
                                query += f" WHERE {where_clause}"
                            try:
                                self.cursor.execute(query)
                                self.conn.commit()
                                messagebox.showinfo("Sucesso", "Dados apagados com sucesso!")
                                delete_window.destroy()
                            except Exception as e:
                                messagebox.showerror("Erro", f"Erro ao apagar dados: {e}")

                        # Botão para confirmar exclusão
                        delete_button = ttk.Button(input_frame, text="Apagar Dados", command=execute_delete)
                        delete_button.pack(pady=10)

                    else:
                        messagebox.showwarning("Aviso", "Selecione uma tabela.")

                # Criar janela para apagar dados
                delete_window = tk.Toplevel(self.root)
                delete_window.title("Apagar Dados")

                # Dropdown para selecionar tabela
                table_dropdown = ttk.Combobox(delete_window, values=tables, state="readonly")
                table_dropdown.pack(pady=5)

                # Botão para carregar opção de exclusão
                load_button = ttk.Button(delete_window, text="Configurar Exclusão", command=fetch_columns)
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

    def generic_query(self):
        if self.cursor:
            query = simpledialog.askstring("Query Genérica", "Escreva a query SQL:")
            try:
                self.cursor.execute(query)
                columns = [desc[0] for desc in self.cursor.description]
                rows = self.cursor.fetchall()

                result_window = tk.Toplevel(self.root)
                result_window.title("Resultados da Query Genérica")

                output = scrolledtext.ScrolledText(result_window, width=80, height=20)
                output.pack(pady=5)
                output.insert(tk.END, f"Colunas: {', '.join(columns)}\n\n")
                for row in rows:
                    output.insert(tk.END, f"{row}\n")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro na execução da query: {e}")
        else:
            messagebox.showwarning("Aviso", "Ligue-se à base de dados primeiro.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
