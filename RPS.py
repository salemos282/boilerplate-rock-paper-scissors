def player(prev_play, opponent_history=[], play_order=[{"RR": 0, "RP": 0, "RS": 0, "PR": 0, "PP": 0, "PS": 0, "SR": 0, "SP": 0, "SS": 0}]):
    if not prev_play:
        prev_play = 'R'

    opponent_history.append(prev_play)

    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        prev_play + "R",
        prev_play + "P",
        prev_play + "S",
    ]

    sub_order = {k: play_order[0][k] for k in potential_plays if k in play_order[0]}

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    return ideal_response[prediction]
