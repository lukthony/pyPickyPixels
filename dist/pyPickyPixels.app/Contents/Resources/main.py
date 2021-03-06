import PySimpleGUI as sg # for GUI library
import cv2               # for getting video resolution
import shutil            # for moving files
import os                # for deleting files
import base64                       # for encoding icon to base64
from urllib.request import urlopen  # for opening online icon file

# v1.0.1

sg.change_look_and_feel('Material2') # Add a touch of color
sg.set_options(icon=base64.b64encode(open(r'pyPickyPixelsIcon.png', 'rb').read()))
 
# Left column, to contain list of files to filter
fileColumn = [  [sg.Listbox(values = [], size = (40,15), k = 'LB', horizontal_scroll=True, enable_events=True)],
                [sg.In(visible = False, enable_events=True, k = 'inputFiles')],
                [sg.FilesBrowse('  Add Files  ', target = (-1,0)), sg.Button('  Empty List  ', k = 'emptyList')] ]

# Right column, to contains settings and run button
optionColumn = [ [sg.Text('Specify a resolution to filter out:')],
                 [sg.Spin([i for i in range(0,10000)], initial_value=1920), sg.Text('Width')],
                 [sg.Spin([i for i in range(0,10000)], initial_value=1080), sg.Text('Height')],
                 [sg.Text('Choose a mode:')],
                 [sg.Radio('Delete', "RADIO1", default = False, k = 'delete', enable_events = True),
                  sg.Radio('Output Folder', "RADIO1", default = True, enable_events = True)],
                 [sg.Text('Specify an output folder: ')],
                 [sg.In(size = (30, 6), enable_events=True, k = 'outputFolder')],
                 [sg.FolderBrowse(target=(-1, 0))],
                 [sg.Column([[sg.Button('  RUN  ', k = 'run', enable_events = True)]], justification='r')] ]

# Layout for the entire window
layout = [[sg.Column(fileColumn),sg.Column(optionColumn)]]

# Create the Window
window = sg.Window('pyPickyPixels', layout, resizable=True, element_justification='center')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window
        break
    elif event == 'emptyList': # if user empties list box(list of files)
            window['LB'].update([])
            LB_vals = []
    elif event == 'inputFiles': # if user adds files (add files button)
            input = values['inputFiles'].split(';') # split the list of inputted files at the semicolon
            newFiles = []
            for i in input: # add filepaths to newFiles list
                newFiles.append(i)
            window.find_element('LB').Update(newFiles) # update the window with listbox values
            LB_vals = newFiles # list for listbox values

    elif event == 'run': # if user hits run button
        listBox = LB_vals
        delete = False # variable for whether delete mode is enabled or disabled
        worked = False # variable for if operation succeeded or failed
        supportedExtensions = ['.webm','.mpg','.mp2','.mpeg','.mpe','.mpv',
                               '.ogg','.mp4','.m4p','.m4v','.m4v','.avi',
                               '.wmv','.mov','.qt','.flv','.swf','.hevc',
                               '.heic']
        
        if listBox:
            for file in listBox:
                fileAndExt = os.path.splitext(file)
                extension = fileAndExt[1].lower()
                if (extension in supportedExtensions):
                    if values['delete'] == True:
                        delete = True # enables delete mode
                        
                    # get video resolution
                    vid = cv2.VideoCapture(file)
                    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    
                    # get target resolution
                    targetWidth = values[0]
                    targetHeight = values[1]
                    
                    # operate on files
                    try:
                        if width == targetWidth and height == targetHeight:
                            if delete: # if delete mode is enable, delete it
                                os.remove(file)
                            else: # otherwise move it to the output folder
                                shutil.move(file, values['outputFolder'])
                        worked = True
                    except:
                        sg.Popup('Error Occurred', keep_on_top=True)
            if worked:
                sg.Popup('Operation succeeded', keep_on_top = True)
                        
    # pprint.pprint(values)
window.close()