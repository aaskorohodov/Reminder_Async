import time
from tkinter import *
import threading
import datetime as dt
import tkinter.messagebox as mb


def timer_proc():
    '''Запускается в каждом потоке, обрабатывает обратный отсчет, затем обращается к классам.'''
    current_timer = Timer()

    secs, mins, hrs = current_timer.time_to_wait()
    goal_time = dt.datetime.now() + dt.timedelta(seconds=secs, minutes=mins, hours=hrs)

    while dt.datetime.now() < goal_time:
        time_left = goal_time - dt.datetime.now()
        print(time_left)
        hrs_left, mins_secs = divmod(time_left.seconds, 3600)
        mins_left, secs_left = divmod(mins_secs, 60)

        time_left = dt.time(hrs_left, mins_left, secs_left)

        current_timer.change_time_left(time_left)
        time.sleep(1)
    else:
        current_timer.f_timer.destroy()
        mb.showinfo(f"Таймер {current_timer.current_timer_number}", timer.txt.get())


def threading_creator():
    '''Запускает потоки. Нужна, так как кнопка TkInter желает общаться именно с функцией.'''
    threading.Thread(target=timer_proc).start()


class App_Window:
    def __init__(self):
        self.timer_number = 0  # номер таймера, отображается пользователю
        self.window = Tk()
        self.window.title("Добро пожаловать в приложение!")

        # Надпись
        self.lbl = Label(self.window, text="О чем напомнить?", font=("Arial Bold", 50))
        self.lbl.pack(expand=1, padx=10)

        # Поле ввода для пользователя
        self.txt = Entry(self.window, font=("Arial Bold", 20))
        self.txt.pack(fill=BOTH, pady=15, padx=10, expand=1)

        # Кнопка
        self.btn = Button(self.window, text="Клик!", command=self.clicked, font=("Arial Bold", 20))
        self.btn.pack(pady=15, expand=1)

    def ml(self):
        '''Запуск TkInter. Вынесено в отдельный метод, так как иначе из main нет доступа к переменной timer –
        Если запустить mainloop в __init__, то, видимо, mainloop мешает завершить первую строчку main (timer = ...),
        как следствие переменная timer не сохраняется, доступ к ней из другого класса становится невозможен.'''
        self.window.mainloop()

    def clicked(self):
        '''Случилось нажатие первой кнопки'''

        # забываем старые элементы
        self.lbl.pack_forget()
        self.btn.pack_forget()
        self.txt.pack_forget()

        # Контейнеры для новых элементов
        self.f_top = Frame(self.window)
        self.f_secs = Frame(self.window)
        self.f_mins = Frame(self.window)
        self.f_hrs = Frame(self.window)
        self.f_btn = Frame(self.window)

        # Вторая надпись = Через сколько?
        self.lbl2 = Label(self.f_top, text='Через сколько?', font=("Arial Bold", 50)).pack()

        # Далее поля для секунд, минут и часов
        self.secslbl = Label(self.f_secs, text='Сек:').pack(side=LEFT)
        self.secsinpt = Entry(self.f_secs)
        self.secsinpt.pack(side=LEFT)

        self.minslbl = Label(self.f_mins, text='Мин:').pack(side=LEFT)
        self.minsinpt = Entry(self.f_mins)
        self.minsinpt.pack(side=LEFT)

        self.hrslbl = Label(self.f_hrs, text='Час:').pack(side=LEFT)
        self.hrsinpt = Entry(self.f_hrs)
        self.hrsinpt.pack(side=LEFT)

        # кнопка запуска таймера
        self.btnstart = Button(self.f_btn, text='Старт', command=threading_creator, font=('Arial Bold', 15))
        self.btnstart.pack()

        # упаковка контейнеров
        self.f_top.pack()
        self.f_secs.pack()
        self.f_mins.pack()
        self.f_hrs.pack()
        self.f_btn.pack()


class Timer:
    '''Класс представляет контейнер для окна таймера, в котором бегут циферы. Каждый экземпляр является отдельным
    таймером, запускаемом в своем потоке.'''
    def __init__(self):

        # Контейнер
        self.f_timer = Frame(timer.window)

        # Окно, в котором бежит время
        self.timer_info = Label(self.f_timer, bd=5)
        self.timer_info.pack(side=RIGHT)

        # Забираем номер таймера из предыдущего класса, меняем номер таймера в предыдущем классе на следующий (+1)
        self.current_timer_number = timer.timer_number + 1
        timer.timer_number += 1

        # Окно, в котором указан номер таймера
        self.timer_number_lbl = Label(self.f_timer, text=(f'Таймер {timer.timer_number} '))
        self.timer_number_lbl.pack(side=RIGHT)

        # пакуем контейнер
        self.f_timer.pack()

    def time_to_wait(self):
        secs = int(timer.secsinpt.get())
        mins = int(timer.minsinpt.get())
        hrs = int(timer.hrsinpt.get())
        return secs, mins, hrs

    def change_time_left(self, num):
        '''Метод для изменения оставшегося времени'''
        self.timer_info.configure(text=num)


timer = App_Window()
timer.ml()
