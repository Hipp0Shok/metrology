import tkinter as tk
from math import *
from tkinter import filedialog
from tkinter import ttk
import os


def click_browse_button():
    global newFilename
    newFilename = filedialog.askopenfilename(parent=windowRoot, title="Choose file:", initialdir=currentPath,
                                             filetypes=[('TXT Files', '.txt')])
    if os.path.isfile(newFilename):
        path.set(newFilename)


def click_exit_button():
    windowRoot.destroy()


def click_analise_button():
    global significanceLevel
    global table
    significanceLevel = comboGrubbs.current()
    for k in table:
        k.grid_remove()
    table = []
    if os.path.isfile(newFilename):
        fileopened = open(newFilename, mode="r")
        if fileopened:
            dictOutput["data"] = fileopened.readline().replace(",", ".")

            dictOutput["data"] = dictOutput["data"].split()
            dictOutput["data"] = list(map(float, dictOutput["data"]))

            if dictOutput["data"].__len__() >= 15:
                textOutput.config(state=tk.NORMAL)
                textOutput.delete(1.0, tk.END)
                textOutput.insert(tk.END, "There are too many values!")
                textOutput.config(state=tk.DISABLED)
            elif dictOutput["data"].__len__() > 2:
                mean()
                textOutput.config(state=tk.NORMAL)
                textOutput.delete(1.0, tk.END)
                textOutput.insert(tk.INSERT, dictOutput["biasedMean"])
                std()
                textOutput.insert(tk.INSERT, str(dictOutput["biasedSTD"]) + "/n")
                textOutput.insert(tk.INSERT, dictOutput["unbiasedSTD"])
                textOutput.insert(tk.INSERT, dictOutput["meanSTD"])
                rudeerrors()
                borders()
                confidenceborders()
                textOutput.config(state=tk.DISABLED)
                print(dictOutput)
                for i in range(0, dictOutput["data"].__len__()):
                    table.append(tk.Label(tableFrame, width=7, height=1, bg="white", fg="black",
                                             font="arial, 10", text=dictOutput["data"][i], bd=5))
                    table[i].grid(row=i + 1, rowspan=1, column=1, columnspan=1)
            else:
                textOutput.config(state=tk.NORMAL)
                textOutput.delete(1.0, tk.END)
                textOutput.insert(tk.END, "More values are required!")
                textOutput.config(state=tk.DISABLED)
        fileopened.close()
    else:
        textOutput.config(state=tk.NORMAL)
        textOutput.delete(1.0, tk.END)
        textOutput.insert(tk.END, "Please, choose correct file!")
        textOutput.config(state=tk.DISABLED)


def mean():
    global dictOutput
    dictOutput["biasedMean"] = sum(dictOutput["data"])/(dictOutput["data"].__len__())


def std():
    disp = 0
    for i in range(0, dictOutput["data"].__len__()):
        disp += pow(dictOutput["data"][i] - displacedMean, 2)
    dictOutput["unbiasedSTD"] = sqrt(disp/(dictOutput["data"].__len__()-1.5))
    dictOutput["biasedSTD"] = sqrt(disp/(dictOutput["data"].__len__()-1))
    dictOutput["meanSTD"] = dictOutput["unbiasedSTD"]/sqrt(dictOutput["data"].__len__())


def rudeerrors():
    global dictOutput
    Gt = dictGrubbs[dictOutput["data"].__len__()][significanceLevel]
    dictOutput["deletedValues"] = []
    flag = True
    while flag:
        flag = False
        xmax = max(dictOutput["data"])
        G1 = abs(xmax - dictOutput["biasedMean"]) / dictOutput["unbiasedSTD"]
        if G1 > Gt:
            dictOutput["data"].remove(xmax)
            dictOutput["deletedValues"].append(xmax)
            flag = True
    flag = True
    while flag:
        flag = False
        xmin = min(dictOutput["data"])
        G2 = abs(xmin - dictOutput["biasedMean"]) / dictOutput["unbiasedSTD"]
        if G2 > Gt:
            dictOutput["data"].remove(xmin)
            dictOutput["deletedValues"].append(xmin)
            flag = True


def borders():
    global confidenceProbability
    confidenceProbability = comboStudent.current()
    t = dictStudent[dictOutput["data"].__len__()-1][confidenceProbability]
    dictOutput["border"] = dictOutput["meanSTD"]*t


def confidenceborders():
    global NSP
    global tableNSP
    NSP = []
    for i in range(0, 14):
        k = tableNSP[i][1].get()
        if k:
            NSP.append(float(k.replace(",", ".")))
    print(NSP)
    m = NSP.__len__()
    print(m)
    if m > 1:
        if confidenceProbability == 0:
            k = 1.1
        else:
            if m > 4:
                k = 1.4
            else:
                if m > 2:
                    etta1diff = 0
                    etta1ind = 0
                    etta2ind = 0
                    for k in range(0, NSP.__len__()):
                        for j in range(k, NSP.__len__()):
                            diff = abs(NSP[k] - NSP[j])
                            if diff > etta1diff:
                                etta1ind = k
                                etta1diff = diff
                    while etta2ind == etta1ind and etta2ind < NSP.__len__():
                        etta2ind += 1
                    etta2diff = abs(NSP[etta2ind] - NSP[etta1ind])
                    for k in range(0, NSP.__len__()):
                        if k != etta2ind and k != etta1ind:
                            diff = abs(NSP[etta1ind] - NSP[etta2ind])
                            if diff < etta2diff:
                                etta2ind = k
                                etta2diff = diff
                else:
                    etta1ind = NSP.index(max(NSP))
                    if etta1ind == 0:
                        etta2ind = 1
                    else:
                        etta2ind = 0
            l = NSP[etta1ind] / NSP[etta2ind]
            lmax = int(ceil(l))
            lmin = int(floor(l))
            k = (graphK[m][lmax] - graphK[m][lmin]) * (l - lmin) + lmin
        summ = 0
        for n in range(0, NSP.__len__()):
            summ += pow(NSP[n], 2)
        etta = k*sqrt(summ)
        setta = etta / (k*sqrt(3))
    else:
        if m != 0:
            etta = NSP[0]
            setta = etta / sqrt(3)
        else:
            etta = 0
            setta = 0
    dictOutput["etta"] = etta
    ssumm = sqrt(pow(setta, 2)+pow(dictOutput["meanSTD"], 2))
    K = (dictOutput["border"] + etta)/(dictOutput["meanSTD"]+setta)
    dictOutput["delta"] = K*ssumm


if __name__ == '__main__':
    significanceLevel = 0
    confidenceProbability = 0
    dictGrubbs = {
        3: [1.155, 1.155],
        4: [1.496, 1.481],
        5: [1.764, 1.715],
        6: [1.973, 1.887],
        7: [2.139, 2.020],
        8: [2.274, 2.126],
        9: [2.387, 2.215],
        10: [2.482, 2.290],
        11: [2.564, 2.355],
        12: [2.636, 2.412],
        13: [2.699, 2.462],
        14: [2.755, 2.507]
    }
    dictStudent = {
        3: [3.182, 5.841],
        4: [2.776, 4.604],
        5: [2.571, 4.032],
        6: [2.447, 3.707],
        7: [2.365, 2.998],
        8: [2.306, 2.355],
        9: [2.262, 3.250],
        10: [2.228, 3.169],
        11: [2.203, 3.112],
        12: [2.179, 3.055],
        13: [2.162, 3.016],
        14: [2.145, 2.977]
    }
    graphK = {
        2: [0.98, 1.28, 1.22, 1.165, 1.125, 1.09, 1.07, 1.05, 1.04],
        3: [1.275, 1.375, 1.32, 1.245, 1.18, 1.15, 1.12, 1.09, 1.08],
        4: [1.38, 1.41, 1.365, 1.28, 1.24, 1.18, 1.145, 1.13, 1.1]
    }
    dictOutput = {}
    windowRoot = tk.Tk()
    table = []
    tableNSP = []
    NSP = []
    displacedMean = 0
    upperFrame = tk.Frame(windowRoot, bg="white", bd=5)
    downerFrame = tk.Frame(windowRoot, bg="white", bd=5)
    tableFrame = tk.Frame(windowRoot, bg="grey", bd=5)
    buttonExit = tk.Button(downerFrame, text="Exit", width=3, height=1, bg="white", fg="black",
                           font="arial, 10", command=click_exit_button)
    buttonStart = tk.Button(upperFrame, text="Browse...", width=7, height=1, bg="white", fg="black",
                            font="arial, 10", command=click_browse_button)
    buttonAnalise = tk.Button(upperFrame, text="Analise", width=70, height=1, bg="white", fg="black",
                              font="arial, 10", command=click_analise_button)
    buttonDummy = tk.Button(tableFrame, text="Analise", width=5, height=1, bg="white", fg="black", font="arial, 10")
    comboGrubbs = ttk.Combobox(upperFrame, values=[">1%", ">5%"], width=14, height=1)
    comboGrubbs.current(0)
    comboStudent = ttk.Combobox(upperFrame, values=["0,95", "0,99"], width=14, height=1)
    comboStudent.current(0)
    labelGrubbs = tk.Label(upperFrame, text="Уровень значимости", bg="white", font="arial, 10", fg="black")
    labelStudent = tk.Label(upperFrame, text="Доверительная вероятность", bg="white", font="arial, 10", fg="black")
    currentPath = os.getcwd()
    newFilename = currentPath
    path = tk.StringVar()
    labelNumber = tk.Label(tableFrame, width=3, height=1, bg="white", fg="black",
                           font="arial, 10", bd=5, text="№")
    labelNumber.grid(row=0, rowspan=1, column=0, columnspan=1)
    labelData = tk.Label(tableFrame, width=7, height=1, bg="white", fg="black",
                         font="arial, 10", bd=5, text="Значение")
    labelData.grid(row=0, rowspan=1, column=1, columnspan=1)
    for i in range(0, 14):
        label = tk.Label(tableFrame, width=3, height=1, bg="white", fg="black",
                         font="arial, 10", bd=5, text=str(i+1))
        label.grid(row=(i+1), rowspan=1, column=0, columnspan=1)
    labelPath = tk.Label(upperFrame, width=60, height=1, bg="white", fg="black",
                         font="arial, 10", textvariable=path, bd=10)
    textOutput = tk.Text(tableFrame, bg="white", bd=5, font="arial, 10")
    textOutput.config(state=tk.DISABLED)
    path.set("Please, choose file containing less than 15 measurements: ")
    upperFrame.pack()
    tableFrame.pack()
    downerFrame.pack()
    buttonExit.pack()
    buttonStart.grid(row=0, rowspan=1, column=4, columnspan=1)
    buttonAnalise.grid(row=1, rowspan=1, column=0, columnspan=5)
    labelGrubbs.grid(row=0, rowspan=1, column=6, columnspan=1)
    labelStudent.grid(row=0, rowspan=1, column=7, columnspan=1)
    comboGrubbs.grid(row=1, rowspan=1, column=6, columnspan=1)
    comboStudent.grid(row=1, rowspan=1, column=7, columnspan=1)
    textOutput.grid(row=0, rowspan=15, column=2, columnspan=1)
    labelPath.grid(row=0, rowspan=1, column=0, columnspan=1)
    labelNumberNSP = tk.Label(tableFrame, bg="white", bd=5, font="arial, 10", width=1, height=1, text="№")
    labelNumberNSP.grid(row=0, rowspan=1, column=3, columnspan=1)
    labelValueNSP = tk.Label(tableFrame, bg="white", bd=5, font="arial, 10", text="Граница НСП", width=10, height=1)
    labelValueNSP.grid(row=0, rowspan=1, column=4, columnspan=1)
    for i in range(0, 14):
        tableNSP.append([])
        tableNSP[i].append(tk.Label(tableFrame, bg="white", bd=5, font="arial, 10", width=1, height=1, text=i+1))
        tableNSP[i].append(tk.Entry(tableFrame, bg="white", bd=5, font="arial, 10", width=10))
        tableNSP[i][0].grid(row=i+1, rowspan=1, column=3, columnspan=1)
        tableNSP[i][1].grid(row=i+1, rowspan=1, column=4, columnspan=1)
    windowRoot.mainloop()
