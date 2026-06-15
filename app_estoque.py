import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import os

# ==========================================
# PERSISTÊNCIA (Banco de Dados - Mantido)
# ==========================================
class BancoDeDados:
    def __init__(self, db_name="estoque.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def inserir(self, nome, quantidade, preco):
        self.cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        self.conn.commit()

    def consultar_todos(self):
        self.cursor.execute("SELECT * FROM produtos")
        return self.cursor.fetchall()

    def atualizar(self, id_produto, nome, quantidade, preco):
        self.cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id_produto))
        self.conn.commit()

    def deletar(self, id_produto):
        self.cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
        self.conn.commit()
        
    def consultar_estoque_baixo(self, limite=5):
        self.cursor.execute("SELECT * FROM produtos WHERE quantidade <= ?", (limite,))
        return self.cursor.fetchall()

# ==========================================
# INTERFACE GRÁFICA PREMIUM
# ==========================================
class AppEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("StockMaster Pro - Controle de Estoque")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f6f9")  # Fundo cinza-claro moderno
        self.db = BancoDeDados()

        # Configuração de Estilo do TTK (Tabela)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Estilizando a Tabela (Treeview)
        self.style.configure("Treeview", 
                             background="#ffffff", 
                             foreground="#333333", 
                             rowheight=28, 
                             fieldbackground="#ffffff",
                             font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", 
                             background="#2c3e50", 
                             foreground="#ffffff", 
                             font=("Segoe UI", 10, "bold"),
                             relief="flat")
        self.style.map("Treeview", background=[('selected', '#3498db')], foreground=[('selected', '#ffffff')])

        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        # 1. CABEÇALHO DO SISTEMA
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_titulo = tk.Label(header, text="STOCKMASTER PRO", fg="#ffffff", bg="#2c3e50", font=("Segoe UI", 14, "bold"))
        lbl_titulo.pack(side="left", padx=20, pady=15)
        
        lbl_subtitulo = tk.Label(header, text="|  Gestão de Inventário RAD", fg="#bdc3c7", bg="#2c3e50", font=("Segoe UI", 10, "italic"))
        lbl_subtitulo.pack(side="left", pady=18)

        # Container Principal com margens
        container = tk.Frame(self.root, bg="#f4f6f9", padx=20, pady=15)
        container.pack(fill="both", expand=True)

        # 2. FORMULÁRIO DE ENTRADA
        frame_inputs = tk.LabelFrame(container, text=" Cadastro e Edição de Itens ", bg="#ffffff", fg="#2c3e50", font=("Segoe UI", 10, "bold"), padx=15, pady=15, relief="solid", bd=1)
        frame_inputs.pack(fill="x", pady=5)

        # Grid de Inputs
        tk.Label(frame_inputs, text="Nome do Produto:", bg="#ffffff", fg="#555555", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_inputs, width=35, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_inputs, text="Quantidade:", bg="#ffffff", fg="#555555", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_qtd = tk.Entry(frame_inputs, width=12, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_qtd.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frame_inputs, text="Preço Unitário (R$):", bg="#ffffff", fg="#555555", font=("Segoe UI", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.entry_preco = tk.Entry(frame_inputs, width=12, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_preco.grid(row=0, column=5, padx=10, pady=5)

        # 3. PAINEL DE AÇÕES (BOTÕES ESTILIZADOS)
        frame_botoes = tk.Frame(container, bg="#f4f6f9", pady=10)
        frame_botoes.pack(fill="x")

        # Botões Principais (Esquerda)
        btn_add = tk.Button(frame_botoes, text="+ Adicionar", command=self.adicionar_produto, bg="#2abc68", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#27ae60", activeforeground="white")
        btn_add.pack(side="left", padx=4)

        btn_edit = tk.Button(frame_botoes, text="💾 Atualizar", command=self.atualizar_produto, bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#2980b9", activeforeground="white")
        btn_edit.pack(side="left", padx=4)

        btn_del = tk.Button(frame_botoes, text="🗑️ Excluir", command=self.excluir_produto, bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#c0392b", activeforeground="white")
        btn_del.pack(side="left", padx=4)

        btn_clear = tk.Button(frame_botoes, text="Limpar", command=self.limpar_campos, bg="#95a5a6", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=6, cursor="hand2", activebackground="#7f8c8d", activeforeground="white")
        btn_clear.pack(side="left", padx=4)

        # Botões de Inteligência/Relatório (Direita)
        btn_json = tk.Button(frame_botoes, text="📥 Exportar Backup (JSON)", command=self.exportar_json, bg="#7f8c8d", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=6, cursor="hand2")
        btn_json.pack(side="right", padx=4)

        self.btn_filtro = tk.Button(frame_botoes, text="⚠️ Alerta: Estoque Baixo", command=self.alternar_filtre, bg="#f1c40f", fg="#2c3e50", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=6, cursor="hand2", activebackground="#f39c12")
        self.btn_filtro.pack(side="right", padx=4)
        
        self.filtrado = False # Controle do estado do botão de relatório

        # 4. PAINEL DA TABELA
        frame_tabela = tk.Frame(container, bg="#ffffff", relief="solid", bd=1)
        frame_tabela.pack(fill="both", expand=True, pady=10)

        colunas = ("ID", "Nome do Produto", "Quantidade em Estoque", "Preço Unitário")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome do Produto", text="NOME DO PRODUTO")
        self.tree.heading("Quantidade em Estoque", text="QTD EM ESTOQUE")
        self.tree.heading("Preço Unitário", text="PREÇO UNITÁRIO")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome do Produto", width=350, anchor="w")
        self.tree.column("Quantidade em Estoque", width=150, anchor="center")
        self.tree.column("Preço Unitário", width=150, anchor="center")

        # Scrollbar Integrada
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self.selecionar_registro)

        # 5. BARRA DE STATUS
        self.lbl_status = tk.Label(self.root, text=" Sistema pronto. ", bd=1, relief="flat", anchor="w", bg="#2c3e50", fg="#ffffff", font=("Segoe UI", 9), padx=10, pady=4)
        self.lbl_status.pack(side="bottom", fill="x")

    # ==========================================
    # LÓGICA DE VALIDAÇÃO E CRUD
    # ==========================================
    def validar_entradas(self):
        nome = self.entry_nome.get().strip()
        qtd_str = self.entry_qtd.get().strip()
        preco_str = self.entry_preco.get().strip()

        if not nome or not qtd_str or not preco_str:
            messagebox.showerror("Campos Vazios", "Por favor, preencha todos os campos do formulário.")
            return None

        try:
            quantidade = int(qtd_str)
            preco = float(preco_str.replace(',', '.'))
            if quantidade < 0 or preco < 0:
                raise ValueError()
            return (nome, quantidade, preco)
        except ValueError:
            messagebox.showerror("Dados Inválidos", "Quantidade deve ser um número inteiro positivo.\nPreço deve ser um valor decimal válido (ex: 19.90).")
            return None

    def carregar_dados(self, linhas=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if linhas is None:
            linhas = self.db.consultar_todos()
            
        for linha in linhas:
            # Formata o preço para a exibição visual ficar profissional (R$ XX,XX)
            id_p, nome, qtd, preco = linha
            preco_formatado = f"R$ {preco:,.2f}".replace('.', ',')
            self.tree.insert("", "end", values=(id_p, nome, qtd, preco_formatado))
        
        self.atualizar_barra_status(f"Total de itens listados: {len(linhas)}")

    def adicionar_produto(self):
        dados = self.validar_entradas()
        if dados:
            self.db.inserir(dados[0], dados[1], dados[2])
            self.limpar_campos()
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso ao inventário!")

    def selecionar_registro(self, event):
        item_selecionado = self.tree.focus()
        if item_selecionado:
            valores = self.tree.item(item_selecionado, 'values')
            self.limpar_campos()
            self.entry_nome.insert(0, valores[1])
            self.entry_qtd.insert(0, valores[2])
            # Remove o 'R$ ' e volta a vírgula para ponto ao jogar no campo de edição
            preco_limpo = valores[3].replace('R$ ', '').replace(',', '.')
            self.entry_preco.insert(0, preco_limpo)

    def atualizar_produto(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Seleção Ausente", "Selecione um produto na tabela antes de clicar em Atualizar.")
            return
            
        id_produto = self.tree.item(item_selecionado, 'values')[0]
        dados = self.validar_entradas()
        
        if dados:
            self.db.atualizar(id_produto, dados[0], dados[1], dados[2])
            self.limpar_campos()
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Dados do produto atualizados com sucesso!")

    def excluir_produto(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Seleção Ausente", "Selecione o produto que deseja remover da tabela.")
            return
            
        valores = self.tree.item(item_selecionado, 'values')
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja apagar permanentemente o produto:\n'{valores[1]} '?")
        if resposta:
            self.db.deletar(valores[0])
            self.limpar_campos()
            self.carregar_dados()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)

    # ==========================================
    # RELATÓRIOS E EXPORTAÇÃO ADVANCED
    # ==========================================
    def alternar_filtre(self):
        """ Alterna entre o relatório de estoque baixo e a visão geral """
        if not self.filtrado:
            linhas = self.db.consultar_estoque_baixo(limite=5)
            self.carregar_dados(linhas)
            self.btn_filtro.configure(text="👁️ Mostrar Todos", bg="#34495e", fg="white")
            self.filtrado = True
            self.atualizar_barra_status(f"Filtro Ativo: Exibindo apenas itens com estoque crítico (<= 5 unidades).")
        else:
            self.carregar_dados()
            self.btn_filtro.configure(text="⚠️ Alerta: Estoque Baixo", bg="#f1c40f", fg="#2c3e50")
            self.filtrado = False

    def exportar_json(self):
        dados = self.db.consultar_todos()
        lista_dicionarios = [{"id": linha[0], "nome": linha[1], "quantidade": linha[2], "preco": linha[3]} for linha in dados]
        
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(lista_dicionarios, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Backup Concluído", f"Dados exportados com sucesso para:\n{os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Falha na Exportação", f"Ocorreu um erro ao salvar o arquivo: {e}")

    def atualizar_barra_status(self, texto):
        self.lbl_status.configure(text=f" 🖥️ {texto}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppEstoque(root)
    root.mainloop()