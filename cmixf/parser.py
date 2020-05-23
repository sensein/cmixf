from sly import Lexer, Parser

decimalsubmultiple = r"(a|c|d|f|m|n|p|u|y|z)"
decimalmultiple = r"(E|G|M|P|T|Y|Z|da|h|k)"
unitb = (
    r"([A-Z][A-Z][A-Z]|A|Bq|C|F|Gy|H|Hz|J|K|N|Ohm|Pa|Sv|S|T|V|W|Wb"
    r"|bit|cd|eV|g|kat|lm|lx|mol|m|s)"
)
unitn = r"(L|Np|oC|o|rad|sr)"
unitp = r"(Bd|B|r|t)"
binary = r"(Ei|Gi|Ki|Mi|Pi|Ti)"


class CMIXFLexer(Lexer):

    tokens = {
        REAL,
        MULTIP,
        SUBMULTIN,
        MULTIB,
        SUBMULTIB,
        UNITP,
        UNITN,
        UNITB,
        UNITS,
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
    MULTIP = decimalmultiple + unitp
    SUBMULTIN = decimalsubmultiple + unitn
    MULTIB = decimalmultiple + unitb
    SUBMULTIB = decimalsubmultiple + unitb
    BIT = binary + r"bit"
    BYTE = binary + r"B"
    UNITS = r"(dB|d|h|min|u)"
    UNITB = unitb
    UNITN = unitn
    UNITP = unitp

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

    @_("UNITP")
    def punit(self, p):
        return p.UNITP

    @_("UNITN")
    def punit(self, p):
        return p.UNITN

    @_("UNITB")
    def punit(self, p):
        return p.UNITB

    @_("UNITS")
    def punit(self, p):
        return p.UNITS

    @_("REAL")
    def real(self, p):
        return p.REAL

    def error(self, t):
        super(CMIXFParser, self).error(t)
        raise RuntimeError(f"Could not parse {t}")


def main():
    lexer = CMIXFLexer()
    parser = CMIXFParser()
    while True:
        try:
            text = input("cmixf > ")
        except EOFError:
            break
        if text:
            for tok in lexer.tokenize(text):
                print("type=%r, value=%r" % (tok.type, tok.value))
            print(parser.parse(lexer.tokenize(text)))
