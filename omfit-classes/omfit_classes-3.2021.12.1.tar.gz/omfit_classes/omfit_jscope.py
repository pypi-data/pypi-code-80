try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

from omfit_classes.omfit_ascii import OMFITascii

__all__ = ['OMFITjscope']


class OMFITjscope(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface with jScope save files

    :param filename: filename passed to OMFITascii class

    :param \**kw: keyword dictionary passed to OMFITascii class
    """

    def __init__(self, filename, **kw):
        SortedDict.__init__(self)
        OMFITascii.__init__(self, filename, **kw)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        with open(self.filename, 'r') as f:
            lines = f.read().split('\n')
        for line in lines:
            if not len(line.strip()):
                continue
            elif line.startswith('Scope.'):
                key, value = line.split(':', 1)
                value = value.strip()
                if value == 'false':
                    value = False
                elif value == 'true':
                    value = True
                else:
                    try:
                        value = ast.literal_eval(value.strip())
                    except (SyntaxError, ValueError):
                        pass
                    except Exception:
                        print(line, value)
                        raise
                h = self
                for item in key.split('.')[1:-1]:
                    h = h.setdefault(item, {})
                h[key.split('.')[-1]] = value

    def treename(self, signal):
        if ':' not in signal:
            return self['global_1_1']['experiment']
        else:
            treename = signal.split(':')[0].strip('\\')
            if treename == 'pcs.dv':  # for NSTX
                treename = 'eng_test'
            return treename

    def plot(self, shot=None):
        '''
        Plot signals

        :param shot: shot number

        :return: dictionary with all axes indexed by a tuple indicating the row and column
        '''
        from matplotlib.pyplot import subplot
        from omfit_classes.omfit_mds import OMFITmdsValue

        axs = {}
        rows = {}
        cols = []
        for item in self:
            if not item.startswith('plot_'):
                continue
            r, c = map(int, item.split('_')[1:])
            rows[c] = r
            cols.append(c)
        cols = max(cols)
        ax = None
        if shot is None:
            print()
        for item in self:
            if not item.startswith('plot_'):
                continue
            r, c = map(int, item.split('_')[1:])
            axs[r, c] = ax = subplot(rows[c], cols, cols * (r - 1) + c, sharex=ax)
            ax.set_title(self[item]['title'], y=0.5)
            treename = self.treename(self[item]['y_expr_1'])
            if shot is not None:
                y = OMFITmdsValue(self['data_server_argument'], treename, shot, self[item]['y_expr_1'])
                if y.check():
                    if 'x_expr_1' in self[item]:
                        treename = self.treename(self[item]['x_expr_1'])
                        x = OMFITmdsValue(self['data_server_argument'], treename, shot, self[item]['x_expr_1']).data()
                    else:
                        x = y.dim_of(0)
                    if y.check():
                        ax.plot(x, y.data())
            if self[item]['x_log']:
                ax.set_xscale('log')
            if self[item]['y_log']:
                ax.set_yscale('log')
        if shot is None:
            printw('Please specify shot number')
        return axs
