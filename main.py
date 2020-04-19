from tkinter import*
import tkinter.messagebox
import csv
from bs4 import BeautifulSoup
import urllib.request
import tkinter.scrolledtext as tkscrolled

links = []
columns = []

def show_results():
    try:
        output.delete(1.0, END)
        urlpage = e1.get()
        page = urllib.request.urlopen(urlpage)
        soup = BeautifulSoup(page, 'html.parser')
        if (var.get() == 1):
            for link in soup.findAll('a', attrs={'href': re.compile("^http://|^https://")}):
                links.append([link.get('href')])
            output.insert(1.0, links)
        elif (var.get() == 2):
            table = soup.find('table')
            results = table.find_all('tr')
            for result in results:
                # find all columns per result
                data = result.find_all('td')
                # check that columns have data
                if len(data) == 0:
                    continue
                i = 0
                while (i < len(data)):
                    columns.append([data[i].getText()])
                    i = i + 1
            output.insert(1.0, columns)
        elif (var.get() == 3):
            output.insert(1.0, soup)
        else:
            output.insert(1.0, "You Must Select an Option !!")

    except:
        output.insert(1.0, "Check Your Web Address Again !!")

#window
root = Tk()
root.title("Web Scrapper")
root.configure(background = "AntiqueWhite1")
root.resizable(width=False, height=False)
root.geometry("480x586")
root.columnconfigure(0, weight=1)

ws = Frame(root)
ws.grid()

#webaddress entry
#label
webadd = Label (root, text="Enter Your Web Address", font = ('arial', 12, 'bold'), bg ="AntiqueWhite1")
webadd.grid(column=0, row=0)


#input
e1 = Entry(root,font = ('arial', 12, 'bold'),bd =3, width=50)
e1.insert(END,"http://www.")
e1.grid(row=1, column=0)

#Options (RadioButtons)
options = Label (root, text="Choose your Desired Scrapper", font = ('arial', 12, 'bold'), bg ="AntiqueWhite1")
options.grid(column=0, row=2)
var = IntVar()
rb1 = Radiobutton(root, text="Links", font = ('arial', 11), bg ="AntiqueWhite1",variable=var, value=1)
rb1.grid(row=3, column=0)
rb2 = Radiobutton(root, text="Tables", font = ('arial', 11), bg ="AntiqueWhite1", variable=var, value=2)
rb2.grid(row=4, column=0)
rb3 = Radiobutton(root, text="Raw HTML", font = ('arial', 11), bg ="AntiqueWhite1", variable=var, value=3)
rb3.grid(row=5, column=0)

#Button
btn = Button(root, text = "GO !!", width=8, height = 1,font = ('arial',12, 'bold'),bd=3, bg ="steel blue", command = show_results).grid(row=6, column = 0, pady =1)

#Output
output = tkscrolled.ScrolledText(root)
output.grid(row=7, column = 0)

def exit():
    exit = tkinter.messagebox.askyesno("Web Scrapper", "Confirm Operation")
    if (exit > 0):
        root.destroy()
        return

def save():
    if (var.get() == 1):
        with open('links.csv', 'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(links)
            output.delete(1.0, END)
            output.insert(1.0, "File Saved Successfully !!")
    elif (var.get() == 2):
        with open('table_data.csv', 'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(columns)
            output.delete(1.0, END)
            output.insert(1.0, "File Saved Successfully !!")
    elif (var.get() == 3):
        with open("raw_html.html", "w") as f:
            f.write(output.get(1.0,END))
            output.insert(1.0, "File Saved Successfully !!")
    else:
        output.insert(1.0, "You Must Select an Option !!")


menubar = Menu(ws)
fileMenu = Menu(menubar, tearoff =0)
menubar.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Save", command = save)
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = exit)

root.config(menu = menubar)
root.mainloop()