be_verbose: bool = False

def setVerbose(verbose: bool):
    global be_verbose
    be_verbose = verbose
    print(f"setVerbose: {be_verbose}")
