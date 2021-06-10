#preciso refatorar os labels
from tkinter import Tk

def main():


def criar():
    root = Tk()
    root['bg'] = '#22D3C1'
    root.resizable(False, False)
    root.iconbitmap('icone QA.ico')
    root.title('Corretor de Pauta | Law_In Technologies')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    posx = screen_width / 2 - 661 / 2
    posy = screen_height / 2 - 512 / 2
    root.geometry('%dx%d+%d+%d' % (661, 512, posx, posy))


class Root(Tk):
    def inicia(self):
        Root.mainloop(self)

a = Root()
a.inicia()