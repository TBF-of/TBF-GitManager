#!/usr/bin/env python3
# ============================================
#   TBF-GitManager v1.2.1 — by TBFPUMBA
#   Ultimate Git Manager for Termux / Linux
# ============================================

import os
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt, Confirm

console = Console()

BANNER_TBF = """[bold blue]
   ████████╗██████╗ ███████╗
   ╚══██╔══╝██╔══██╗██╔════╝
      ██║   ██████╔╝█████╗  
      ██║   ██╔══██╗██╔══╝  
      ██║   ██████╔╝██║     
      ╚═╝   ╚═════╝ ╚═╝     
[/bold blue][bright_blue]
     [ TBF GIT MANAGER v1.2.1 ]
[/bright_blue]"""

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def check_git():
    out, _, code = run_cmd("git --version")
    if code != 0:
        console.print("[red]❌ Git не встановлено![/red]")
        console.print("[yellow]Встановіть: apk add git (Alpine) або pkg install git (Termux)[/yellow]")
        return False
    return True

def show_header():
    clear()
    console.print(Align.center(BANNER_TBF))
    console.print(Align.center("[bold cyan]dev>[/bold cyan] [bold white]@TBFPUMBA[/bold white]   [bold cyan]series>[/bold cyan] [bold white]G Edition[/bold white]   [bold cyan]version>[/bold cyan] [bold white]v1.2.1[/bold white]"))
    console.print()

def get_current_branch():
    out, _, code = run_cmd("git rev-parse --abbrev-ref HEAD 2>/dev/null")
    return out if code == 0 else "Не Git репозиторій"

def get_remote():
    out, _, code = run_cmd("git remote -v")
    if code == 0 and out:
        return out.split()[1]
    return None

def git_status():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
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
                table.add_row(parts[0], parts[1])
            else:
                table.add_row("?", line)
        console.print(table)
    input("\n[Натисніть Enter для повернення в меню...]")

def git_quick_commit():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
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
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    branch = get_current_branch()
    if branch == "Не Git репозиторій":
        console.print("[red]❌ Це не Git-репозиторій![/red]")
        input("\n[Натисніть Enter...]")
        return
    remote = get_remote()
    if not remote:
        console.print("[yellow]⚠️ Немає віддаленого репозиторію! Додайте remote (пункт 10).[/yellow]")
        input("\n[Натисніть Enter...]")
        return
    console.print(f"[bold cyan][+] Пуш змін на GitHub (гілка: {branch})...[/bold cyan]")
    out, err, code = run_cmd(f"git push origin {branch}")
    if code == 0:
        console.print(Panel("[bold green]🚀 Зміни успішно відправлені на GitHub![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка при git push:[/bold red]\n{err or out}", border_style="red"))
    input("\n[Натисніть Enter для повернення в меню...]")

def git_log():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
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

def git_init():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    out, err, code = run_cmd("git init")
    if code == 0:
        console.print(Panel("[bold green]🎉 Новий Git-репозиторій успішно ініціалізовано![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка:[/bold red]\n{err}", border_style="red"))
    input("\n[Натисніть Enter для повернення в меню...]")

def git_branches():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    out, _, code = run_cmd("git branch -a")
    if code != 0:
        console.print(Panel("[bold red]❌ Помилка: це не Git-репозиторій![/bold red]", border_style="red"))
    else:
        table = Table(title="🌿 Всі гілки", border_style="cyan", expand=True)
        table.add_column("Гілка", style="bold white")
        for line in out.splitlines():
            if line.strip():
                table.add_row(line.strip())
        console.print(table)
    input("\n[Натисніть Enter для повернення в меню...]")

def git_create_branch():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    name = Prompt.ask("[bold green]🌿 Введіть назву нової гілки[/bold green]")
    out, err, code = run_cmd(f"git checkout -b {name}")
    if code == 0:
        console.print(Panel(f"[bold green]✅ Гілка '{name}' створена та переключено![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Помилка:[/bold red]\n{err}", border_style="red"))
    input("\n[Натисніть Enter для повернення в меню...]")

def git_switch_branch():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    out, _, code = run_cmd("git branch")
    if code != 0 or not out:
        console.print(Panel("[bold yellow]⚠️ Немає гілок або це не Git-репозиторій.[/bold yellow]", border_style="yellow"))
        input("\n[Натисніть Enter...]")
        return
    branches = [b.strip() for b in out.splitlines() if b.strip()]
    console.print("[cyan]📌 Доступні гілки:[/cyan]")
    for i, b in enumerate(branches, 1):
        console.print(f"  {i}. {b}")
    try:
        choice = int(Prompt.ask("[bold green]Виберіть номер гілки[/bold green]")) - 1
        if 0 <= choice < len(branches):
            branch = branches[choice].replace("*", "").strip()
            run_cmd(f"git checkout {branch}")
            console.print(f"[green]✅ Переключено на {branch}[/green]")
        else:
            console.print("[red]❌ Невірний вибір.[/red]")
    except:
        console.print("[red]❌ Введіть число.[/red]")
    input("\n[Натисніть Enter...]")

def git_delete_branch():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    branch = Prompt.ask("[bold red]🗑️ Введіть назву гілки для видалення[/bold red]")
    if Confirm.ask(f"[yellow]Ви впевнені, що хочете видалити гілку '{branch}'?[/yellow]"):
        out, err, code = run_cmd(f"git branch -d {branch}")
        if code == 0:
            console.print(Panel(f"[green]✅ Гілка '{branch}' видалена![/green]", border_style="green"))
        else:
            console.print(Panel(f"[red]❌ Помилка:[/red]\n{err}", border_style="red"))
    else:
        console.print("[yellow]❌ Скасовано.[/yellow]")
    input("\n[Натисніть Enter...]")

def git_remote_add():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    url = Prompt.ask("[bold green]🔗 Введіть URL віддаленого репозиторію[/bold green]")
    out, err, code = run_cmd(f"git remote add origin {url}")
    if code == 0:
        console.print(Panel("[green]✅ Remote додано![/green]", border_style="green"))
    else:
        console.print(Panel(f"[red]❌ Помилка:[/red]\n{err}", border_style="red"))
    input("\n[Натисніть Enter...]")

def git_remote_show():
    show_header()
    if not check_git():
        input("\n[Натисніть Enter...]")
        return
    out, _, code = run_cmd("git remote -v")
    if code != 0 or not out:
        console.print(Panel("[yellow]⚠️ Немає віддалених репозиторіїв.[/yellow]", border_style="yellow"))
    else:
        table = Table(title="🔗 Віддалені репозиторії", border_style="cyan", expand=True)
        table.add_column("Назва", style="bold yellow")
        table.add_column("URL", style="bold white")
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                table.add_row(parts[0], parts[1])
        console.print(table)
    input("\n[Натисніть Enter...]")

def main():
    while True:
        show_header()
        branch = get_current_branch()
        remote = get_remote()
        remote_info = f"[bold green]{remote}[/bold green]" if remote else "[red]❌ Немає remote[/red]"
        info_panel = f"[bold yellow]Гілка:[/bold yellow] [bold green]{branch}[/bold green]  |  [bold yellow]Remote:[/bold yellow] {remote_info}  |  [bold yellow]Шлях:[/bold yellow] [dim]{os.getcwd()}[/dim]"
        console.print(Panel(info_panel, title="📍 Інформація", border_style="cyan"))
        console.print()
        console.print(" [bold cyan]1.[/bold cyan] 📊 Статус репозиторію")
        console.print(" [bold cyan]2.[/bold cyan] ⚡ Швидкий коміт")
        console.print(" [bold cyan]3.[/bold cyan] 🚀 Пуш на GitHub")
        console.print(" [bold cyan]4.[/bold cyan] 📜 Історія комітів")
        console.print(" [bold cyan]5.[/bold cyan] 🎉 Ініціалізувати Git")
        console.print(" [bold cyan]6.[/bold cyan] 🌿 Показати всі гілки")
        console.print(" [bold cyan]7.[/bold cyan] 🌿 Створити гілку")
        console.print(" [bold cyan]8.[/bold cyan] 🔄 Переключити гілку")
        console.print(" [bold cyan]9.[/bold cyan] 🗑️ Видалити гілку")
        console.print(" [bold cyan]10.[/bold cyan] 🔗 Додати remote")
        console.print(" [bold cyan]11.[/bold cyan] 📋 Показати remote")
        console.print(" [bold red]0.[/bold red] ❌ Вихід\n")
        choice = Prompt.ask("Оберіть дію", choices=["1","2","3","4","5","6","7","8","9","10","11","0"], default="1")
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
        elif choice == "6":
            git_branches()
        elif choice == "7":
            git_create_branch()
        elif choice == "8":
            git_switch_branch()
        elif choice == "9":
            git_delete_branch()
        elif choice == "10":
            git_remote_add()
        elif choice == "11":
            git_remote_show()
        elif choice == "0":
            console.print("\n[bold red][!] Вихід з TBF-GitManager.[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
