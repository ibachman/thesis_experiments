import socket

def dividendo_hipotecario(precio_pesos, pie_porcentaje, tiempo_anios, tasa):
    precio = precio_pesos
    pie = precio * pie_porcentaje
    tiempo = tiempo_anios
    monto_credito = precio - pie
    tasa = tasa/100
    div = (monto_credito * (1 + tasa) * tiempo) / (12 * tiempo + 12 * (1 + tasa) * ((tiempo - 1) * (tiempo - 2) / 2))
    return div


def anios_para_liquidar(precio_pesos, pie_pesos, extra, ahorro_anual, dividendo):
    ahorro_mensual = ahorro_anual / 12 + dividendo
    meses = (precio_pesos - (pie_pesos + extra)) / ahorro_mensual
    anios = meses / 12
    return anios

def run():
    millon = 1000000
    anios_arriendo = 0

    precio_pesos = 155 * millon
    pie_pesos = precio_pesos * 0.2
    dividendo = 0.9 * millon
    extra = (55 + 18 * anios_arriendo) * millon + 12 * anios_arriendo * dividendo
    ahorro_anual = 15 * millon - (0.06 + dividendo / millon - 0.35) * millon * 12
    print(15 * millon - dividendo * 12)
    print(anios_para_liquidar(precio_pesos, pie_pesos, extra, ahorro_anual, dividendo))

    ahorro_anual_real = 16 * millon - (0.75 + 0.2) * millon * 12
    print(16 * millon / 12 + 600000 - 1800000 - 1900000)

