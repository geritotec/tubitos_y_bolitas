def mover_bolita(tubitos, source_index, destination_index):
    # Check if the source tube is empty or contains only "nada" values
    source_tube = tubitos[source_index]
    destination_tube = tubitos[destination_index]

    # Find the last non-"nada" ball in the source tube
    source_ball = None
    for ball in reversed(source_tube):
        if ball != "nada":
            source_ball = ball
            break
    
    if source_ball is None:
        return False  # No balls to move (source tube is empty)

    # Find the last non-"nada" ball in the destination tube
    destination_ball = None
    for ball in reversed(destination_tube):
        if ball != "nada":
            destination_ball = ball
            break

    # Check if the destination tube is not full
    if len([b for b in destination_tube if b != "nada"]) >= 4:
        return False  # Destination tube is full

    # Move the ball only if the destination is empty or has the same color as the ball
    if destination_ball is None or destination_ball == source_ball:
        # Remove the ball from the source tube
        for i in range(len(source_tube) - 1, -1, -1):
            if source_tube[i] == source_ball:
                source_tube[i] = "nada"
                break
        
        # Add the ball to the destination tube
        for i in range(len(destination_tube) - 1, -1, -1):
            if destination_tube[i] == "nada":
                destination_tube[i] = source_ball
                break

        return True  # Successful move
    
    return False  # Invalid move
