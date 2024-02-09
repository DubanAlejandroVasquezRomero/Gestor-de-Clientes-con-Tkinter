from tkinter import *
import sqlite3

root = Tk()
root.title("Gestor De Tareas")
root.geometry("500x500")

conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        render_todos()
    return _remove

def complete(id):
    def _complete():
        c.execute("SELECT * FROM todo WHERE id = ?", (id,))
        todo = c.fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def render_todos():
    rows = c.execute("SELECT * FROM todo").fetchall()
    for widget in frame.winfo_children():
        widget.destroy()
    for i, row in enumerate(rows):
        id, _, description, completed = row
        color = '#555555' if completed else '#ffffff'
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=lambda id=id: complete(id)())
        l.grid(row=i, column=0, sticky="w")
        btn = Button(frame, text='Eliminar', command=remove(id))
        btn.grid(row=i, column=1)
        if completed:
            l.select()
        else:
            l.deselect()

def addTodo():
    todo = e.get()
    if todo:
        c.execute("INSERT INTO todo (description, completed) VALUES (?, ?)", (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nwse', padx=3)

e.focus()
render_todos()

root.bind('<Return>', lambda event: addTodo())
root.mainloop()
