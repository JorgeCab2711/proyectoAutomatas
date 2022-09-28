def a_pairs(table: dict):
    # subset construction already removed the non reachable states
    cadenas = []
    current_state_counter = 0
    next_state_counter = 0
    working = True
    while working:
        if (next_state_counter == len(table['a'])):
            next_state_counter = 0
        elif(current_state_counter == len(table["a"]) - 1):
            working = False
        pair = (
            table["a"][current_state_counter],
            table["a"][next_state_counter]
        )
        if (table["a"][current_state_counter] != table["a"][next_state_counter] and table["a"][current_state_counter] != "NONE" and table["a"][current_state_counter] != "NONE"):
            cadenas.append(pair)
        next_state_counter += 1

        if(next_state_counter == len(table["a"])):
            current_state_counter += 1

    return cadenas
