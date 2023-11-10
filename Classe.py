import tkinter as t
from tkinter import ttk
from functools import partial

from Gestion_Stock.Autre import *

#####################################
#                                   #
#              Classes              #
#                                   #
#####################################

class Fen(t.Tk):
    def __init__(self, *args, **kwargs):
        self.page=0

        t.Tk.__init__(self, *args, **kwargs)
        t.Tk.wm_title(self, Nom_projet)

        self.bind('<KeyPress-Escape>', self.keypress_enter)
        self.bind('<KeyPress-Return>', self.keypress_enter)


        self.iconbitmap(Nom_icon)

        container = t.Frame(self)

        container.pack(side="top")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Page1, Page2, Page3, Page4):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[F] = frame

        self.change_page1()
        self.mainloop()

    def keypress_enter(self, key):
        if self.page == 1 and key.keysym == 'Return':
            self.change_page2()
        elif self.page == 1 and key.keysym == 'Escape':
            self.quit()
        elif self.page == 2 and key.keysym == 'Escape':
            self.change_page1()

    def change_page1(self):
        frame = self.frames[Page1]
        frame.ouverture_page()
        frame.tkraise()
        self.page = 1

    def change_page2(self):
        frame = self.frames[Page2]
        if self.page == 1:
            frame2 = self.frames[Page1]
        elif self.page == 3:
            frame2 = self.frames[Page3]
        elif self.page == 4:
            frame2 = self.frames[Page4]
        frame.cestquoi = frame2.var_cestquoi.get()
        frame.param = frame2.var_param.get()
        frame.ouverture_page()
        frame.tkraise()
        self.page = 2

    def change_page3(self):
        frame = self.frames[Page3]
        frame.tkraise()
        self.page = 3

    def change_page4(self):
        frame = self.frames[Page4]
        frame.tkraise()
        frame.ouverture_page()
        self.page = 4

    def quit(self):
        self.destroy()

    def combobox_cestquoi(self, enfant):
        Val_combo = [VAR_NULL]
        f = open(NOM_FILE, 'r')
        for i in f:
            i = i.split(';')
            if len(i) >= 3:
                if i[1] not in Val_combo:
                    Val_combo.append(i[1])
        f.close()
        enfant.c_cestquoi['values'] = Val_combo

    def combobox_param(self, enfant, *args):
        Val_combo = [VAR_NULL]
        f = open(NOM_FILE, 'r')
        for i in f:
            i = i.split(';')
            if i[1] == enfant.var_cestquoi.get() and i[2] not in Val_combo:
                Val_combo.append(i[2])
        f.close()
        enfant.c_param['values'] = Val_combo


class Button(t.Button):
    def __init__(self, *args, **kwargs):
        t.Button.__init__(self, *args, **kwargs)
class Entry(t.Button):
    def __init__(self, *args, **kwargs):
        t.Entry.__init__(self, *args, **kwargs)
class Label(t.Label):
    def __init__(self, *args, **kwargs):
        t.Label.__init__(self, *args, **kwargs)
class Listbox(t.Listbox):
    def __init__(self, *args, **kwargs):
        t.Listbox.__init__(self, *args, **kwargs)
class Checkbutton(t.Checkbutton):
    def __init__(self, *args, **kwargs):
        t.Checkbutton.__init__(self, *args, **kwargs)
        self.onvalue = 1
        self.offvalue = 0
class Combobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        ttk.Combobox.__init__(self, *args, **kwargs)


class Page1(t.Frame):
    def __init__(self, parent, controlleur):
        t.Frame.__init__(self, parent)
        self.controlleur = controlleur

        self.var_cestquoi = t.StringVar()
        self.var_param = t.StringVar()

        self.l_text = Label(self, text='Gestion du stock - Couture')
        self.c_cestquoi = Combobox(self, textvariable=self.var_cestquoi)
        self.c_param = Combobox(self, textvariable=self.var_param)
        self.b_valid = Button(self, text = 'Valider', command=lambda: self.validation())
        self.b_newcoul = Button(self, text = 'Nouvelle Couleur', command=lambda: controlleur.change_page3())
        self.b_invent = Button(self, text = 'Inventaire', command=lambda: controlleur.change_page4())
        self.b_reorg = Button(self, text = "Réogranisation\nde l'inventaire", command=lambda: reorganiser())
        self.b_quit = Button(self, text = 'Quiter', command=lambda: controlleur.quit())

        self.controlleur.combobox_cestquoi(self)
        f = partial(self.controlleur.combobox_param, self)
        self.c_cestquoi.bind('<<ComboboxSelected>>', f)
        self.c_param['values'] = (VAR_NULL)
        self.var_cestquoi.set(VAR_NULL)
        self.var_param.set(VAR_NULL)

        self.l_text.grid(row=0, column=0, columnspan=3)
        self.c_cestquoi.grid(row=1, column=0)
        self.c_param.grid(row=1, column=2)
        self.b_valid.grid(row=2, column=2)
        self.b_newcoul.grid(row=2, column=1)
        self.b_invent.grid(row=2, column=0)
        self.b_reorg.grid(row=2, column=3)
        self.b_quit.grid(row=3, column=4)

    def validation(self):
        if self.var_cestquoi.get() != VAR_NULL and self.var_param.get() != VAR_NULL:
            self.controlleur.change_page2()
    
    def ouverture_page(self):
        self.controlleur.combobox_cestquoi(self)
        self.c_param['values'] = (VAR_NULL)
        self.var_cestquoi.set(VAR_NULL)
        self.var_param.set(VAR_NULL)


class Page2(t.Frame):
    def __init__(self, parent, controlleur):
        t.Frame.__init__(self, parent)
        self.stock = Stock('', '')

        self.var_text = t.StringVar()
        self.var_text.set("")

        self.cestquoi = ""
        self.param = ""
        self.frames = {}

        for nb in range(1, 4): # 1, 2, 3
            frame = FrameStock(self, nb)
            frame.grid(row=1, column=0, sticky='nsew')
            self.frames[nb] = frame

        self.text = Label(self, textvariable=self.var_text)
        self.b = Button(self, text='Reset', command=lambda: self.reset())
        self.b_valid = Button(self, text='Validation', command=lambda: self.validation())
        self.b_quit = Button(self, text='Retour', command=lambda: controlleur.change_page1())
        self.text.grid(row=0, column=0, columnspan=2)
        self.b.grid(row=1, column=1)
        self.b_valid.grid(row=2, column=1)
        self.b_quit.grid(row=3, column=2)

    def ouverture_page(self):
        self.var_text.set(f'Gestion du stock de {self.cestquoi} {self.param}')
        self.stock = Stock(self.cestquoi, self.param)
        self.stock.read_line()
        frame = self.frames[self.stock.nb]
        for i in range(len(self.stock.stock)):
            frame.var[i].set(self.stock.stock[i])
        frame.tkraise()

    def modif_stock(self, i, p):
        if self.stock.nb != 0:
            if self.stock.stock[i]+p >= 0:
                self.stock.stock[i] += p
                self.frames[self.stock.nb].var[i].set(self.stock.stock[i])

    def reset(self):
        for i in range(self.stock.nb):
            self.frames[self.stock.nb].var[i].set(self.stock.stock[i])

    def validation(self):
        for i in range(self.stock.nb):
            self.stock.stock[i] = self.frames[self.stock.nb].var[i].get()
        self.stock.modif_line()


class Page3(t.Frame):
    def __init__(self, parent, controlleur):
        t.Frame.__init__(self, parent)
        self.controlleur = controlleur
        self.stock = Stock('', '')

        self.var_cestquoi = t.StringVar()
        self.var_param = t.StringVar()
        self.var = []
        self.ck = []
        self.var_cestquoi.set("")
        self.var_param.set("")

        for i in range(len(PARAM_STOCK)):
            self.var.append(t.IntVar())
            self.var[i].set(0)
            self.ck.append(Checkbutton(self, text=PARAM_STOCK[i], variable=self.var[i]))
            self.ck[i].grid(row=3, column=i)

        self.lab_prin = Label(self, text="Nouveau Item")
        self.lab_cquoi = Label(self, text="Item : ")
        self.lab_param = Label(self, text="Paramètre : ")
        self.c_cestquoi = Combobox(self, textvariable=self.var_cestquoi)
        self.c_param = Combobox(self, textvariable=self.var_param)
        self.b_valid = Button(self, text="Validation", command=lambda: self.validation(controlleur))
        self.b_quit = Button(self, text="Retour", command=lambda: controlleur.change_page1())
        
        self.lab_prin.grid(row=0, column=0, columnspan=3)
        self.lab_cquoi.grid(row=1, column=0)
        self.c_cestquoi.grid(row=1, column=1)
        self.lab_param.grid(row=2, column=0)
        self.c_param.grid(row=2, column=1)
        self.b_valid.grid(row=4, column=4)
        self.b_quit.grid(row=5, column=5)
        f = partial(self.controlleur.combobox_param, self)
        self.c_cestquoi.bind('<<ComboboxSelected>>', f)
        self.controlleur.combobox_cestquoi(self)

    def ouverture_page(self):
        self.cestquoi.set("")
        self.param.set("")
        for i in self.var:
            i.set(0)

    def validation(self, controlleur):
        nb = self.valid_check()
        if self.var_cestquoi.get() != '' and self.var_param.get() != '' and self.var_cestquoi.get() != VAR_NULL and self.var_param.get() != VAR_NULL and nb != 0:
            self.stock.nom_stock = self.var_cestquoi.get()
            self.stock.param = self.var_param.get()
            self.stock.new_id()
            for i in range(nb):
                self.stock.stock.append(0)
            self.stock.add_line()
            controlleur.change_page2()

    def valid_check(self):
        nb = 0
        for i in self.var:
            if i.get() != 0:
                nb += 1
        return nb


class Page4(t.Frame):
    def __init__(self, parent, controlleur):
        t.Frame.__init__(self, parent)
        self.controlleur = controlleur
        self.stocks = []

        self.var_cestquoi = t.StringVar()
        self.var_param = t.StringVar()
        self.var_cestquoi.set('')
        self.var_param.set('')

        self.l_text = Label(self, text="Inventaire")
        self.list = Listbox(self, width=80, height=20)
        self.list.bind("<<ListboxSelect>>", self.select_stock)
        self.b_quit = Button(self, text='Retour', command=lambda: controlleur.change_page1())

        self.l_text.grid(row=0, column=0)
        self.list.grid(row=1, column=0)
        self.b_quit.grid(row=2, column=1)

    def ouverture_page(self):
        self.list.delete(0,t.END)
        f = open(NOM_FILE, 'r')
        self.stocks = []
        for line in f:
            line = line.split(';')
            stock = []
            for i in range(len(line[3:-1])):
                stock.append(int(line[i+3]))
            s = Stock(line[1], line[2], line[0], stock)
            s.read_line()
            self.stocks.append(s)

        for i in range(len(self.stocks)):
            self.list.insert(i, self.stocks[i].print())
        f.close()

    def select_stock(self, event):
        a = self.list.curselection()
        id = str(a[0])

        f = open(NOM_FILE, 'r')
        line = f.readlines()
        f.close()
        for i in line:
            i = i.split(';')
            if id == i[0]:        
                self.var_cestquoi.set(i[1])
                self.var_param.set(i[2])

        self.controlleur.change_page2()


class FrameStock(t.Frame):
    def __init__(self, parent, nb):
        t.Frame.__init__(self, parent)
        self.var = []
        self.lab = []
        self.ent = []
        self.bom = []
        self.bop = []
        self.nb = nb
        cmd = self.register(lambda s: not s or s.isdigit())

        self.text_lab = []
        if self.nb == 1:
            self.text_lab = [PARAM_STOCK[1]]
        elif self.nb == 2:
            self.text_lab = PARAM_STOCK[:2]
        elif self.nb == 3:
            self.text_lab = PARAM_STOCK
        for i in range(len(self.text_lab)):
            fonction_bouton_m = partial(parent.modif_stock, i, -1)
            fonction_bouton_p = partial(parent.modif_stock, i, 1)

            self.var.append(t.IntVar())
            self.var[i].set(0)
            self.lab.append(Label(self, text=self.text_lab[i]))

            self.ent.append(Entry(self, textvariable=self.var[i], validate="key", vcmd=(cmd, "%P")))
            self.bom.append(Button(self, text='-', command=fonction_bouton_m))
            self.bop.append(Button(self, text='+', command=fonction_bouton_p))

            self.lab[i].grid(row=0, column=(i*2), columnspan=2)
            self.ent[i].grid(row=1, column=(i*2), columnspan=2)
            self.bom[i].grid(row=2, column=(i*2))
            self.bop[i].grid(row=2, column=(i*2)+1)


class Stock():
    def __init__(self, nom_stock="", param="", id="", stock=[]):
        self.id = id
        self.nom_stock = nom_stock
        self.param = param
        self.stock = stock
        self.nb = len(self.stock)

    def read_line(self):
        f = open(NOM_FILE, 'r')
        self.stock = []
        for line in f:
            line = line.split(';')
            if line[1] == self.nom_stock and line[2] == self.param:
                self.id = line[0]
                for i in range(len(line[3:-1])):
                    self.stock.append(int(line[i+3]))
        self.nb = len(self.stock)
        f.close()

    def modif_line(self):
        f = open(NOM_FILE, 'r')
        lines = f.readlines()
        f.close()

        ligne_id = f'{self.id};{self.nom_stock};{self.param};'
        for i in self.stock:
            ligne_id += f'{i};'
        ligne_id += '\n'

        f = open(NOM_FILE, 'w')
        for i in lines:
            if i.split(';')[0] == self.id:
                f.writelines(ligne_id)
            else:
                f.writelines(i)
        f.close()

    def add_line(self):
        f = open(NOM_FILE, 'a')
        line_id = f'{self.id};{self.nom_stock};{self.param};'
        for i in self.stock:
            line_id += f'{i};'
        line_id += '\n'
        f.writelines(line_id)
        f.close()

    def new_id(self):
        nb = 0
        f = open(NOM_FILE, 'r')
        for i in f:
            i = i.split(';')
            if int(i[0]) >= nb:
                nb = int(i[0])+1
        f.close()
        self.id = nb

    def print(self):
        if self.nb == 1:
            val_txt = [PARAM_STOCK[1]]
        elif self.nb == 2:
            val_txt = PARAM_STOCK[:2]
        elif self.nb == 3:
            val_txt = PARAM_STOCK
        t = f'{self.nom_stock} - {self.param} --> '
        for i in range(self.nb):
            t += f'{val_txt[i]} : {self.stock[i]} '
            if i != self.nb-1:
                t += ' -- '
        return t
