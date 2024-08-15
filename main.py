import os
import tkinter as tk
from tkinter import filedialog, END, ttk, messagebox,font

# Создание главного окна
root = tk.Tk()
root.title("Test Edit") # Изначальное заголовка окна 
root.geometry("980x800")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.option_add("*tearOff", tk.FALSE)


#Сначала установим светлую тему 
current_theme = 'light'

def new_file():
    editor.delete('1.0', END) #Очищает текстовый виджет с помощью 
    root.title('Untitled - Text Editor')
def switch_theme():
    global current_theme
    if current_theme == 'light':
        set_dark_theme()
        current_theme = 'dark'
    else:
        set_light_theme()
        current_theme = 'light'
def set_dark_theme():
    editor.config(bg='black', fg='white', insertbackground='white')
    root.config(bg='black')
    main_menu.config(bg='black', fg='white')
    file_menu.config(bg='black', fg='white')
    edit_menu.config(bg='black', fg='white')
    view_menu.config(bg='black', fg='white')

def set_light_theme():
    editor.config(bg='white', fg='black', insertbackground='black')
    root.config(bg='white')
    main_menu.config(bg='white', fg='black')
    file_menu.config(bg='white', fg='black')
    edit_menu.config(bg='white', fg='black')
    view_menu.config(bg='white', fg='black')

def open_file(*args):
    try:
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                editor.delete('1.0', END)  # Очистить текстовый виджет перед загрузкой нового файла
                editor.insert('1.0', content)
                root.title(os.path.basename(filename)) #Обновить заголовок окна 
    except FileNotFoundError:
        print("Файл не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def save_file(*args): # Добавление *args для поддержки биндинга
    filename = filedialog.asksaveasfilename(defaultextension='.txt',
                                            filetypes=[('Text files', '*.txt'),
                                                       ('All files', '*.*')])
    if filename:
        # Проверить, существует ли файл
        if os.path.exists(filename):
            if not messagebox.askyesno('Подтверждение', 'Файл уже существует. Вы точно хотите заменить его?'):
                return
        try:
            text = editor.get('1.0', tk.END)
            with open(filename, "w") as file:
                file.write(text)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка при сохранении файла: {e}')

def Edit():
    pass
def search_word():
    def perform_search():
        search_term = search_entry.get()
        editor.tag_remove('found', '1.0', END)
        if search_term:
            start_pos = '1.0'
            while True:
                start_pos = editor.search(search_term, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                editor.tag_add('found', start_pos, end_pos)
                start_pos = end_pos
            editor.tag_config('found', foreground='red', background='yellow')
        search_window.destroy()

    search_window = tk.Toplevel(root)
    search_window.title("Search")
    search_window.geometry("300x100")

    tk.Label(search_window, text="Enter word to search:").pack(pady=5)
    search_entry = tk.Entry(search_window, font=("Arial", 12))
    search_entry.pack(pady=5, padx=10, fill='x')

    tk.Button(search_window, text="Search", command=perform_search).pack(pady=5)
# Создание текстового редактора
editor = tk.Text(root, wrap='word', font=('Arial', 11)) #Установка ширфт и размер 
editor.pack(expand=1, fill=tk.BOTH)

# Создание вертикальной полосы прокрутки и привязка ее к текстовому виджету
#ys = ttk.Scrollbar(orient='vertical', command=editor.yview)
#ys.pack(side='right', fill='y')
#editor.config(yscrollcommand=ys.set)

# Создание меню
main_menu = tk.Menu(root)
file_menu = tk.Menu(main_menu, tearoff=0)
edit_menu = tk.Menu(main_menu, tearoff=0)
view_menu = tk.Menu(main_menu, tearoff=0)
settings_menu = tk.Menu(main_menu, tearoff=0)
theme_menu = tk.Menu(main_menu,tearoff=0 )

#File
file_menu.add_command(label='New', command= new_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Open', command=open_file)
#Settings
settings_menu.add_command(label='')
settings_menu.add_command(label='')
#View 
view_menu.add_command(label='Search', command=search_word)

#Опиции для переключения темы
theme_menu.add_command(label='Switch Theme', command=switch_theme)

main_menu.add_cascade(label='File', menu=file_menu)
main_menu.add_cascade(label='Edit')  # Раздел редактирования (пока пустой)
main_menu.add_cascade(label='View', menu=view_menu )  # Раздел просмотра (пока пустой)
#main_menu.add_cascade(label='settings', menu=settings_menu)
main_menu.add_cascade(label='Theme', menu=theme_menu)
root.config(menu=main_menu)
# Привязка комбинации клавиш Ctrl+S к функции сохранения
root.bind('<Control-s>',save_file)
root.bind('<Control-r>',open_file)
#Установим начальную тему
set_light_theme()
root.mainloop()
