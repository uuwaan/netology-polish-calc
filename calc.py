ERR_NOP = "элемент выражения не является арифметической операцией"
ERR_BAD = "недопустимый элемент выражения"
ERR_OPS = "в хвосте выражения содержатся лишние элементы"
ERR_ARGS = "недостаточно аргументов для операции"
ERR_ZDIV = "деление на 0"

FMT_ERROR = "[позиция {0}, элемент '{1}'] {2}"

CALC_OPS = {
    "+": lambda lhs, rhs: lhs + rhs,
    "-": lambda lhs, rhs: lhs - rhs,
    "*": lambda lhs, rhs: lhs * rhs,
    "/": lambda lhs, rhs: lhs / rhs,
}


class ExpressionError(ValueError):
    def __str__(self):
        return FMT_ERROR.format(*self.args)


class ExprToken:
    def __init__(self, pos, img):
        self.pos = pos
        self.img = img

    @classmethod
    def try_parse(cls, pos, img):
        return cls(pos, img)


class ValueToken(ExprToken):
    def __init__(self, pos, img, value):
        super(ValueToken, self).__init__(pos, img)
        self.val = value

    def value(self, tok_queue):
        return self.val

    @classmethod
    def try_parse(cls, pos, img):
        try:
            return cls(pos, img, float(img))
        except ValueError:
            return None


class OperationToken(ExprToken):
    def __init__(self, pos, img, op_func):
        super(OperationToken, self).__init__(pos, img)
        self.func = op_func

    def value(self, tok_queue):
        lhs_val = self.next_arg(tok_queue).value(tok_queue)
        rhs_val = self.next_arg(tok_queue).value(tok_queue)
        try:
            return self.func(lhs_val, rhs_val)
        except ZeroDivisionError:
            raise ExpressionError(self.pos, self.img, ERR_ZDIV)

    def next_arg(self, tok_queue):
        try:
            return next(tok_queue)
        except StopIteration:
            raise ExpressionError(self.pos, self.img, ERR_ARGS)

    @classmethod
    def try_parse(cls, pos, img):
        try:
            return cls(pos, img, CALC_OPS[img])
        except KeyError:
            return None


TOKEN_VARIANTS = [
    ValueToken,
    OperationToken,
]


def expr_result(expr_tokens):
    parsed_toks = (parsed_token(tn + 1, t) for tn, t in enumerate(expr_tokens))
    root_op = next(parsed_toks)
    if not isinstance(root_op, OperationToken):
        assert isinstance(root_op, ExprToken)
        raise ExpressionError(root_op.pos, root_op.img, ERR_NOP)
    result = root_op.value(parsed_toks)
    extra_tok = tail_token(parsed_toks)
    if extra_tok:
        raise ExpressionError(extra_tok.pos, extra_tok.img, ERR_OPS)
    else:
        return result


def parsed_token(tok_num, token):
    for tok_var in TOKEN_VARIANTS:
        result = tok_var.try_parse(tok_num, token)
        if result:
            return result
    raise ExpressionError(tok_num, token, ERR_BAD)


def tail_token(tok_queue):
    try:
        return next(tok_queue)
    except StopIteration:
        return None
