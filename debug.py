debug = False

def aff (text):
    
    global debug
    
    if debug:
        print (text)


def start():
    
    global debug
    
    debug = True
    
    
def stop():
    
    global debug
    
    debug = False
