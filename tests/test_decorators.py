import pytest
from src.decorators import log, my_function


def test_log():
    @log()
    def my_function(x, y):
        return x + y

    result = my_function(5, 12)
    assert result == 17


def test_log_capsys(capsys):
    @log()
    def my_function(x, y, c=2):
        return x * y + c

    result = my_function(2, 4)
    assert result == 10
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


def test_log_error():
    @log()
    def my_function(value):
        if value < 0:
            raise Exception(
                'my_function error: my_function() missing 2 required positional arguments: \'x\' and \'y\', Inputs: args=(), kwargs={}')
        return value ** 0.5

    with pytest.raises(Exception, match="cannot access local variable 'result' where it is not associated with a value"):
        my_function(-4)

