import csv # 1 (import csv for reading csv file)
import tkinter # 3 (import toolkit for section 3)
from tkinter.filedialog import askopenfilename


# 1. creating and reading CSV file 
from collections import namedtuple
Task = namedtuple("Task", ["title", "duration", "prerequisites"])

def read_tasks(filename):
    tasks = {}
    for row in csv.reader(open(filename)):
        number = int(row[0])
        title = row[1]
        duration = float(row[2])
        prerequisites = set(map(int, row[3].split()))
        tasks[number] = Task(title, duration, prerequisites)
    return tasks


# 2. ordering the tasks
def order_tasks(tasks):
    incomplete = set(tasks)
    completed = set()
    start_days = {}
    while incomplete:
        for task_number in incomplete:
            task = tasks[task_number]
            if task.prerequisites.issubset(completed):
                earliest_start_day = 0
                for prereq_number in task.prerequisites:
                    prereq_end_day = start_days[prereq_number] + tasks[prereq_number].duration
                    if prereq_end_day > earliest_start_day:
                        earliest_start_day = prereq_end_day
                start_days[task_number] = earliest_start_day
                incomplete.remove(task_number)
                completed.add(task_number)
                break
    return start_days

# 3 drawing the chart
def draw_chart(tasks, canvas, row_height=40, title_width=300, line_height =40, day_width=20, bar_height=20, title_indent=20, font_size=-16):
    height = canvas["height"]
    width = canvas["width"]
    week_width = 5 * day_width
    canvas.create_line(0, row_height, width, line_height, fill="grey")
    for week_number in range(5):
        x = title_width + week_number * week_width
        canvas.create_line(x, 0, x, height, fill="grey")
        canvas.create_text(x + week_width / 2, row_height / 2, text=f"Week {week_number+1}", font=("Helvetica", font_size, "bold"))
        start_days = order_tasks(tasks)
        y = row_height
        for task_number in start_days:
                task = tasks[task_number]
                canvas.create_text(title_indent, y + row_height / 2, text=task.title, anchor=tkinter.W, \
                                   font=("Helvetica", font_size))
                bar_x = title_width + start_days[task_number] * day_width
                bar_y = y + (row_height - bar_height) / 2
                bar_width = task.duration * day_width
                canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, fill="red")
                y += row_height

def open_project():
    filename = askopenfilename(title="Open Project", initialdir=".", filetypes=[("CSV Document", "*.csv")])
    tasks = read_tasks(filename)
    draw_chart(tasks, canvas)
    filename_label.config(text=filename) # add filename label to chart

# 3. drawing the chart
root = tkinter.Tk()
root.title("Project Planner")
root.resizable(width=False, height=False) # prevents being able to resize window
button_frame = tkinter.Frame(root, padx=5, pady=5) # sets Open Project button to top left 
button_frame.pack(side="top", fill="x") # sets Open Project button to top left 
open_button = tkinter.Button(root, text="Open project...", command=open_project) # (button_frame impacts open project button position)
filename_label = tkinter.Label(button_frame) # add filename label to chart
filename_label.pack(side="right") # add filename label to chart 
open_button.pack(side="top") # puts open button to left, can replace left with top
canvas = tkinter.Canvas(root, width=800, height=400, bg="white")
canvas.pack(side="bottom")
tkinter.mainloop()