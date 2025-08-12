# Migrador de Perfil Fácil para Windows

Este é um script em Python com uma interface gráfica simples (Tkinter) para ajudar a migrar dados de um perfil de usuário para outro no mesmo computador Windows.

## Funcionalidades

- **Interface Gráfica Intuitiva:** Selecione o usuário de origem e destino em menus suspensos.
- **Segurança Aprimorada:** O script impede a seleção do usuário atualmente logado para evitar corrupção de dados.
- **Log de Atividades:** A interface mostra em tempo real quais arquivos estão sendo copiados.
- **Cópia Segura:** Ignora arquivos críticos do sistema (`NTUSER.dat`, etc.) para não danificar o perfil de destino.

## Como Usar

1.  **Pré-requisito:** Tenha o [Python](https://www.python.org/downloads/windows/) instalado em seu computador.
2.  **Faça o login em uma conta de Administrador** que NÃO seja a de origem nem a de destino.
3.  Baixe o arquivo `migrador_de_perfil.py`.
4.  Clique com o botão direito no arquivo e selecione **"Executar como administrador"**.
5.  Selecione o perfil de origem e o de destino na janela do programa.
6.  Clique em "Iniciar Migração".

### ⚠️ Aviso Importante

- **Faça backup!** Sempre copie seus arquivos mais importantes para um local seguro antes de usar esta ferramenta.
- **Senhas não são migradas.** Por razões de segurança, senhas salvas em navegadores e outros aplicativos não são copiadas. Você deve exportá-las e importá-las manualmente.
- **Use por sua conta e risco.** Este script modifica um grande volume de arquivos. O autor não se responsabiliza por qualquer perda de dados.