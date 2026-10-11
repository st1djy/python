from colorama import init, Fore, Style

init(autoreset=True)
import os
from datetime import datetime

FILE = "tasks.txt"

RED    = Fore.RED
YELLOW = Fore.YELLOW
GREEN  = Fore.GREEN
CYAN   = Fore.CYAN
GRAY   = Fore.LIGHTBLACK_EX
BOLD   = Style.BRIGHT
RESET  = Style.RESET_ALL

DATETIME_FORMAT = "%Y-%m-%d %H:%M"



def load_tasks():
    """Загружает задачи из файла. Возвращает список словарей."""
    tasks = []
    if not os.path.exists(FILE):
        return tasks
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                continue
            tid, desc, dt, done = parts
            try:
                deadline = datetime.strptime(dt, DATETIME_FORMAT)
            except ValueError:
                continue
            tasks.append({
                "id": int(tid),
                "desc": desc,
                "deadline": deadline,
                "done": done == "1",
            })
    return tasks


def save_tasks(tasks):
    """Сохраняет список задач в файл."""
    with open(FILE, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(
                f"{t['id']}|{t['desc']}|"
                f"{t['deadline'].strftime(DATETIME_FORMAT)}|"
                f"{1 if t['done'] else 0}\n"
            )


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1



def categorize(task):
    """Возвращает категорию: 'done', 'overdue', 'today', 'future'."""
    if task["done"]:
        return "done"
    now = datetime.now()
    if task["deadline"] < now:
        return "overdue"
    if task["deadline"].date() == now.date():
        return "today"
    return "future"


def category_color(cat):
    return {
        "done":    GRAY,
        "overdue": RED,
        "today":   YELLOW,
        "future":  GREEN,
    }[cat]


def category_label(cat):
    return {
        "done":    "[ВЫПОЛНЕНО]",
        "overdue": "[ПРОСРОЧЕНО]",
        "today":   "[СЕГОДНЯ]",
        "future":  "[БУДУЩЕЕ]",
    }[cat]




def show_tasks(tasks, show_done=True):
    if not tasks:
        print(f"{CYAN}Список задач пуст.{RESET}")
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t["done"], t["deadline"])
    )

    print(f"\n{BOLD}--- СПИСОК ЗАДАЧ ---{RESET}")
    for t in sorted_tasks:
        cat = categorize(t)
        if cat == "done" and not show_done:
            continue
        color = category_color(cat)
        label = category_label(cat)
        deadline_str = t["deadline"].strftime("%Y-%m-%d %H:%M")
        print(
            f"{color}{t['id']:>3}. {label:<14} "
            f"{deadline_str}  {t['desc']}{RESET}"
        )
    print()



def add_task(tasks):
    desc = input("Описание задачи: ").strip()
    if not desc:
        print(f"{RED}Описание не может быть пустым.{RESET}")
        return
    dt_str = input("Дедлайн (ГГГГ-ММ-ДД ЧЧ:ММ): ").strip()
    try:
        deadline = datetime.strptime(dt_str, DATETIME_FORMAT)
    except ValueError:
        print(f"{RED}Неверный формат даты. Пример: 2025-01-20 18:30{RESET}")
        return
    tasks.append({
        "id": next_id(tasks),
        "desc": desc,
        "deadline": deadline,
        "done": False,
    })
    save_tasks(tasks)
    print(f"{GREEN}Задача добавлена.{RESET}")


def mark_done(tasks):
    show_tasks(tasks, show_done=False)
    try:
        tid = int(input("ID выполненной задачи: ").strip())
    except ValueError:
        print(f"{RED}ID должен быть числом.{RESET}")
        return
    for t in tasks:
        if t["id"] == tid:
            t["done"] = True
            save_tasks(tasks)
            print(f"{GREEN}Задача #{tid} отмечена выполненной.{RESET}")
            return
    print(f"{RED}Задача с ID {tid} не найдена.{RESET}")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        tid = int(input("ID задачи для удаления: ").strip())
    except ValueError:
        print(f"{RED}ID должен быть числом.{RESET}")
        return
    new_tasks = [t for t in tasks if t["id"] != tid]
    if len(new_tasks) == len(tasks):
        print(f"{RED}Задача с ID {tid} не найдена.{RESET}")
    else:
        save_tasks(new_tasks)
        tasks[:] = new_tasks
        print(f"{GREEN}Задача #{tid} удалена.{RESET}")




def main():
    tasks = load_tasks()

    menu = (
        f"\n{BOLD}{CYAN}=== НАПОМИНАЛКА ToDo ==={RESET}\n"
        f"  1. Показать все задачи\n"
        f"  2. Добавить задачу\n"
        f"  3. Отметить задачу выполненной\n"
        f"  4. Удалить задачу\n"
        f"  0. Выход\n"
    )

    while True:
        print(menu)
        choice = input("Выбор: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "0":
            print(f"{CYAN}До встречи!{RESET}")
            break
        else:
            print(f"{RED}Неизвестный пункт меню.{RESET}")


if __name__ == "__main__":
    main()
