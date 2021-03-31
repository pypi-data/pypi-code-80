import re


def check_value(currency, letter_index, verified_currency, checked_decimal):
    if letter_index > 2 or checked_decimal:
        return verified_currency + ((currency[letter_index:]).replace('.', '')).replace(',', '')

    if letter_index <= 2 and (currency[letter_index] == "." or currency[letter_index] == ","):
        checked_decimal = True
        return check_value(currency, letter_index + 1, verified_currency + ".", checked_decimal)
    else:
        return check_value(currency, letter_index + 1, verified_currency + currency[letter_index], checked_decimal)


def parser(currency):
    currency = re.sub(r'[^\d.,]', '', currency)

    verified_currency = check_value(currency[::-1], 0, "", False)

    if verified_currency.find(".") == 0:
        return verified_currency[::-1] + "00"

    elif verified_currency.find(".") == -1:
        return verified_currency[::-1] + ".00"

    return verified_currency[::-1]
