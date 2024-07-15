import tkinter as Tk
from tkinter import messagebox
from tkinter import filedialog as fd

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from verifyxpathview.graphs.networkx import DirectedGraph


L, H = 800, 600


donothing = lambda: None
APP_NAME = "VerifyXPathView"


class MainMenu(Tk.Menu):
    
    @classmethod
    def create(cls, wnd):
        menu = cls(wnd.root)
        filemenu = Tk.Menu(menu, tearoff=False)
        filemenu.add_command(label="Open schema...", command=wnd.onmenu_openschema)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=wnd.root.quit)
        menu.add_cascade(label="File", menu=filemenu)

        helpmenu = Tk.Menu(menu, tearoff=False)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menu.add_cascade(label="Help", menu=helpmenu)

        return menu


class MainWindow(object):

    def __init__(self):
        self.root = Tk.Tk()
        self._current_file = None
        self._graph = None

    def onmenu_openschema(self):
        self.current_file = fd.askopenfilename(defaultextension="xsd")

    def onclick_xpathrefresh(self):
        # TODO replace with actual behavior
        messagebox.showinfo("Title", "Doi zece")
        pass
 
    def create_menu(self):
        return MainMenu.create(self)

    def setup_xpath_input(self):
        # Set up XPath query to test
        xpath_input_container = Tk.Frame(self.root)

        xpath_label = Tk.Label(xpath_input_container, text="XPath query:")
        xpath_label.pack(anchor=Tk.W, padx=10, side=Tk.LEFT)

        xpath_textbox = Tk.Entry(xpath_input_container, width=50)
        xpath_textbox.pack(anchor=Tk.W, padx=0, side=Tk.LEFT, expand=True)

        xpath_refresh = Tk.Button(xpath_input_container, text="Refresh", command=self.onclick_xpathrefresh)
        xpath_refresh.pack(anchor=Tk.W, padx=10, side=Tk.LEFT)

        xpath_input_container.pack(anchor=Tk.SW, side=Tk.BOTTOM, expand=True)

    def setup_graph(self):
        if not self.current_file:
            return

        self._graph = DirectedGraph()
        self._graph.add_node(1)
        self._graph.add_node(2)
        self._graph.add_edge(1, 2)
        self.show_graph()

    def show_graph(self):
        figure = Figure(figsize=(5, 5), dpi=200)
        plt1 = figure.add_subplot(111)
        pos = nx.planar_layout(self._graph)
        nx.draw(self._graph, ax=plt1)

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor=Tk.NW, expand=True)

    def setup(self):
        """
        Set up the window.
        """
        self.root.geometry(f"{L}x{H}")
        self.root.title(APP_NAME)
        self.root.config(menu=self.create_menu())

        self.setup_xpath_input()

    def show(self):
        """
        Show the main window.
        """
        self.setup()
        self.root.mainloop()

    @property
    def current_file(self):
        return self._current_file
    
    @current_file.setter
    def current_file(self, new_file):
        self._current_file = new_file
        if self._current_file:
            self.root.title(f"{self.current_file} - {APP_NAME}")
            self.setup_graph()