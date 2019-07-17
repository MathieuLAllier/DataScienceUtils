import matplotlib.pyplot as plt


def set_size(w, h, ax=None):
    """ w, h: width, height in inches
    https://stackoverflow.com/a/44971177/6395612 """
    if not ax:
        ax = plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)


def smooth(scalars, weight=0.5):
    """ Python TensorBoard Smoothing function """
    last = scalars[0]
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point
        smoothed.append(smoothed_val)
        last = smoothed_val

    return smoothed


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    x = [0.12, 0.15, 0.11, 0.2, 0.1, 0.12, 1.5]
    y = smooth(x, 0.75)
    l = range(len(x))

    plt.plot(l, x)
    plt.plot(l, y)

    plt.show()
