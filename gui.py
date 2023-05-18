import tkinter as tk
import webbrowser
import analyzer_data
import pandas as pd

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
        tempframe = tk.Frame(master=masterFrame,relief=tk.GROOVE,borderwidth=5)
        tempframe.pack(fill=tk.X)
        labelcontents = str(i+1) + ". " + word
        templabel = tk.Label(master=tempframe, text=labelcontents)
        templabel.pack(side=tk.LEFT)
        templabeltype = tk.Label(master=tempframe, text=types_list[i], font=font_types)
        templabeltype.pack(side=tk.LEFT)
        tempbutton = tk.Button(master=tempframe,text="?",command=make_button_command(word))
        tempbutton.pack(side=tk.RIGHT)

def results_window(parse_wiki: bool, parse_reddit: bool, parse_youtube: bool, word_number: str, topic: str):
    results = tk.Tk()
    results.geometry('600x800')
    results.title('Results')
    wordN = int(word_number.get())
    tpc = topic.get()

    #scrollbar = tk.Scrollbar(results)

    top_frame_results = tk.Frame(results)
    title_win = tk.Label(top_frame_results, text='Results')
    font_titles = ('arial', 20, "bold")
    title_win.configure(font=font_titles)
    title_win.pack()

    parse_frame_results = tk.Frame(results)
    font_header = ('arial',14,"bold")

    wiki_header = tk.Label(parse_frame_results, text="Wikipedia", font=font_header)
    #wiki_label = tk.Label(parse_frame_results, text=generate_results_list_string(generate_dummy_list("Wikipedia", wordN)))
    reddit_header = tk.Label(parse_frame_results, text="Reddit", font=font_header)
    #reddit_label = tk.Label(parse_frame_results, text=generate_results_list_string(generate_dummy_list("Reddit", wordN)))
    youtube_header = tk.Label(parse_frame_results, text="YouTube", font=font_header)
    #youtube_label = tk.Label(parse_frame_results, text=generate_results_list_string(generate_dummy_list("YouTube", wordN)))
    #print("wiki ", parse_wiki.get())
    #print("n ", word_number.get())
    if parse_wiki.get():
        # activate search for wikipedia
        wiki_header.pack()
        #wiki_label.pack()
        wikidf = analyzer_data.top_words_gui_getter(tpc,wordN,0)
        generate_frames(parse_frame_results,
                        wikidf['words'].values.tolist(),
                        wikidf['type'].values.tolist())
    if parse_reddit.get():
        reddit_header.pack()
        #reddit_label.pack()
        redditdf = analyzer_data.top_words_gui_getter(tpc,wordN,1)
        generate_frames(parse_frame_results,
                        redditdf['words'].values.tolist(),
                        redditdf['type'].values.tolist())
    if parse_youtube.get():
        youtube_header.pack()
        #youtube_label.pack()
        youtubedf = analyzer_data.top_words_gui_getter(tpc,wordN,2)
        generate_frames(parse_frame_results,
                        youtubedf['words'].values.tolist(),
                        youtubedf['type'].values.tolist())

    # TODO: clear information get from everyparsing and print it in the app

    top_frame_results.pack()
    parse_frame_results.pack(fill=tk.X)

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