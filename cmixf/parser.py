import click
from sly import Lexer, Parser

decimal_multiple_prefix = ['E', 'G', 'M', 'P', 'T', 'Y', 'Z', 'da', 'h', 'k']
decimal_submultiple_prefix = ['a', 'c', 'd', 'f', 'm', 'n', 'p', ['u', 'µ'],
                              'y', 'z']
binary_prefix = ['Ei', 'Gi', 'Ki', 'Mi', 'Pi', 'Ti']
unit_p_symbol = ['Bd', 'B', 'r', 't']
unit_n_symbol = ['L', 'Np', ['oC', '°C'], ['o', '°'], 'rad', 'sr']
unit_b_symbol = ['A', 'Bq', 'C', 'F', 'Gy', 'Hz', 'H', 'J', 'K', 'N',
                 ['Ohm', 'Ω'], 'Pa', 'Sv', 'S', 'T', 'V', 'Wb', 'W', 'bit',
                 'cd', 'eV', 'g', 'kat', 'lm', 'lx', 'mol', 'm', 's',
                 ]
unit_b_N_index = unit_b_symbol.index('N')
unit___symbol = ['dB', 'd', 'h', 'min', 'u']
currency = ['[A-Z][A-Z][A-Z]']


def encapsulate(value_list):
    if all([isinstance(val, str) for val in value_list]):
        return r'(' + r'|'.join(value_list) + r')'
    return encapsulate([val if isinstance(val, str) else encapsulate(val) for val in value_list])


def to_regex(components):
    if not isinstance(components, list):
        components = [components]
    return r''.join([encapsulate(comp) for comp in components])


def to_list(unit_list):
    out = []
    for val in unit_list:
        if isinstance(val, str):
            out.append(val)
        else:
            out.extend(val)
    return out


def create_combos():
    """
    punit
        : decimal_multiple_prefix unit_p_symbol
        | decimal_submultiple_prefix unit_n_symbol
        | decimal_multiple_prefix unit_b_symbol
        | decimal_submultiple_prefix unit_b_symbol
        | binary_prefix 'B'
        | binary_prefix 'bit'
        | unit_p_symbol
        | unit_n_symbol
        | unit_b_symbol
        | unit___symbol
        ;
    """
    def combine(list1, list2):
        combos = []
        for val1 in to_list(list1):
            for val2 in to_list(list2):
                combos.append(val1 + val2)
        return combos
    combos = combine(decimal_multiple_prefix, unit_p_symbol) + \
             combine(decimal_submultiple_prefix, unit_n_symbol) + \
             combine(decimal_multiple_prefix, unit_b_symbol) + \
             combine(decimal_submultiple_prefix, unit_b_symbol) + \
             combine(binary_prefix, ["B", "bit"]) + \
             to_list(unit_p_symbol) + to_list(unit_n_symbol) + \
             to_list(unit_b_symbol) + to_list(unit___symbol)
    return ["1"+val for val in combos]


class CMIXFLexer(Lexer):

    tokens = {
        REAL,
        MULTIP,
        SUBMULTIN,
        MULTIB,
        SUBMULTIB,
        UNITC,
        DOT,
        DIV,
        LPAREN,
        RPAREN,
        EXP,
        BIT,
        BYTE,
    }
    ignore = " \t"

    # Tokens
    DIV = r"/"
    LPAREN = r"\("
    RPAREN = r"\)"
    EXP = r"\^"
    REAL = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
    DOT = r"\."
    BIT = to_regex([binary_prefix, [r"bit"]])
    BYTE = to_regex([binary_prefix, [r"B"]])
    SUBMULTIN = r"mol|" + to_regex([decimal_submultiple_prefix, unit_n_symbol])
    MULTIB = to_regex([decimal_multiple_prefix, currency + unit_b_symbol])
    SUBMULTIB = to_regex([decimal_submultiple_prefix, currency + unit_b_symbol])
    MULTIP = to_regex([decimal_multiple_prefix, unit_p_symbol])
    UNITC = r'|'.join([encapsulate(val)[1:-1] for val in [currency + unit_b_symbol[:unit_b_N_index],
                                                          unit___symbol,
                                                          unit_n_symbol,
                                                          unit_b_symbol[unit_b_N_index:],
                                                          unit_p_symbol,
                                                          ]
                       ])

    def error(self, t):
        raise ValueError("Line %d: Bad character %r" % (self.lineno, t.value[0]))


class CMIXFParser(Parser):
    tokens = CMIXFLexer.tokens

    def __init__(self):
        self.names = {}

    """
    quantity_value
            : real
            | real ' ' unit
            | real '.' unit
            | real unit
            ;
    """

    @_("real")
    def quantity(self, p):
        return p.real

    @_("real unit")
    def quantity(self, p):
        return p.real + p.unit

    @_("real DOT unit")
    def quantity(self, p):
        return p.real + p.DOT + p.unit

    """
    unit
        : unit_product
        | unit_product '/' single_unit
        ;
    """

    @_("unit_product")
    def unit(self, p):
        return p.unit_product

    @_("unit_product DIV single_unit")
    def unit(self, p):
        return p.unit_product + p.DIV + p.single_unit

    """
    unit_product
        : single_unit
        | unit_product '.' single_unit
        ;
    """

    @_("single_unit")
    def unit_product(self, p):
        return p.single_unit

    @_("unit_product DOT single_unit")
    def unit_product(self, p):
        return p.unit_product + p.DOT + p.single_unit

    """
    single_unit
        : punit
        | punit '^' uxponent
        | '(' unit ')'
        | '(' unit ')^' uxponent
        ;
    """

    @_("punit")
    def single_unit(self, p):
        return p.punit

    @_("punit EXP uxponent")
    def single_unit(self, p):
        return p.punit + p.EXP + p.uxponent

    @_("LPAREN unit RPAREN")
    def single_unit(self, p):
        return p.LPAREN + p.unit + p.RPAREN

    @_("LPAREN unit RPAREN EXP uxponent")
    def single_unit(self, p):
        return p.LPAREN + p.unit + p.RPAREN + p.EXP + p.uxponent

    """
    uxponent
        : uinteger
        | '-' uinteger
        | '(' uinteger '/' uinteger ')'
        | '(-' uinteger '/' uinteger ')'
        ;
    """

    @_("real")
    def uxponent(self, p):
        return p.real

    @_("LPAREN real DIV real RPAREN")
    def uxponent(self, p):
        return p.LPAREN + p.real0 + p.DIV + p.real1 + p.RPAREN

    """
    punit
        : decimal_multiple_prefix unit_p_symbol
        | decimal_submultiple_prefix unit_n_symbol
        | decimal_multiple_prefix unit_b_symbol
        | decimal_submultiple_prefix unit_b_symbol
        | binary_prefix 'B'
        | binary_prefix 'bit'
        | unit_p_symbol
        | unit_n_symbol
        | unit_b_symbol
        | unit___symbol
        ;
    """

    @_("MULTIP")
    def punit(self, p):
        return p.MULTIP

    @_("SUBMULTIN")
    def punit(self, p):
        return p.SUBMULTIN

    @_("MULTIB")
    def punit(self, p):
        return p.MULTIB

    @_("SUBMULTIB")
    def punit(self, p):
        return p.SUBMULTIB

    @_("BYTE")
    def punit(self, p):
        return p.BYTE

    @_("BIT")
    def punit(self, p):
        return p.BIT

    @_("UNITC")
    def punit(self, p):
        return p.UNITC

    @_("REAL")
    def real(self, p):
        return p.REAL

    def error(self, t):
        super(CMIXFParser, self).error(t)
        raise RuntimeError(f"Could not parse {t}")


def parse(text, debug):
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    tokens = lexer.tokenize(text)
    if debug:
        for tok in tokens:
            print("type=%r, value=%r" % (tok.type, tok.value))
    print(parser.parse(tokens))


@click.command()
@click.option("-d", "--debug", is_flag=True, help="Turn on token debugging")
@click.argument("text", nargs=-1)
def main(debug, text):
    if text:
        for val in text:
            parse(val, debug)
        return
    while True:
        try:
            text = input("cmixf (Ctrl+d to quit) > ")
        except EOFError:
            break
        if text:
            try:
                parse(text, debug)
            except Exception as e:
                print("FAILED: ", e)
