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
            self.image = PhotoImage(file="BD.png")
            image_label = tk.Label(self.home_frame, image=self.image)
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

        perguntas_button = ttk.Button(buttons_frame, text="Informações", command=self.show_perguntas,
                                   style="MenuButton.TButton")
        perguntas_button.pack(side="left", pady=20)


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
                tables = [row.TABLE_NAME for row in self.cursor.fetchall() if row.TABLE_NAME.lower() != 'id']

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
                            columns = [row.COLUMN_NAME for row in self.cursor.fetchall() if row.COLUMN_NAME.lower() != 'id']

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

    def show_perguntas(self):
        # nova interface é fullscreen e não tem barra de título
        self.root.attributes("-fullscreen", True)

        def exit_fullscreen(event):
            self.root.attributes("-fullscreen", False)

        self.root.bind("<Escape>", exit_fullscreen)

        # Frame do menu perguntas
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)

        # Criar uma nova janela
        self.perguntas_window = tk.Toplevel(self.root)
        self.perguntas_window.title("Perguntas")

        # Adicionar título
        ttk.Label(
            self.perguntas_window,
            text="Resposta às perguntas do enunciado e mais algumas",
            style='primary.Inverse.TLabel',
            font=("Times New Roman", 20)
        ).pack(pady=20)

        # Frame para os botões, utilizando grid para organizar na horizontal
        buttons_frame = tk.Frame(self.perguntas_window)
        buttons_frame.pack(pady=20)

        # Criar botões na horizontal, utilizando o método grid para alinhá-los lado a lado
        rotas_button = ttk.Button(
            buttons_frame,
            text="Identificar Rotas de Autocarro\ncom Maior Número de Passageiros",
            command=self.identificar_rotas_maior_passageiros,
            style="MenuButton.TButton",
            width=30
        )
        rotas_button.grid(row=0, column=0, padx=10, pady=10)

        tipos_autocarro_button = ttk.Button(
            buttons_frame,
            text="Identificar tipos de autocarro\ne respetivo condutor",
            command=self.identificar_tipos_autocarro,
            style="MenuButton.TButton",
            width=30
        )
        tipos_autocarro_button.grid(row=0, column=1, padx=10, pady=10)

        paragens_button = ttk.Button(
            buttons_frame,
            text="Identificar Paragens com\nMaior Afluência de Passageiros",
            command=self.identificar_paragens_maior_afluencia,
            style="MenuButton.TButton",
            width=30
        )
        paragens_button.grid(row=0, column=2, padx=10, pady=10)

        qualidade_ar_button = ttk.Button(
            buttons_frame,
            text="Analisar Qualidade do\nAr nas Paragens",
            command=self.analisar_qualidade_ar,
            style="MenuButton.TButton",
            width=30
        )
        qualidade_ar_button.grid(row=0, column=3, padx=10, pady=10)

        velocidade_congestionamento_button = ttk.Button(
            buttons_frame,
            text="Identificar Velocidade Média\ne Congestionamento",
            command=self.calcular_velocidade_congestionamento,
            style="MenuButton.TButton",
            width=30
        )
        velocidade_congestionamento_button.grid(row=0, column=4, padx=10, pady=10)

        veiculos_segmentos_button = ttk.Button(
            buttons_frame,
            text="Identificar Veículos e Segmentos",
            command=self.listar_veiculos_por_segmento,
            style="MenuButton.TButton",
            width=30
        )
        veiculos_segmentos_button.grid(row=1, column=0, padx=10, pady=10)

        estacionamento_button = ttk.Button(
            buttons_frame,
            text="Identificar Estacionamentos",
            command=self.ocupacao_estacionameto,
            style="MenuButton.TButton",
            width=30
        )
        estacionamento_button.grid(row=1, column=1, padx=10, pady=10)

        velocidade_media_button = ttk.Button(
            buttons_frame,
            text="Identificar Velocidade Média",
            command=self.velocidade_media_veiculos,
            style="MenuButton.TButton",
            width=30
        )
        velocidade_media_button.grid(row=1, column=2, padx=10, pady=10)

        rotas_paragens_button = ttk.Button(
            buttons_frame,
            text="Identificar Rotas e Paragens",
            command=self.rotas_com_paragens,
            style="MenuButton.TButton",
            width=30
        )
        rotas_paragens_button.grid(row=1, column=3, padx=10, pady=10)

        paragens_poluentes_button = ttk.Button(
            buttons_frame,
            text="Identificar Paragens Poluentes",
            command=self.paragens_com_alto_co2,
            style="MenuButton.TButton",
            width=30
        )
        paragens_poluentes_button.grid(row=1, column=4, padx=10, pady=10)

    def identificar_rotas_maior_passageiros(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para identificar as rotas com maior número de passageiros
            query = """
                SELECT rp.linha_id AS rota,
                        SUM(pp.quantidade_pessoas) AS total_passageiros_2_meses
                FROM 
                    rotas_paragens rp
                    JOIN 
                        pessoas_paragem pp ON rp.paragem_id = pp.paragem_id
                        GROUP BY 
                            rp.linha_id
                                ORDER BY 
                                    total_passageiros_2_meses DESC;
            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Exibir resultados
            if resultados:
                resultado_texto = "Rotas com Maior Número de Passageiros:\n\n"
                for linha in resultados:
                    resultado_texto += f"Rota {linha[0]}: {linha[1]} passageiros\n"
                messagebox.showinfo("Resultados", resultado_texto)
            else:
                messagebox.showinfo("Resultados", "Nenhuma rota encontrada com passageiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao identificar rotas: {e}")

    def identificar_tipos_autocarro(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para identificar os tipos de autocarro e respetivos condutores
            query = """
            SELECT
                a.matricula,
                a.combustivel,
                c.nome AS condutor_nome,
                CASE
                    WHEN a.combustivel = 'elétrico' THEN 'Elétrico'
                    WHEN a.combustivel = 'Diesel' THEN 'Diesel'
                    WHEN a.combustivel = 'gasolina' THEN 'Gasolina'
                    WHEN a.combustivel = 'Híbrido' THEN 'Híbrido'
                END AS tipo_combustivel
            FROM 
                autocarros a
            JOIN 
                condutores_autocarros ca ON a.matricula = ca.matricula
            JOIN 
                condutores c ON ca.cartao_cidadao = c.cartao_cidadao
            ORDER BY 
                tipo_combustivel DESC, a.matricula;
            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar nova janela para exibir a tabela
            self.table_window = tk.Toplevel(self.root)
            self.table_window.title("Autocarros e Condutores")
            self.table_window.geometry("800x600")

            # Criar o Treeview (tabela) para exibir os resultados
            treeview = ttk.Treeview(self.table_window, columns=(
                "Matrícula", "Combustível", "Condutor", "Tipo de Combustível"), show="headings")
            treeview.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

            # Definir as colunas do Treeview
            treeview.heading("Matrícula", text="Matrícula")
            treeview.heading("Combustível", text="Combustível")
            treeview.heading("Condutor", text="Condutor")
            treeview.heading("Tipo de Combustível", text="Tipo de Combustível")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(self.table_window, orient="vertical", command=treeview.yview)
            treeview.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(row=0, column=4, sticky="ns", padx=10)

            # Número de linhas a serem exibidas por "página"
            num_linhas_por_pagina = 50
            total_linhas = len(resultados)

            def mostrar_pagina(pagina):
                """ Função para mostrar as linhas de acordo com a página selecionada """
                for item in treeview.get_children():
                    treeview.delete(item)

                # Limitar a quantidade de linhas por página
                start = pagina * num_linhas_por_pagina
                end = start + num_linhas_por_pagina
                for i in range(start, min(end, total_linhas)):
                    matricula, combustivel, condutor_nome, tipo_combustivel = resultados[i]
                    treeview.insert("", "end", values=(matricula, combustivel, condutor_nome, tipo_combustivel))

            # Variável para armazenar a página atual
            pagina_atual = 0
            mostrar_pagina(pagina_atual)

            # Botões para navegação
            nav_frame = tk.Frame(self.table_window)
            nav_frame.grid(row=1, column=0, columnspan=3, pady=10)

            def proxima_pagina():
                nonlocal pagina_atual
                if (pagina_atual + 1) * num_linhas_por_pagina < total_linhas:
                    pagina_atual += 1
                    mostrar_pagina(pagina_atual)

            def pagina_anterior():
                nonlocal pagina_atual
                if pagina_atual > 0:
                    pagina_atual -= 1
                    mostrar_pagina(pagina_atual)

            # Botões de navegação
            prev_button = ttk.Button(nav_frame, text="Página Anterior", command=pagina_anterior)
            prev_button.pack(side="left", padx=5)

            next_button = ttk.Button(nav_frame, text="Próxima Página", command=proxima_pagina)
            next_button.pack(side="left", padx=5)

            # Desabilitar o botão "Próxima Página" se não houver mais páginas
            if total_linhas <= num_linhas_por_pagina:
                next_button.config(state="disabled")

            # Desabilitar o botão "Página Anterior" se estiver na primeira página
            if pagina_atual == 0:
                prev_button.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def identificar_paragens_maior_afluencia(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para identificar as paragens com maior afluência de passageiros
            query = """
                SELECT p.nome AS paragem, SUM(pp.quantidade_pessoas) AS total_passageiros_2_meses
                FROM 
                    paragens p
                JOIN 
                    pessoas_paragem pp ON p.paragem_id = pp.paragem_id
                GROUP BY 
                    p.nome
                ORDER BY 
                    total_passageiros_2_meses DESC;
            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.table_window = tk.Toplevel(self.root)
            self.table_window.title("Paragens com Maior Afluência de Passageiros")
            self.table_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.table_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Paragem", "Total de Passageiros"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Paragem", text="Paragem")
            treeview.heading("Total de Passageiros", text="Total de Passageiros")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
            scrollbar.pack(side="right", fill="y")
            treeview.configure(yscrollcommand=scrollbar.set)

            # Número de linhas a serem exibidas por "página"
            num_linhas_por_pagina = 50
            total_linhas = len(resultados)

            def mostrar_pagina(pagina):
                """ Função para mostrar as linhas de acordo com a página selecionada """
                for item in treeview.get_children():
                    treeview.delete(item)

                # Limitar a quantidade de linhas por página
                start = pagina * num_linhas_por_pagina
                end = start + num_linhas_por_pagina
                for i in range(start, min(end, total_linhas)):
                    paragem, total_passageiros = resultados[i]
                    treeview.insert("", "end", values=(paragem, total_passageiros))

            # Variável para armazenar a página atual
            pagina_atual = 0
            mostrar_pagina(pagina_atual)

            # Botões para navegação
            nav_frame = tk.Frame(self.table_window)
            nav_frame.pack(fill="x", padx=10, pady=5)

            def proxima_pagina():
                nonlocal pagina_atual
                if pagina_atual * num_linhas_por_pagina + num_linhas_por_pagina < total_linhas:
                    pagina_atual += 1
                    mostrar_pagina(pagina_atual)

            def pagina_anterior():
                nonlocal pagina_atual
                if pagina_atual > 0:
                    pagina_atual -= 1
                    mostrar_pagina(pagina_atual)

            # Botões de navegação
            prev_button = ttk.Button(nav_frame, text="Página Anterior", command=pagina_anterior)
            prev_button.pack(side="left", padx=5)

            next_button = ttk.Button(nav_frame, text="Próxima Página", command=proxima_pagina)
            next_button.pack(side="left", padx=5)

            # Desabilitar o botão "Próxima Página" se não houver mais páginas
            if total_linhas <= num_linhas_por_pagina:
                next_button.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao identificar paragens: {e}")

    def analisar_qualidade_ar(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta SQL para juntar os dados ambientais e as paragens
            query = """
                SELECT p.nome AS paragem, 
                       da.temperatura, 
                       da.co2, 
                       da.co, 
                       da.no2, 
                       da.o3, 
                       da.pm10, 
                       da.humidade, 
                       da.hora
                FROM 
                    dados_ambientais da
                JOIN 
                    paragens p ON da.paragem_id = p.paragem_id
                ORDER BY 
                    da.hora DESC; 
            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.table_window = tk.Toplevel(self.root)
            self.table_window.title("Análise da Qualidade do Ar nas Paragens")
            self.table_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.table_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=(
            "Paragem", "Temperatura", "CO2", "CO", "NO2", "O3", "PM10", "Humidade", "Hora"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Paragem", text="Paragem")
            treeview.heading("Temperatura", text="Temperatura (°C)")
            treeview.heading("CO2", text="CO2 (ppm)")
            treeview.heading("CO", text="CO (ppm)")
            treeview.heading("NO2", text="NO2 (ppm)")
            treeview.heading("O3", text="O3 (ppm)")
            treeview.heading("PM10", text="PM10 (µg/m³)")
            treeview.heading("Humidade", text="Humidade (%)")
            treeview.heading("Hora", text="Hora da Medição")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
            scrollbar.pack(side="right", fill="y")
            treeview.configure(yscrollcommand=scrollbar.set)

            # Número de linhas a serem exibidas por "página"
            num_linhas_por_pagina = 50
            total_linhas = len(resultados)

            def mostrar_pagina(pagina):
                """ Função para mostrar as linhas de acordo com a página selecionada """
                for item in treeview.get_children():
                    treeview.delete(item)

                # Limitar a quantidade de linhas por página
                start = pagina * num_linhas_por_pagina
                end = start + num_linhas_por_pagina
                for i in range(start, min(end, total_linhas)):
                    paragem, temperatura, co2, co, no2, o3, pm10, humidade, hora = resultados[i]
                    treeview.insert("", "end", values=(paragem, temperatura, co2, co, no2, o3, pm10, humidade, hora))

            # Variável para armazenar a página atual
            pagina_atual = 0
            mostrar_pagina(pagina_atual)

            # Botões para navegação
            nav_frame = tk.Frame(self.table_window)
            nav_frame.pack(fill="x", padx=10, pady=5)

            def proxima_pagina():
                nonlocal pagina_atual
                if pagina_atual * num_linhas_por_pagina + num_linhas_por_pagina < total_linhas:
                    pagina_atual += 1
                    mostrar_pagina(pagina_atual)

            def pagina_anterior():
                nonlocal pagina_atual
                if pagina_atual > 0:
                    pagina_atual -= 1
                    mostrar_pagina(pagina_atual)

            # Botões de navegação
            prev_button = ttk.Button(nav_frame, text="Página Anterior", command=pagina_anterior)
            prev_button.pack(side="left", padx=5)

            next_button = ttk.Button(nav_frame, text="Próxima Página", command=proxima_pagina)
            next_button.pack(side="left", padx=5)

            # Desabilitar o botão "Próxima Página" se não houver mais páginas
            if total_linhas <= num_linhas_por_pagina:
                next_button.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao analisar qualidade do ar: {e}")

    def calcular_velocidade_congestionamento(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta SQL para calcular a velocidade dos veículos por segmento de rua, incluindo o nome da rua
            query = """
                            SELECT 
				r.nome AS rua,
                s.segmento_id,
                AVG(v.velocidades) AS velocidade_media
            FROM 
                velocidades v
            JOIN 
                segmentos s ON v.segmento_id = s.segmento_id
            JOIN 
                ruas r ON s.rua_id = r.rua_id
            GROUP BY 
                s.segmento_id, r.nome
            ORDER BY 
                velocidade_media ASC;

            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir os resultados
            self.table_window = tk.Toplevel(self.root)
            self.table_window.title("Velocidade dos Veículos por Segmento de Rua")
            self.table_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.table_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Segmento", "Rua", "Velocidade Média (km/h)"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Segmento", text="Segmento")
            treeview.heading("Rua", text="Rua")
            treeview.heading("Velocidade Média (km/h)", text="Velocidade Média (km/h)")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
            scrollbar.pack(side="right", fill="y")
            treeview.configure(yscrollcommand=scrollbar.set)

            # Número de linhas a serem exibidas por "página"
            num_linhas_por_pagina = 50
            total_linhas = len(resultados)

            def mostrar_pagina(pagina):
                """ Função para mostrar as linhas de acordo com a página selecionada """
                for item in treeview.get_children():
                    treeview.delete(item)

                # Limitar a quantidade de linhas por página
                start = pagina * num_linhas_por_pagina
                end = start + num_linhas_por_pagina
                for i in range(start, min(end, total_linhas)):
                    segmento_id, rua, velocidade_media = resultados[i]
                    # Convertendo a velocidade média para km/h
                    velocidade_media_kmh = velocidade_media  # Se os dados já estiverem em km/h
                    treeview.insert("", "end", values=(segmento_id, rua, round(velocidade_media_kmh, 2)))

            # Variável para armazenar a página atual
            pagina_atual = 0
            mostrar_pagina(pagina_atual)

            # Botões para navegação
            nav_frame = tk.Frame(self.table_window)
            nav_frame.pack(fill="x", padx=10, pady=5)

            def proxima_pagina():
                nonlocal pagina_atual
                if pagina_atual * num_linhas_por_pagina + num_linhas_por_pagina < total_linhas:
                    pagina_atual += 1
                    mostrar_pagina(pagina_atual)

            def pagina_anterior():
                nonlocal pagina_atual
                if pagina_atual > 0:
                    pagina_atual -= 1
                    mostrar_pagina(pagina_atual)

            # Botões de navegação
            prev_button = ttk.Button(nav_frame, text="Página Anterior", command=pagina_anterior)
            prev_button.pack(side="left", padx=5)

            next_button = ttk.Button(nav_frame, text="Próxima Página", command=proxima_pagina)
            next_button.pack(side="left", padx=5)

            # Desabilitar o botão "Próxima Página" se não houver mais páginas
            if total_linhas <= num_linhas_por_pagina:
                next_button.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular a velocidade nos segmentos de rua: {e}")

    def listar_veiculos_por_segmento(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para listar os tipos de veículos e quantificar o tráfego
            query = """
            SELECT 
                s.segmento_id,
                r.nome AS rua,
                ve.tipo AS tipo_veiculo,
                COUNT(v.matricula) AS quantidade_veiculos_tipo,
                (SELECT COUNT(*) 
                 FROM velocidades v2 
                 WHERE v2.segmento_id = s.segmento_id) AS total_trafego_segmento
            FROM 
                velocidades v
            JOIN 
                veiculos ve ON v.matricula = ve.matricula
            JOIN 
                segmentos s ON s.segmento_id = v.segmento_id
            JOIN 
                ruas r ON r.rua_id = s.rua_id
            GROUP BY 
                r.nome, s.segmento_id, ve.tipo
            ORDER BY 
                s.segmento_id, quantidade_veiculos_tipo DESC;
            """
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.resultados_window = tk.Toplevel(self.root)
            self.resultados_window.title("Tipos de Veículos e Tráfego por Segmento")
            self.resultados_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.resultados_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Segmento ID", "Rua", "Tipo de Veículo", "Quantidade de Veículos", "Total Tráfego"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Segmento ID", text="Segmento ID")
            treeview.heading("Rua", text="Rua")
            treeview.heading("Tipo de Veículo", text="Tipo de Veículo")
            treeview.heading("Quantidade de Veículos", text="Quantidade de Veículos")
            treeview.heading("Total Tráfego", text="Total de Tráfego")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
            scrollbar.pack(side="right", fill="y")
            treeview.configure(yscrollcommand=scrollbar.set)

            # Preencher a tabela com os resultados
            for linha in resultados:
                segmento_id, rua, tipo_veiculo, quantidade_veiculos_tipo, total_trafego_segmento = linha
                treeview.insert("", "end", values=(segmento_id, rua, tipo_veiculo, quantidade_veiculos_tipo, total_trafego_segmento))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def ocupacao_estacionameto(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para monitorizar a taxa de ocupação dos estacionamentos
            query = """
                    SELECT 
            e.nome AS estacionamento,
            e.tipo AS tipo_estacionamento,
            r.nome AS rua,
            COUNT(l.lugar_id) AS total_lugares,
            SUM(CASE WHEN l.ocupaçao = 1 THEN 1 ELSE 0 END) AS lugares_ocupados,
            (SUM(CASE WHEN l.ocupaçao = 1 THEN 1 ELSE 0 END) * 100.0 / e.capacidade) AS taxa_ocupacao
        FROM 
            estacionamento e
        JOIN 
            ruas r ON r.rua_id = e.rua_id
        JOIN 
            lugares l ON l.estacionamento_id = e.estacionamento_id
        GROUP BY 
            e.nome, e.tipo, r.nome, e.capacidade
        ORDER BY 
            taxa_ocupacao DESC;
            """

            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.resultados_window = tk.Toplevel(self.root)
            self.resultados_window.title("Taxa de Ocupação dos Estacionamentos")
            self.resultados_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.resultados_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=(
                "Estacionamento", "Tipo", "Rua", "Total Lugares", "Lugares Ocupados", "Taxa de Ocupação"),
                                    show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Estacionamento", text="Estacionamento")
            treeview.heading("Tipo", text="Tipo de Estacionamento")
            treeview.heading("Rua", text="Rua")
            treeview.heading("Total Lugares", text="Total de Lugares")
            treeview.heading("Lugares Ocupados", text="Lugares Ocupados")
            treeview.heading("Taxa de Ocupação", text="Taxa de Ocupação (%)")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(self.resultados_window, orient="vertical", command=treeview.yview)
            treeview.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Preencher a tabela com os resultados
            for linha in resultados:
                estacionamento, tipo, rua, total_lugares, lugares_ocupados, taxa_ocupacao = linha
                treeview.insert("", "end", values=(
                estacionamento, tipo, rua, total_lugares, lugares_ocupados, f"{taxa_ocupacao:.2f}%"))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def velocidade_media_veiculos(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para calcular a velocidade média dos veículos
            query = """
                SELECT 
    ve.matricula, 
    ve.marca,
    ve.tipo,
    AVG(vel.velocidades) AS velocidade_media
FROM 
    velocidades vel
JOIN 
    veiculos ve ON vel.matricula = ve.matricula
GROUP BY 
    ve.matricula, ve.marca, ve.tipo
ORDER BY 
                velocidade_media DESC;

            """

            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.resultados_window = tk.Toplevel(self.root)
            self.resultados_window.title("Velocidade Média dos Veículos")
            self.resultados_window.geometry("900x600")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.resultados_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Matricula", "Marca", "Tipo", "Velocidade Média"),
                                    show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Matricula", text="Matrícula")
            treeview.heading("Marca", text="Marca")
            treeview.heading("Tipo", text="Tipo")
            treeview.heading("Velocidade Média", text="Velocidade Média (km/h)")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(self.resultados_window, orient="vertical", command=treeview.yview)
            treeview.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Preencher a tabela com os resultados
            for linha in resultados:
                matricula, marca, tipo, velocidade_media = linha
                treeview.insert("", "end", values=(matricula, marca, tipo, f"{velocidade_media:.2f} km/h"))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def rotas_com_paragens(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para contar o número de paragens por rota
            query = """
                SELECT 
                    r.linha_id, 
                    COUNT(rp.paragem_id) AS numero_paragens
                FROM 
                    rotas r
                JOIN 
                    rotas_paragens rp ON r.linha_id = rp.linha_id
                GROUP BY 
                    r.linha_id
                ORDER BY 
                    numero_paragens DESC;
            """

            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.resultados_window = tk.Toplevel(self.root)
            self.resultados_window.title("Rotas e o Número de Paragens")
            self.resultados_window.geometry("600x400")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.resultados_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Linha ID", "Número de Paragens"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Linha ID", text="Linha ID")
            treeview.heading("Número de Paragens", text="Número de Paragens")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(self.resultados_window, orient="vertical", command=treeview.yview)
            treeview.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Preencher a tabela com os resultados
            for linha in resultados:
                linha_id, numero_paragens = linha
                treeview.insert("", "end", values=(linha_id, numero_paragens))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def paragens_com_alto_co2(self):
        if not self.conn or not self.cursor:
            messagebox.showwarning("Aviso", "Conecte-se à base de dados antes de continuar.")
            return

        try:
            # Consulta para encontrar paragens com CO2 maior que 400
            query = """
                SELECT 
                    p.nome AS paragem,
                    da.co2
                FROM 
                    dados_ambientais da
                JOIN 
                    paragens p ON da.paragem_id = p.paragem_id
                WHERE 
                    da.co2 > 450
                ORDER BY 
                    da.co2 DESC;
            """

            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Criar uma nova janela para exibir a tabela
            self.resultados_window = tk.Toplevel(self.root)
            self.resultados_window.title("Paragens com CO2 Alto")
            self.resultados_window.geometry("600x400")

            # Criar Frame para organizar o Treeview e a barra de rolagem
            frame = tk.Frame(self.resultados_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Criar Treeview para exibir os dados
            treeview = ttk.Treeview(frame, columns=("Paragem", "CO2"), show="headings")
            treeview.pack(side="left", fill="both", expand=True)

            # Definir as colunas do Treeview
            treeview.heading("Paragem", text="Paragem")
            treeview.heading("CO2", text="Nível de CO2")

            # Barra de rolagem
            scrollbar = ttk.Scrollbar(self.resultados_window, orient="vertical", command=treeview.yview)
            treeview.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Preencher a tabela com os resultados
            for linha in resultados:
                paragem, co2 = linha
                treeview.insert("", "end", values=(paragem, co2))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
