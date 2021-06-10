import os
from docx import Document
from tkinter import *
from tkinter.filedialog import askopenfilename as askop
from re import compile, findall, split


class Corretor:
    def __init__(self, local_pauta, local_pafs):
        self.local1 = local_pauta
        self.local2 = local_pafs
        self.ntotal_pafs = 0
        self.ntotal_pauta = 0
        self.list_pafs = []
        self.list_pauta = []
        self.p1 = compile("[0-9]{5}[.][0-9]{6}[/][0-9]{4}[-][0-9]{2}")
        self.p2 = compile("[0-9]{9}")
        self.p3 = compile("[0-9]{2}[.][0-9]{3}[//][0-9]{2}[-][0-9]{1}")
        self.p4 = compile("[0-9]{5}[.][0-9]{6}[//][0-9]{2}[-][0-9]{2}")
        self.p5 = compile("[0-9]{4}[.][0-9]{6}[//][0-9]{4}[-][0-9]{2}")
        self.p6 = compile("[0-9]{4}[.][0-9]{12}[-][0-9]{2}")
        self.p7 = compile("[0-9]{2}[.][0-9]{4}[.][0-9]{4}[.][0-9]{6}[-][0-9]{1}")
        self.list_pdr = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7]
        self.listmatched = []
        self.n_matched = 0

    def pafs(self):  # ler
        with open(self.local2, 'r') as read:
            for line in read:
                pro_read = line[:-1]
                self.list_pafs.append(pro_read)
                self.ntotal_pafs = self.ntotal_pafs + 1

    def pauta(self):  # procura na pauta
        doc = Document(self.local1)
        for line in doc.paragraphs:
            procs = line.text
            for pattern in self.list_pdr:
                find = findall(pattern, procs)
                if find:  # OBS2
                    self.list_pauta.append(find[0])
                    self.ntotal_pauta = self.ntotal_pauta + 1

    def match(self):
        ties1 = self.list_pafs
        ties2 = self.list_pauta
        for proces in ties1:
            result = search_bin(ties2, proces)
            if result is not None:
                self.listmatched.append(result)
                print("Há atualização do processo:", proces)
                # Printa os processos lá na listbox, posso fazer o match lá!?
                self.n_matched = self.n_matched + 1
        return True


def quicksort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista) - 1
    if inicio < fim:
        p = partition(lista, inicio, fim)
        quicksort(lista, inicio, p - 1)
        quicksort(lista, p + 1, fim)
    return lista


def partition(lista, inicio, fim):
    pivot = lista[fim]
    i = inicio
    for j in range(inicio, fim):
        if lista[j] <= pivot:
            lista[j], lista[i] = lista[i], lista[j]
            i = i + 1
    lista[i], lista[fim] = lista[fim], lista[i]
    return i


def search_bin(lista, elemento, min=0, max=None):
    if max is None:
        max = len(lista) - 1
    if max < min:
        return None
    else:
        meio = min + (max - min) // 2
    if lista[meio] > elemento:
        return search_bin(lista, elemento, min, meio - 1)
    elif lista[meio] < elemento:
        return search_bin(lista, elemento, meio + 1, max)
    else:
        return lista[meio]


class DialogBox:
    def __init__(self):
        self.pathPauta = None
        self.pathPAFs = None

    def openBox(self, docum=True):
        if docum:
            self.pathPauta = askop(title='Selecione a Pauta',
                                   filetypes=[('Word', '.docx')])
            pathDir1 = self.path(self.pathPauta)
            self.newLabel(pathDir1, 340, 125)
        else:
            self.pathPAFs = askop(title='Selecione os PAFs',
                                  filetypes=[('Bloco de Notas', '.txt')])
            pathDir2 = self.path(self.pathPAFs)
            self.newLabel(pathDir2, 340, 198)

    def path(self, path):
        p = os.path.normpath(path)
        dirsplit = split(r'[\\]+', p)
        pathdir = dirsplit[-2] + "\\" + dirsplit[-1]

        return pathdir

    def newLabel(self, title, x_is, y_is):
        Label(text=title,
              font='Arial 8',
              fg='gray',
              anchor=W).place(x=x_is, y=y_is, width=207, height=24)


root = Tk()
root.title('Corretor de Pauta | Law_In Technologies')
w = 661
h = 512
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
posx = screen_width / 2 - w / 2
posy = screen_height / 2 - h / 2
root.geometry('%dx%d+%d+%d' % (w, h, posx, posy))
root['bg'] = '#23D3C1'
root.resizable(False, False)
root.iconbitmap('icone QA.ico')

Label(text='Processo(s) Encontrado(s):',
      bg='#22D3C1',
      font='Arial 12 bold',
      fg='black').place(x=85, y=65)

Label(root, relief='flat').place(x=85, y=94, width=239, height=373)

Label(text='Pauta:',
      bg='#22D3C1',
      font='Arial 12 bold',
      fg='black').place(x=340, y=94)

Label(text='Escolha a pauta',
      font='Arial 8',
      fg='gray',
      anchor=W).place(x=340, y=125, width=207, height=24)


alexandre = DialogBox()

lupa = PhotoImage(file='Lupa.png')
botaolupa1 = Button(image=lupa,
                    bg='#24AA91',
                    relief='flat',
                    command=lambda: alexandre.openBox(True)).place(x=547, y=125, width=32, height=24)
Label(text='PAFs:',
      bg='#22D3C1',
      font='Arial 12 bold',
      fg='black').place(x=340, y=165)

Label(text='Selecione arquivo com os PAFs',
      font='Arial 8',
      fg='gray',
      anchor=W).place(x=340, y=198, width=207, height=24)

botaolupa2 = Button(image=lupa,
                    bg='#24AA91',
                    relief='flat',
                    command=lambda: alexandre.openBox(False)).place(x=547, y=198, width=32, height=24)


def execute():
    gabriel = Corretor(alexandre.pathPauta, alexandre.pathPAFs)
    gabriel.pafs()
    gabriel.pauta()
    quicksort(gabriel.list_pafs)
    quicksort(gabriel.list_pauta)
    gabriel.match()
    lista = Listbox(root,
                    selectmode=EXTENDED,
                    relief='flat',
                    font='Times 10')
    lista.place(x=85, y=94, width=239, height=373)
    if not gabriel.listmatched:
        lista.insert(END, "Não há atualizações.")
    else:
        lista.insert(END, 'Há atualização(ões) do(s) processo(s):')
        for procs_att in gabriel.listmatched:
            lista.insert(END, procs_att)
        lista.insert(END, '\n')
        lista.insert(END, 'Total de processos atualizados: ' + str(gabriel.n_matched))
        lista.insert(END, 'Total de processos na PAF: ' + str(gabriel.ntotal_pafs))
        lista.insert(END, 'Total de processos na pauta: ' + str(gabriel.ntotal_pauta))


botaopesq = Button(text='Pesquisar',
                   font='Arial 12 bold',
                   fg='white',
                   bg='black',
                   relief='flat',
                   command=execute).place(x=409, y=239, width=101, height=25)


logo = PhotoImage(file='Logo QA.png')
Label(image=logo,
      bg='#23D3C1').place(x=324, y=368)

root.mainloop()
