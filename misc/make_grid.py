# Load a list of image files and make a grid image
col = 4
with open('list.txt') as f:
    filenames = f.readlines()


def imshow_grid(ims, ncol):
    nrow = np.ceil(len(ims) / ncol)
    fig = plt.figure(figsize=(ncol * 6, nrow * 4), dpi= 80, facecolor='w', edgecolor='k')
    for i, im in enumerate(ims):
        ax = fig.add_subplot(nrow, ncol, i+1)
        ax.axis('off')
        ax.imshow(im)
    # fig.tight_layout()
    # fig.show()
    fig.savefig('grid.png')
