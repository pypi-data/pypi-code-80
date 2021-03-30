import io
from lyncs_cppyy import cppdef, make_shared, gbl
from lyncs_utils import redirect_stdout


def test_make_shared():
    cppdef(
        """
    struct Foo {
    ~Foo() { printf("Foo deleted"); }
    };
    Foo * create_foo() { return new Foo(); }
    """
    )

    fp = io.StringIO()
    with redirect_stdout(fp):
        gbl.Foo()
    assert fp.getvalue() == "Foo deleted"

    fp = io.StringIO()
    with redirect_stdout(fp):
        make_shared(gbl.create_foo())
    assert fp.getvalue() == "Foo deleted"
