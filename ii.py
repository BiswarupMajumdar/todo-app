import PySimpleGUI as sg

label1 = sg.Text("Select Files to compress : ")
input1 = sg.Input()
choose_button1 = sg.FilesBrowse("Choose")

label2 = sg.Text("Select Files to compress : ")
input2 = sg.Input()
choose_button2 = sg.FilesBrowse("Choose")


window = sg.Window("File Compressor : ",
                   layout=[[label1, input1, choose_button1],
                           [label2, input2, choose_button2]])

window.read()
window.close()