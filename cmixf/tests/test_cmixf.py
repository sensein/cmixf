import pytest

from ..parser import CMIXFLexer, CMIXFParser


@pytest.mark.parametrize(
    "text,exception",
    [
        ("12E", True),
        ("12E+", True),
        (".", True),
        ("12", False),
        ("-12", False),
        ("12.1", False),
        ("-.1", False),
        (".1", False),
        ("-12.1", False),
        ("12.1E+1", False),
        ("-12.1E+1", False),
        ("12.1e+1", False),
        ("-12.1e+1", False),
    ],
)
def test_real(text, exception):
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    if exception:
        with pytest.raises((ValueError, RuntimeError)):
            parser.parse(lexer.tokenize(text))
    else:
        assert isinstance(parser.parse(lexer.tokenize(text)), str)


@pytest.mark.parametrize(
    "text",
    [
        "60.s",
        "60.min",
        "24.h",
        "1s^-1",
        "6.283185307179586.rad",
        "1m^2",
        "1m^3",
        "1m/s",
        "1m/s^2",
        "1m^-1",
        "1kg/m^3",
        "1m^3/kg",
        "1A/m^2",
        "1A/m",
        "1cd/m^2",
        "1rad/s",
        "1rad/s^2",
        "1Pa.s",
        "1N.m",
        "1N/m",
        "1W/m^2",
        "1J/K",
        "1J/(kg.K)",
        "1J/kg",
        "1W/(m.K)",
        "1J/m^3",
        "1V/m",
        "1C/m^3",
        "1C/m^2",
        "1F/m",
        "1H/m",
        "1C/kg",
        "1Gy/s",
        "1r/min",
        "1kat/m^3",
        "1USD/h",
        "1EUR/kg",
        "1JPY/USD",
        "1",
        "1mol/m^3",
        "1W/sr",
        "1W/(m^2.sr)",
        "1J/mol",
        "1J/(mol.K)",
        "1nV/Hz^(1/2)",
        "1Mibit/s",
    ],
)
def test_cmixf_examples(text):
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    assert isinstance(parser.parse(lexer.tokenize(text)), str)


@pytest.mark.parametrize(
    "text",
    [
        "1µm",
        "1°C",
        "1Ω",
    ],
)
def test_bids_chars(text):
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    assert isinstance(parser.parse(lexer.tokenize(text)), str)


@pytest.mark.parametrize(
    "text",
    [
        "1µV",
        "1uV",
        "1ms",
        "1kBq",
    ],
)
def test_new_errors(text):
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    assert isinstance(parser.parse(lexer.tokenize(text)), str)
