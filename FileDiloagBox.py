from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import OMR_main
from numpy import array
from functools import partial

g=0
path = " "
###########################################################################
window = Tk()
window.title("Optical Mark Recognize System")


Topframe = Frame(window, height=600, width=600)
Topframe.config(background='gray')
Topframe.pack(side=TOP)


bottomframe = Frame(window)
bottomframe.pack(side=BOTTOM)

#############################################################################
def browserImage():
    global path, panel
    if not path==" ":
        print(path)
        panel.destroy()
    else:
        pass

    path = filedialog.askopenfilename(initialdir=os.getcwd(), title="A select file",
                                      filetype=(("JPG", "*.jpg"), ("JPEG", ".jpeg"), ("png", "*.png")))
    img = Image.open(path)
    img = img.resize((500, 600), Image.ANTIALIAS) #High to Low  for maintain
    img = ImageTk.PhotoImage(img)
    panel = Label(Topframe, image=img)
    panel.image = img
    panel.pack(side=TOP)
    Grade()
##############################################################################
# Answer Question Choice
def create():
    AnswerWindow = Toplevel(window)
    AnswerWindow.title("Answer Window")
    lbl = Label(AnswerWindow, text="Answer Window", font=("Arial", 25))
    lbl.pack(side=TOP)

    lab1 = Label(AnswerWindow, text="Question:")
    lab1.pack()
    global Question, choice
    Question = IntVar()
    QuestionEntry = Entry(AnswerWindow, textvariable=Question)
    QuestionEntry.pack()

    lab2 = Label(AnswerWindow, text="Choice:")
    lab2.pack()

    choice = IntVar()
    choiceEntry = Entry(AnswerWindow, textvariable=choice)
    choiceEntry.pack()

    btn4 = Button(AnswerWindow, text="ENTER ANSWER", command=partial(Answer,AnswerWindow))
    btn4.pack(pady=10)

    AnswerWindow.geometry("300x300")
    AnswerWindow.mainloop()
##############################################################################
# Correct Answer Write Using
def Answer(Answerwindow):
    Answerwindow.destroy()
    AnswerWin = Toplevel(window)
    AnswerWin.title("Give Answer OF Question")
    lbl = Label(AnswerWin, text="Answer Window", font=("Arial", 25))
    lbl.grid(row=1, column=2)
    global q,c
    q = Question.get()
    c = choice.get()

    lbl6 = Label(AnswerWin, text="Enter Choice 0 to "+str(c-1)).place(x=5, y=50)

    global choice1, choice2, choice3, choice4, choice5

    for i in range(q):
        Mylabel = Label(AnswerWin, text="Q " + str(i) + " :").place(x=10, y=50 + (30 * (i + 1)))



    choice1 = IntVar()
    CEntry = Entry(AnswerWin, textvariable=choice1).place(x=60, y=50 + (30 * 1))
    choice2 = IntVar()
    CEntry = Entry(AnswerWin, textvariable=choice2).place(x=60, y=50 + (30 * 2))
    choice3 = IntVar()
    CEntry = Entry(AnswerWin, textvariable=choice3).place(x=60, y=50 + (30 * 3))
    choice4 = IntVar()
    CEntry = Entry(AnswerWin, textvariable=choice4).place(x=60, y=50 + (30 * 4))
    choice5 = IntVar()
    CEntry = Entry(AnswerWin, textvariable=choice5).place(x=60, y=50 + (30 * 5))

    btn6 = Button(AnswerWin, text="Final", command=partial(FinalAnswer,AnswerWin)).place(x=60, y=50 + (30 * 6))
    AnswerWin.geometry("300x400")
    AnswerWin.mainloop()
##############################################################################
# Final Answer Pass Into Tkinter
def FinalAnswer(AnswerWin):
    lb1=Label(AnswerWin, text="!Answer Uploaded Successfully.\n please Click Final Button").place(x=5, y=270)
    global f
    f = array([choice1.get(), choice2.get(), choice3.get(), choice4.get(), choice5.get()])
    global g
    g=1
    pre = 0
    fin = 0
    OMR_main.Process(path, pre, fin,f,q,c)
    Grade()

#All preprocessing Step Show
def PreProcessStepShow():
    pre = 1
    fin = 1
    OMR_main.Process(path, pre, fin,f,q,c)

#Show Final Image Of Pre Processing
def show_FinalImage():
    pre = 0
    fin = 1
    OMR_main.Process(path, pre, fin,f,q,c)

#############################################################################

#############################################################################
def Grade():
    global Grade_Label
    # Grade_Label.destroy()
    if g==1:
        grade = OMR_main.Score()
        print("Final: ")
        print(grade)
        Grade_Label =Label(Topframe, text="Grade Of:"+str(grade)+" %",font='family="Helvetica",size=36,weight="bold"').pack(side=BOTTOM,padx=20)



ID_Num = Label(bottomframe, text="ID_NUMBER :").pack(side=LEFT,pady=10)
IdNumber = IntVar()
CEntry = Entry(bottomframe, textvariable=IdNumber).pack(side=LEFT,pady=10)

btn1 = Button(bottomframe, text="Browse Image", command=browserImage)     #20
btn1.pack(side=LEFT, pady=10)

btn1 = Button(bottomframe, text="Answer", command=lambda: create())
btn1.pack(side=LEFT, pady=10)

btn2 = Button(bottomframe, text="Final Image", command=show_FinalImage)
btn2.pack(side=LEFT, pady=10)

btn3 = Button(bottomframe, text="Pre-Process", command=PreProcessStepShow)
btn3.pack(side=LEFT, pady=10)
############################################################################
window.geometry("650x750")
window.mainloop()