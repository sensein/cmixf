quantity_value
        : real
        | real ' ' unit
        | real '.' unit
        | real unit
        ;

unit
    : unit_product
    | unit_product '/' single_unit
    ;

unit_product
    : single_unit
    | unit_product '.' single_unit
    ;

single_unit
    : punit
    | punit '^' uxponent
    | '(' unit ')'
    | '(' unit ')^' uxponent
    ;

uxponent
    : uinteger
    | '-' uinteger
    | '(' uinteger '/' uinteger ')'
    | '(-' uinteger '/' uinteger ')'
    ;

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

decimal_multiple_prefix
    : 'E' | 'G' | 'M' | 'P' | 'T' | 'Y' | 'Z' | 'da' | 'h' | 'k'
    ;

decimal_submultiple_prefix
    : 'a' | 'c' | 'd' | 'f' | 'm' | 'n' | 'p' | 'u' | 'y' | 'z'
    ;

binary_prefix
    : 'Ei' | 'Gi' | 'Ki' | 'Mi' | 'Pi' | 'Ti'
    ;

unit_p_symbol
    : 'B' | 'Bd' | 'r' | 't'
    ;

unit_n_symbol
    : 'L' | 'Np' | 'o' | 'oC' | 'rad' | 'sr'
    ;

unit_b_symbol
    : 'A' | 'Bq' | 'C' | 'F' | 'Gy' | 'H' | 'Hz' | 'J' | 'K' | 'N'
    | 'Ohm' | 'Pa' | 'S' | 'Sv' | 'T' | 'V' | 'W' | 'Wb' | 'bit'
    | 'cd' | 'eV' | 'g' | 'kat' | 'lm' | 'lx' | 'm' | 'mol' | 's'
| currency_symbol
    ;

unit___symbol
    : 'd' | 'dB' | 'h' | 'min' | 'u'
    ;

currency_symbol
    : upper_letter upper_letter upper_letter
;

upper_letter
    : 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J'
| 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T'
| 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
;

real
    : ureal
    | '-' ureal
    ;

ureal
    : numerical_value
    | numerical_value suffix
    ;

numerical_value
    : uinteger
    | dot uinteger
    | uinteger dot uinteger
    | uinteger dot
    ;

dot
    : '.' | ','
    ;

uinteger
    : digit uinteger
    | uinteger
    ;

suffix
    : exponent_marker uinteger
    | exponent_marker '-' uinteger
    ;

exponent_marker
    : 'e' | 'E'
    ;

digit
    : '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    ;
