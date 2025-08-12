import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ctypes
import sys

# --- Funções do Núcleo da Aplicação ---

def is_admin():
    """Verifica se o script está rodando com privilégios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_user_profiles():
    """
    Busca os diretórios de perfis de usuário em C:\\Users,
    IGNORANDO o usuário atualmente logado para segurança.
    """
    users_path = "C:\\Users"
    # Adicionamos o usuário logado à lista de exclusão
    try:
        # Pega o nome do usuário da sessão atual. É mais confiável.
        logged_in_user = os.getlogin()
    except OSError:
        # Como fallback, caso getlogin() falhe em alguns contextos
        logged_in_user = os.environ.get('USERNAME')

    excluded_users = {'Default', 'Default User', 'Public', 'All Users', logged_in_user}
    
    profiles = []
    if os.path.exists(users_path):
        for item in os.listdir(users_path):
            if os.path.isdir(os.path.join(users_path, item)) and item not in excluded_users:
                profiles.append(item)
    return profiles, logged_in_user

def copy_profile_data(source_user, dest_user, text_widget):
    """Copia os dados de um perfil para outro, com logs e exclusões."""
    source_path = f"C:\\Users\\{source_user}"
    dest_path = f"C:\\Users\\{dest_user}"
    
    # Arquivos críticos a serem ignorados para não corromper o perfil de destino
    files_to_ignore = ['ntuser.dat', 'ntuser.dat.log', 'ntuser.dat.log1', 'ntuser.dat.log2', 'ntuser.ini']

    def log(message):
        """Função para adicionar mensagens na caixa de texto da interface."""
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)
        text_widget.update_idletasks()

    log(f"Iniciando migração de '{source_user}' para '{dest_user}'.")
    log("="*40)
    
    if not os.path.exists(dest_path):
        log(f"ERRO: O diretório de destino {dest_path} não existe.")
        log("Por favor, faça login uma vez com o usuário de destino para que a pasta seja criada.")
        return

    # Percorre todos os arquivos e pastas da origem
    for root, dirs, files in os.walk(source_path):
        # Ignora a verificação dos arquivos críticos na raiz do perfil
        if os.path.samefile(root, source_path):
            items_to_process = files + dirs
        else:
            items_to_process = files + dirs
        
        for item in items_to_process:
            source_item_path = os.path.join(root, item)
            
            # Checa se o item deve ser ignorado
            if item.lower() in [f.lower() for f in files_to_ignore] and os.path.samefile(root, source_path):
                log(f"IGNORANDO: Arquivo de sistema crítico '{item}'")
                continue

            # Cria o caminho de destino correspondente
            relative_path = os.path.relpath(source_item_path, source_path)
            dest_item_path = os.path.join(dest_path, relative_path)

            try:
                if os.path.isdir(source_item_path):
                    if not os.path.exists(dest_item_path):
                        os.makedirs(dest_item_path)
                else: # se for arquivo
                    os.makedirs(os.path.dirname(dest_item_path), exist_ok=True)
                    shutil.copy2(source_item_path, dest_item_path)
                    log(f"COPIADO: {relative_path}")
            except Exception as e:
                log(f"ERRO ao copiar '{item}': {e}")
    
    log("="*40)
    log("MIGRAÇÃO CONCLUÍDA!")
    log("\nLEMBRETES IMPORTANTES:")
    log("1. Senhas NÃO foram copiadas. Exporte/importe manualmente pelo seu navegador.")
    log("2. Aplicativos da Microsoft Store podem precisar ser reinstalados no novo usuário.")
    messagebox.showinfo("Sucesso", "A migração de dados foi concluída com sucesso! Verifique o log para detalhes.")

# --- Classe da Interface Gráfica ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Migrador de Perfil Fácil (Seguro)")
        self.geometry("600x650")
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Migrador de Perfil Fácil", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        # Frame de Instruções
        instructions_frame = ttk.LabelFrame(main_frame, text="Instruções Importantes", padding="10")
        instructions_frame.pack(fill="x", pady=5)
        
        self.logged_in_user_label = ttk.Label(instructions_frame, text="Aguardando detecção...", foreground="blue")
        self.logged_in_user_label.pack(anchor="w")
        ttk.Label(instructions_frame, text="Para realizar a migração, você deve estar logado em uma\nconta de Administrador que NÃO seja a de origem nem a de destino.").pack(anchor="w")

        user_frame = ttk.LabelFrame(main_frame, text="1. Selecione os Usuários", padding="10")
        user_frame.pack(fill="x", pady=5)

        ttk.Label(user_frame, text="Copiar de (Origem):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_user_var = tk.StringVar()
        self.source_user_menu = ttk.Combobox(user_frame, textvariable=self.source_user_var, state="readonly", width=40)
        self.source_user_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Para (Destino):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_user_var = tk.StringVar()
        self.dest_user_menu = ttk.Combobox(user_frame, textvariable=self.dest_user_var, state="readonly", width=40)
        self.dest_user_menu.grid(row=1, column=1, padx=5, pady=5)

        self.populate_user_menus()

        action_frame = ttk.LabelFrame(main_frame, text="2. Iniciar o Processo", padding="10")
        action_frame.pack(fill="x", pady=10)

        self.start_button = ttk.Button(action_frame, text="Iniciar Migração", command=self.start_migration)
        self.start_button.pack(pady=10)

        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.pack(fill="both", expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=13, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def populate_user_menus(self):
        profiles, logged_in_user = get_user_profiles()
        self.logged_in_user_label.config(text=f"Usuário atual (ignorado): {logged_in_user}")
        
        if not profiles:
            messagebox.showwarning("Atenção", "Nenhum outro perfil de usuário foi encontrado para migração.\n\nLembre-se que você precisa de pelo menos duas outras contas além da sua.")
            self.source_user_menu['values'] = [""]
            self.dest_user_menu['values'] = [""]
        else:
            self.source_user_menu['values'] = profiles
            self.dest_user_menu['values'] = profiles

    def start_migration(self):
        source = self.source_user_var.get()
        dest = self.dest_user_var.get()

        if not source or not dest:
            messagebox.showerror("Erro", "Por favor, selecione um usuário de origem e um de destino.")
            return

        if source == dest:
            messagebox.showerror("Erro", "O usuário de origem e de destino não podem ser o mesmo.")
            return
            
        confirmation = messagebox.askyesno(
            "Confirmação Final",
            f"Você tem certeza que deseja copiar TUDO de '{source}' para '{dest}'?\n\n"
            f"AVISO: Arquivos existentes em '{dest}' com o mesmo nome serão SOBRESCRITOS.\n"
            "É ALTAMENTE RECOMENDADO FAZER UM BACKUP ANTES DE CONTINUAR."
        )

        if confirmation:
            self.log_text.delete(1.0, tk.END)
            self.start_button.config(state="disabled")
            copy_profile_data(source, dest, self.log_text)
            self.start_button.config(state="normal")


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        app = App()
        app.mainloop()