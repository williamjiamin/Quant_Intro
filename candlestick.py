from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

def william_edu_candlestick(ax, quotes, width=0.2, colorup='#00FF00', colordown='#FF0000',
                         alpha=1.0, shadowCol='k', ochl=True):

    OFFSET = width / 2.0

    lines = []
    patches = []
    for q in quotes:
        if ochl:
            t, open, close, high, low = q[:5]
        else:
            t, open, high, low, close = q[:5]

        if close >= open:
            color = colorup
            lower = open
            height = close - open
            vline = Line2D(
                xdata=(t, t), ydata=(low, high),
                color=colorup, 
                linewidth=0.5,
                antialiased=True,
                )
        else:
            color = colordown
            lower = close
            height = open - close
            vline = Line2D(
                xdata=(t, t), ydata=(low, high),
                color=colordown, 
                linewidth=0.5,
                antialiased=True,
                )


        rect = Rectangle(
            xy=(t - OFFSET, lower),
            width=width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        rect.set_alpha(alpha)

        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches