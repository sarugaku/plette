import pytest

from plette.models import Script


def test_parse():
    script = Script(['python', '-c', "print('hello')"])
    assert script.command == 'python'
    assert script.args == ['-c', "print('hello')"], script


def test_parse_error():
    with pytest.raises(IndexError):
        Script('')

def test_cmdify():
    script = Script(['python', '-c', "print('hello world')"])
    cmd = script.cmdify()
    assert cmd == 'python -c "print(\'hello world\')"', script


def test_cmdify_extend():
    script = Script(['python', '-c', "print('hello world')"])
    cmd = script.cmdify(['--verbose'])
    assert cmd == 'python -c "print(\'hello world\')" --verbose'


def test_cmdify_complex():
    script = Script(' '.join([
        '"C:\\Program Files\\Python36\\python.exe" -c',
        """ "print(\'Double quote: \\\"\')" """.strip(),
    ]))
    assert script.cmdify() == ' '.join([
        '"C:\\Program Files\\Python36\\python.exe"',
        '-c',
        """ "print(\'Double quote: \\\"\')" """.strip(),
    ]), script
