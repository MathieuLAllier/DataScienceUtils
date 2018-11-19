import matplotlib.pyplot as plt


def set_size(w, h, ax=None):
    """ w, h: width, height in inches
    https://stackoverflow.com/a/44971177/6395612 """
    if not ax: ax = plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)


def shap_force_plot(class_index, n_index, explainer, shap_values):
    import shap
    shap.initjs()
    return shap.force_plot(explainer.expected_value[class_index], shap_values[class_index][n_index, :])
