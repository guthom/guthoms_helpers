import progressbar

#just a simple wrapper of the beautiful progressbar package..

def ProgressBar(iterator):
    widgets = [
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]

    return progressbar.progressbar(iterator, widgets=widgets)
