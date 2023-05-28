import tkinter as tk
from tkinter import ttk
import webbrowser
import analyzer_data
import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def generate_dummy_list(word, length):
    rlist = [word]
    dummy_words = ["is","the","best","source","you","can","use","as"]
    for i in range(length-1):
        rlist.append(dummy_words[i%len(dummy_words)])
    return rlist

def generate_results_list_string(words_list):
    rstr = ""
    for i, word in enumerate(words_list):
        rstr += str(i+1) + ". " + word + "\n"
    return rstr

def generate_frames(masterFrame, words_list, types_list):
    def make_button_command(w):
        return lambda: webbrowser.open("https://en.wiktionary.org/wiki/" + w)
    font_types = ('arial', 9, "italic")

    for i, word in enumerate(words_list):
        tempframe = ttk.Frame(master=masterFrame,relief=tk.GROOVE,borderwidth=5)
        tempframe.pack(fill=tk.X)
        labelcontents = str(i+1) + ". " + word
        templabel = ttk.Label(master=tempframe, text=labelcontents)
        templabel.pack(side=tk.LEFT)
        templabeltype = tk.Label(master=tempframe, text=types_list[i], font=font_types)
        templabeltype.pack(side=tk.LEFT)
        tempbutton = ttk.Button(master=tempframe,text="?",command=make_button_command(word))
        tempbutton.pack(side=tk.RIGHT)

def gen_dummy_figure():
    fig = Figure(figsize=(5,4),dpi=100)
    t = np.arange(0,3,0.01)
    ax = fig.add_subplot()
    line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
    ax.set_xlabel("time [s]")
    ax.set_ylabel("f(t)")

    return fig


def graphs_window(figure1, figure2):
    graphs_win = tk.Tk()
    graphs_win.geometry('600x600')
    graphs_win.title('Graphs')

    graphics = tk.Frame(graphs_win)
    canvas1 = FigureCanvasTkAgg(figure1, master=graphics)
    canvas2 = FigureCanvasTkAgg(figure2, master=graphics)
    canvas1.draw()
    canvas2.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    graphics.pack()

def results_window(parse_wiki: bool, parse_reddit: bool, parse_youtube: bool, word_number: str, topic: str):
    results = tk.Tk()
    results.geometry('800x300')
    results.title('Results')
    wordN = int(word_number.get())
    tpc = topic.get()

    #scrollbar = tk.Scrollbar(results)

    cont = ttk.Frame(results)
    canv = tk.Canvas(cont)

    top_frame_results = tk.Frame(results)
    title_win = tk.Label(top_frame_results, text='Results')
    graphs_button = tk.Button(master=top_frame_results, text="See graphs",command=lambda: graphs_window(gen_dummy_figure(),gen_dummy_figure()))
    export_button = tk.Button(master=top_frame_results, text="Export")
    font_titles = ('arial', 20, "bold")
    title_win.configure(font=font_titles)
    export_button.pack(side=tk.LEFT, fill=tk.X)
    graphs_button.pack(side=tk.RIGHT, fill=tk.X)
    title_win.pack(side=tk.TOP,fill=tk.X)


    parse_frame_results = ttk.Frame(canv)
    scrollbar = ttk.Scrollbar(cont, orient="vertical", command=canv.yview)

    parse_frame_results.bind(
        "<Configure>",
        lambda e: canv.configure(
            scrollregion=canv.bbox("all")
        )
    )

    canv.create_window((0, 0), window=parse_frame_results, anchor=tk.NW, width=780)

    canv.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    font_header = ('arial',14,"bold")

    wiki_header = tk.Label(parse_frame_results, text="Wikipedia", font=font_header)
    reddit_header = tk.Label(parse_frame_results, text="Reddit", font=font_header)
    youtube_header = tk.Label(parse_frame_results, text="YouTube", font=font_header)
    if parse_wiki.get():
        wiki_header.pack()
        wikidf = analyzer_data.top_words_gui_getter(tpc,wordN,0)
        generate_frames(parse_frame_results,
                        wikidf['words'].values.tolist(),
                        wikidf['type'].values.tolist())
    if parse_reddit.get():
        reddit_header.pack()
        redditdf = analyzer_data.top_words_gui_getter(tpc,wordN,1)
        generate_frames(parse_frame_results,
                        redditdf['words'].values.tolist(),
                        redditdf['type'].values.tolist())
    if parse_youtube.get():
        youtube_header.pack()
        youtubedf = analyzer_data.top_words_gui_getter(tpc,wordN,2)
        generate_frames(parse_frame_results,
                        youtubedf['words'].values.tolist(),
                        youtubedf['type'].values.tolist())

    top_frame_results.pack(fill=tk.X)
    cont.pack(fill=tk.BOTH)
    canv.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #parse_frame_results.pack(fill=tk.X)
    scrollbar.pack(side=tk.LEFT,fill=tk.Y)

    results.mainloop()

window = tk.Tk()

window.geometry('600x400')
font_titles = ('arial', 20, "bold")
window.title('Menu')

topFrame = tk.Frame(window)
dividerFrame = tk.Frame(window)
buttonsFrame = tk.Frame(window)
outputFrame = tk.Frame(window)

name_app = tk.Label(topFrame, text='WoWord')
name_app.configure(font=font_titles)
name_app.pack()

nPrompt = tk.Label(topFrame, text="Show me the top (number) ")
nEntryVariable = tk.StringVar()
nEntry = tk.Entry(topFrame, width=5, textvariable=nEntryVariable)
topicPromp = tk.Label(topFrame, text="words about (topic)")
topicEntryVariable = tk.StringVar()
topicEntry = tk.Entry(topFrame, width = 10, textvariable=topicEntryVariable)
sourcePromp = tk.Label(topFrame, text="from (source)")

sources_label = tk.Label(buttonsFrame, text="Choose from whcih sources you want to get information", font='arial', justify='left', anchor="e")
sources_label.pack()

# wikipedia
wiki_button_checkbox = tk.IntVar()
wk_checkbox = tk.Checkbutton(buttonsFrame, text="Wikipedia", variable=wiki_button_checkbox)
wk_checkbox.pack()

# reddit
reddit_button_checkbox = tk.IntVar()
reddit_checkbox = tk.Checkbutton(buttonsFrame, text="Reddit", variable=reddit_button_checkbox)
reddit_checkbox.pack()

# youtube
youtube_button_checkbox = tk.IntVar()
yt_checkbox = tk.Checkbutton(buttonsFrame, text="Youtube", variable=youtube_button_checkbox, justify='left')
yt_checkbox.pack()

confirmButton = tk.Button(dividerFrame, text="Go!", command=lambda:
                          results_window(wiki_button_checkbox, reddit_button_checkbox, youtube_button_checkbox, nEntryVariable, topicEntryVariable))
topFrame.pack(side=tk.TOP)

outputFrame.pack(side=tk.BOTTOM)
dividerFrame.pack(side=tk.BOTTOM,fill=tk.X)
buttonsFrame.pack(pady=20)

nPrompt.pack(side=tk.LEFT)
nEntry.pack(side=tk.LEFT)

topicPromp.pack(side=tk.LEFT)
topicEntry.pack(side=tk.LEFT)

sourcePromp.pack(side=tk.LEFT)

confirmButton.pack(side=tk.BOTTOM,fill=tk.X, padx=30, pady=30)
#outputLabel.pack()

window.mainloop()