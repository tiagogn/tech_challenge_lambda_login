def validar_cpf(cpf: str) -> bool:
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma_1 * 10) % 11
    if digito_1 == 10:
        digito_1 = 0

    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(9)) + digito_1 * 2
    digito_2 = (soma_2 * 10) % 11
    if digito_2 == 10:
        digito_2 = 0

    return cpf[-2:] == f'{digito_1}{digito_2}'
