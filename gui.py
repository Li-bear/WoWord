import tkinter as tk
import webbrowser

window = tk.Tk()

topFrame = tk.Frame(window)
dividerFrame = tk.Frame(window)
buttonsFrame = tk.Frame(window)
outputFrame = tk.Frame(window)

nPrompt = tk.Label(topFrame, text="Show me the top (number) ")
nEntry = tk.Entry(topFrame, width=5)
topicPromp = tk.Label(topFrame, text="words about (topic)")
topicEntry = tk.Entry(topFrame)
sourcePromp = tk.Label(topFrame, text="from (source)")

outputLabel = tk.Label(outputFrame,text="1.\t\t\t\n2.\t\t\t\n3.\t\t\t\n4.\t\t\t\n5.\t\t\t\n6.\t\t\t\n7.\t\t\t")

sourceGoogleButton = tk.Button(
    buttonsFrame,
    text="Google Books",
    command=lambda: webbrowser.open("https://books.google.com/")
)
sourceWikipediaButton = tk.Button(
    buttonsFrame,
    text="Wikipedia",
    command=lambda: webbrowser.open("https://www.wikipedia.org/")
)
sourceYouTubeButton = tk.Button(
    buttonsFrame,
    text="YouTube",
    command=lambda: webbrowser.open("https://www.youtube.com/")
)
sourceRedditButton = tk.Button(
    buttonsFrame,
    text="Reddit",
    command=lambda: webbrowser.open("https://www.reddit.com/")
)

confirmButton = tk.Button(dividerFrame, text="Go!")
topFrame.pack(side=tk.TOP)

outputFrame.pack(side=tk.BOTTOM)
dividerFrame.pack(side=tk.BOTTOM,fill=tk.X)
buttonsFrame.pack(side=tk.BOTTOM)

nPrompt.pack(side=tk.LEFT)
nEntry.pack(side=tk.LEFT)

topicPromp.pack(side=tk.LEFT)
topicEntry.pack(side=tk.LEFT)

sourcePromp.pack(side=tk.LEFT)

sourceGoogleButton.pack(side=tk.LEFT)
sourceWikipediaButton.pack(side=tk.LEFT)
sourceYouTubeButton.pack(side=tk.LEFT)
sourceRedditButton.pack(side=tk.LEFT)

confirmButton.pack(side=tk.BOTTOM,fill=tk.X)
outputLabel.pack()

window.mainloop()