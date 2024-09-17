import random

def generar_tubitos(difficulty):

    colores_existentes = ["rosa", "amarillo", "aqua", "naranja", "morado", "checker_blanco", "checker_aqua", "checker_rosa", "checker_naranja"]
    sin_bolita = "nada"

    cantidad_colores_bolitas = 3 * difficulty
    cantidad_tubitos = cantidad_colores_bolitas + 2
    cantidad_bolitas_por_color = 4
    espacio_por_tubito = cantidad_bolitas_por_color

    colores_seleccionados = random.sample(colores_existentes, cantidad_colores_bolitas)
    
    bolitas = []
    for color in colores_seleccionados:
        bolitas.extend([color] * cantidad_bolitas_por_color)
    
    random.shuffle(bolitas)
    
    tubitos = []
    for i in range(cantidad_tubitos):
        if i < cantidad_colores_bolitas:

            tubito = []
            for _ in range(espacio_por_tubito):
                if bolitas:
                    tubito.append(bolitas.pop())
                else:
                    tubito.append(sin_bolita)
            tubitos.append(tubito)
        else:
    
            tubitos.append([sin_bolita] * espacio_por_tubito)
    
    return tubitos

if __name__ == "__main__":
    tubitos = generar_tubitos(1)
    for tubito in tubitos:
        print(tubito)