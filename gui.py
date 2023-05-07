import tkinter as tk
import webbrowser

def results_window(parse_wiki: bool, parse_reddit: bool, parse_youtube: bool):
    results = tk.Tk()
    results.geometry('600x400')
    results.title('Results')

    top_frame_results = tk.Frame(results)
    title_win = tk.Label(top_frame_results, text='Results')
    font_titles = ('arial', 20, "bold")
    title_win.configure(font=font_titles)
    title_win.pack()

    parse_frame_results = tk.Frame(results)

    #print("wiki ", parse_wiki.get())
    if parse_wiki.get():
        # activate search for wikipedia
        pass
    if parse_reddit.get():
        pass
    if parse_youtube.get():
        pass

    # TODO: clear information get from everyparsing and print it in the app

    parse_frame_results.pack()
    top_frame_results.pack()

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
nEntry = tk.Entry(topFrame, width=5)
topicPromp = tk.Label(topFrame, text="words about (topic)")
topicEntry = tk.Entry(topFrame)
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

confirmButton = tk.Button(dividerFrame, text="Go!", command=lambda: results_window(wiki_button_checkbox, reddit_button_checkbox, youtube_button_checkbox))
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