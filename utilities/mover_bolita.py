def mover_bolita(tubitos, source_index, destination_index):
    source_tube = tubitos[source_index]
    destination_tube = tubitos[destination_index]

    source_ball = None
    for ball in reversed(source_tube):
        if ball != "nada":
            source_ball = ball
            break
    
    if source_ball is None:
        return False # El jugador seleccionó un tubito vacío

    destination_ball = None
    for ball in reversed(destination_tube):
        if ball != "nada":
            destination_ball = ball
            break

    if len([b for b in destination_tube if b != "nada"]) >= 4:
        return False  

    if destination_ball is None or destination_ball == source_ball:
        for i in range(len(source_tube) - 1, -1, -1):
            if source_tube[i] == source_ball:
                source_tube[i] = "nada"
                break
        
        for i in range(len(destination_tube)):
            if destination_tube[i] == "nada":
                destination_tube[i] = source_ball
                break

        return True  
    
    return False

if __name__ == "__main__":
    tubitos = [
        ['rosa', 'checker_rosa', 'naranja', 'rosa'],
        ['checker_rosa', 'checker_rosa', 'rosa', 'checker_rosa'],
        ['naranja', 'rosa', 'naranja', 'naranja'],
        ['nada', 'nada', 'nada', 'nada'],
        ['nada', 'nada', 'nada', 'nada']
    ]
    
    no_resuelto = True
    
    while no_resuelto:
        print(f'Tubitos: ')
        for tubito in tubitos:
            print(tubito)
        source_index = int(input("Selecciona el índice del tubito de origen (0-n): "))
        destination_index = int(input("Selecciona el índice del tubito de destino (0-n): "))

        if mover_bolita(tubitos, source_index, destination_index):
            print("Movimiento exitoso.")

        elif not mover_bolita(tubitos, source_index, destination_index):
            print("Movimiento fallido.")
        
        resuelto = True
        for tube in tubitos:
            if len(set(tube)) != 1:
                resuelto = False

        if resuelto:
            print("Ganaste!")
            no_resuelto = False
