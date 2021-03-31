import pytest
from royalnet_console.pda import ConsolePDA
from royalnet.engineer import PartialCommand, Sentry, Message


def test_construction():
    pda = ConsolePDA()
    assert pda is not None


@pytest.fixture
def pda():
    return ConsolePDA()


@pytest.fixture
def command():
    @PartialCommand.new(syntax="")
    async def test(*, _sentry: Sentry, _msg: Message, **__):
        """
        Ah, non lo so io!
        """
        await _msg.reply(text=r"test")

    return test


def test_registration(pda: ConsolePDA, command: PartialCommand):
    pda.register_partial(command, ["test"])


@pytest.fixture
def pda_with_command(pda: ConsolePDA, command: PartialCommand):
    pda.register_partial(command, ["test"])
    return pda


@pytest.mark.asyncio
async def test_run(pda_with_command: ConsolePDA, monkeypatch):
    check = False

    def trigger(text):
        assert text == "test"
        nonlocal check
        check = True

    monkeypatch.setattr("click.prompt", lambda *_, **__: "test")
    monkeypatch.setattr("click.echo", trigger)

    await pda_with_command.run(cycles=1)

    assert check is True
