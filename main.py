import sqlite3
from tkinter import filedialog, messagebox, Tk
from scripts.extrair_backup import extrair_backup
from scripts.exportar_dados import exportar_clientes, exportar_processos

class MigracaoApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Migração de Dados")
        self.root.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        # Botão para selecionar e extrair o backup
        btn_extrair = filedialog.Button(
            self.root,
            text="Selecionar e Processar Backup",
            command=self.processar_backup
        )
        btn_extrair.pack(pady=10)

        # Botão para exportar clientes
        btn_exportar_clientes = filedialog.Button(
            self.root,
            text="Exportar Clientes",
            command=self.exportar_clientes
        )
        btn_exportar_clientes.pack(pady=10)

        # Botão para exportar processos
        btn_exportar_processos = filedialog.Button(
            self.root,
            text="Exportar Processos",
            command=self.exportar_processos
        )
        btn_exportar_processos.pack(pady=10)

    def processar_backup(self):
        try:
            arquivo = filedialog.askopenfilename(filetypes=[("Arquivos RAR", "*.rar")])
            if arquivo:
                extrair_backup(arquivo, "data/input")
                messagebox.showinfo("Sucesso", "Backup processado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar backup: {e}")

    def exportar_clientes(self):
        try:
            conn = sqlite3.connect("data/database.sqlite")
            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if caminho:
                exportar_clientes(conn, caminho)
                messagebox.showinfo("Sucesso", "Clientes exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar clientes: {e}")

    def exportar_processos(self):
        try:
            conn = sqlite3.connect("data/database.sqlite")
            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if caminho:
                exportar_processos(conn, caminho)
                messagebox.showinfo("Sucesso", "Processos exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar processos: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MigracaoApp()
    app.run()
