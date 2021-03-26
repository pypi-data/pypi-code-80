# This is the example in the Aesara/doc/tutorial/extending_aesara.txt
import aesara
from aesara.graph.basic import Apply
from aesara.graph.op import Op


class DoubleOp(Op):
    """
    Double each element of a tensor.

    Parameters
    ----------
    x : tensor
        Input tensor

    Returns
    -------
    tensor
        a tensor of the same shape and dtype as the input with all
        values doubled.

    Notes
    -----
    this is a test note

    See Also
    --------
    :class:`~aesara.tensor.elemwise.Elemwise` : You can use this to replace
    this example.  Just execute `x * 2` with x being an Aesara variable.


    .. versionadded:: 0.6
    """

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self))

    def __str__(self):
        return self.__class__.__name__

    def make_node(self, x):
        x = aesara.tensor.as_tensor_variable(x)
        return Apply(self, [x], [x.type()])

    def perform(self, node, inputs, output_storage):
        x = inputs[0]
        z = output_storage[0]
        z[0] = x * 2

    def infer_shape(self, fgraph, node, i0_shapes):
        return i0_shapes

    def grad(self, inputs, output_grads):
        return [output_grads[0] * 2]

    def R_op(self, inputs, eval_points):
        # R_op can receive None as eval_points.
        # That means there is no differentiable path through that input.
        # If this implies that you cannot compute some outputs,
        # return None for those.
        if eval_points[0] is None:
            return eval_points
        return self.grad(inputs, eval_points)
