#!/usr/bin/env python3
# ============================================
#   TBF (Series G Edition)
#   by TBFPUMBA — Ultimate Git Manager
# ============================================

import os
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt

console = Console()

BANNER_TBF = """[bold blue]
   ████████╗██████╗ ███████╗
   ╚══██╔══╝██╔══██╗██╔════╝
      ██║   ██████╔╝█████╗  
      ██║   ██╔══██╗██╔══╝  
      ██║   ██████╔╝██║     
      ╚═╝   ╚═════╝ ╚═╝     
[/bold blue][bright_blue]
     [ TBF GIT MANAGER v1.1 ]
[/bright_blue]"""

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def show_header():
    clear()
    console.print(Align.center(BANNER_TBF))
    console.print(Align.center("[bold cyan]dev>[/bold cyan] [bold white]@TBFPUMBA[/bold white]   [bold cyan]series>[/bold cyan] [bold white]G Edition[/bold white]"))
    console.print()

def get_current_branch():
    out, _, code = run_cmd("git rev-parse --abbrev-ref HEAD 2>/dev/null")
    return out if code == 0 else "Не Git репозиторій"

def git_status():
    show_header()
    out, err, code = run_cmd("git status -s")
    if code != 0:
        console.print(Panel("[bold red]❌ Помилка: Поточна папка не є Git-репозиторієм![/bold red]", border_style="red"))
    elif not out:
        console.print(Panel("[bold green]✔ Робоча директорія чиста! Змін не виявлено.[/bold green]", title="📊 Git Status", border_style="green"))
    else:
        table = Table(title="📌 Змінені файли", border_style="cyan", expand=True)
        table.add_column("Статус", style="bold yellow", width=10)
        table.add_column("Файл", style="bold white")
        
        for line in out.splitlines():
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                st, fname = parts
                table.add_row(st, fname)
            else:
                table.add_row("?", line)
        console.print(table)
    
    input("\n[Натисніть Enter для повернення в меню...]")

def git_quick_commit():
    show_header()
    console.print("[bold cyan][+] Індексація файлів (git add .)...[/bold cyan]")
    run_cmd("git add .")
    
    msg = Prompt.ask("\n[bold yellow]📝 Введіть коментар до коміту[/bold yellow]", default="Update project")
    out, err, code = run_cmd(f'git commit -m "{msg}"')
    
    if code == 0:
        console.print(Panel(f"[bold green]✔ Коміт успішно створено![/bold green]\n\n[bold white]Коментар:[/bold white] {msg}", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка коміту:[/bold red]\n{err or out}", border_style="red"))
    
    input("\n[Натисніть Enter для повернення в меню...]")

def git_push():
    show_header()
    branch = get_current_branch()
    console.print(f"[bold cyan][+] Пуш змін на GitHub (гілка: {branch})...[/bold cyan]")
    
    out, err, code = run_cmd(f"git push origin {branch}")
    if code == 0:
        console.print(Panel("[bold green]🚀 Зміни успішно відправлені на GitHub![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка при git push:[/bold red]\n{err or out}", border_style="red"))
    
    input("\n[Натисніть Enter для повернення в меню...]")

def git_init():
    show_header()
    out, err, code = run_cmd("git init")
    if code == 0:
        console.print(Panel("[bold green]🎉 Новий Git-репозиторій успішно ініціалізовано![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка:[/bold red]\n{err}", border_style="red"))
    
    input("\n[Натисніть Enter для повернення в меню...]")

def git_log():
    show_header()
    out, err, code = run_cmd('git log -n 5 --pretty=format:"%h|%an|%s|%cr"')
    if code != 0 or not out:
        console.print(Panel("[bold yellow]⚠️ Історія комітів порожня або це не Git-репозиторій.[/bold yellow]", border_style="yellow"))
    else:
        table = Table(title="📜 Останні 5 комітів", border_style="blue", expand=True)
        table.add_column("Хеш", style="bold cyan", width=10)
        table.add_column("Автор", style="bold green", width=15)
        table.add_column("Коментар", style="bold white")
        table.add_column("Час", style="dim white", width=15)
        
        for line in out.splitlines():
            parts = line.split("|")
            if len(parts) == 4:
                table.add_row(*parts)
        console.print(table)
    
    input("\n[Натисніть Enter для повернення в меню...]")

def main():
    while True:
        show_header()
        branch = get_current_branch()
        
        info_panel = f"[bold yellow]Гілка:[/bold yellow] [bold green]{branch}[/bold green]  |  [bold yellow]Шлях:[/bold yellow] [dim]{os.getcwd()}[/dim]"
        console.print(Panel(info_panel, title="📍 Інформація", border_style="cyan"))
        console.print()
        
        console.print(" [bold cyan]1.[/bold cyan] 📊 Статус репозиторію [dim](git status)[/dim]")
        console.print(" [bold cyan]2.[/bold cyan] ⚡ Швидкий коміт [dim](git add . + git commit)[/dim]")
        console.print(" [bold cyan]3.[/bold cyan] 🚀 Пуш на GitHub [dim](git push origin)[/dim]")
        console.print(" [bold cyan]4.[/bold cyan] 📜 Історія комітів [dim](git log)[/dim]")
        console.print(" [bold cyan]5.[/bold cyan] 🎉 Ініціалізувати новий Git [dim](git init)[/dim]")
        console.print(" [bold red]0.[/bold red] ❌ Вихід\n")
        
        choice = Prompt.ask("Оберіть дію", choices=["1", "2", "3", "4", "5", "0"], default="1")
        
        if choice == "1":
            git_status()
        elif choice == "2":
            git_quick_commit()
        elif choice == "3":
            git_push()
        elif choice == "4":
            git_log()
        elif choice == "5":
            git_init()
        elif choice == "0":
            console.print("\n[bold red][!] Вихід з TBF-GitManager.[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()

