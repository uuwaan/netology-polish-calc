import calc

PROMPT_EXPR = "Выражение:"

MSG_STRANGEOP = "Неизвестный оператор: {}"
MSG_RESULT = "Результат: {}"
MSG_ERROR = "Ошибка: {}"
MSG_BYE = "До свидания!"

ERR_CALC = "Непредвиденный сбой вычисления"

OP_QUIT = "q"


def main():
    can_run = True
    while can_run:
        try:
            expr_tokens = user_input(PROMPT_EXPR).split()
        except KeyboardInterrupt:
            expr_tokens = [OP_QUIT]
        if expr_tokens[0] == OP_QUIT:
            can_run = False
        else:
            result, err = eval_expr(expr_tokens)
            if err:
                print(MSG_ERROR.format(str(err)))
            elif result:
                print(MSG_RESULT.format(result))
            else:
                print(ERR_CALC)
        print()
    print(MSG_BYE)


def eval_expr(expr_tokens):
    try:
        result = calc.expr_result(expr_tokens)
        return result, None
    except calc.ExpressionError as e:
        return None, e


def user_input(prompt):
    result = None
    while not result:
        result = input(prompt + " ").strip()
    return result
