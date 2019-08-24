from IPython.display import Markdown, Code
import matplotlib.pyplot as plt
import numpy as np

def read_md(filename):
    # parse markdown as sections
    with open(filename) as f:
        lines = f.readlines()
    sections = {}
    for l in lines:
        if l.startswith('##'):
            sect_key = l.replace('##', '').strip().lower().replace(' ', '-')
            sections[sect_key] = ''
            continue
        sections[sect_key] += l
    return sections

def md(filename):
    if '#' in filename:
        filename, sect_key = filename.split('#')
        sections = read_md(filename)
        txt = sections[sect_key]
    else:
        with open(filename) as f:
            txt = f.read()
    return Markdown(txt)

def py(filename):
    with open(filename) as f:
        txt = f.read()
        display(Code(txt, language='python'))
        exec(txt)


def imshow(im):
    plt.imshow(im)
    plt.axis('off')
    plt.show()

def imshow_grid(ims, ncol):
    nrow = np.ceil(len(ims) / ncol)
    fig = plt.figure(figsize=(ncol * 6, nrow * 4), dpi= 80, facecolor='w', edgecolor='k')
    for i, im in enumerate(ims):
        ax = fig.add_subplot(nrow, ncol, i+1)
        ax.axis('off')
        ax.imshow(im)
    # fig.tight_layout()
    fig.show()