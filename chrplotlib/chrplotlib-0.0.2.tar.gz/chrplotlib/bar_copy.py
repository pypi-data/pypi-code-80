import numpy as np


def tidy_label(label):
    return ['{:2}'.format(str(i)[:2]) for i in label]


def bar_generate_canvas(y):
    height, length = int(max(y)) + 1, y.shape[0]
    canvas = [[0] * height for _ in range(length)]
    for i, j in enumerate(y):
        j = j * 10
        int_part, frac_part = int(j // 10), int(j % 10)
        k = -1
        for k in range(int_part):
            canvas[i][k] = 10
        canvas[i][k + 1] = frac_part
    return canvas


def bar_change_direction(canvas):
    canvas = [i[::-1] for i in canvas]
    return canvas


def bar_add_segment(canvas):
    canvas_c = list()
    height = len(canvas[0])
    for i in canvas:
        canvas_c.append(i)
        canvas_c.append(i)
        canvas_c.append([0] * height)

    return canvas_c


def bar_rotate(canvas):
    return list(zip(*canvas))


def bar(x=None, y=None):
    x = x or [''] * len(y)
    mark = ' ▂▃▃▄▅▅▆▇▇█'
    canvas = bar_generate_canvas(y)
    canvas = bar_change_direction(canvas)
    canvas = bar_add_segment(canvas)
    canvas = bar_rotate(canvas)

    res = '\n'.join([''.join([mark[col] for col in row]) for row in canvas])
    res = res + '\n' + ' '.join(tidy_label(label=x)) if x else res
    return res


def barh(x=None, y=None):
    x = x or [''] * len(y)
    mark = ['  ', '▎ ', '▍ ', '▌ ', '▋ ', '█ ', '█▎', '█▍', '█▌', '█▌', '██']
    canvas = bar_generate_canvas(y)
    label = tidy_label(x)
    res = '\n'.join([''.join([label[idx_row]] + [mark[col] for col in row]) for idx_row, row in enumerate(canvas)])
    return res


if __name__ == '__main__':
    data = 10 * np.random.rand(20)
    print(bar(y=data))
    print(bar(x=range(20), y=data))
    print(barh(y=data))
    print(barh(x=range(20), y=data))
