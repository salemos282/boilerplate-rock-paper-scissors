# RPS.py

def counter(move):
    if move == "R":
        return "P"
    if move == "P":
        return "S"
    return "R"

def player(prev_play, opponent_history=[], my_history=[], transition_table={}):
    
    if prev_play in ["R", "P", "S"]:
        opponent_history.append(prev_play)

    
    if not opponent_history:
        my_history.append("R")
        return "R"

    
    if len(my_history) > 0 and len(opponent_history) > 1:
        my_last = my_history[-1]
        opp_before = opponent_history[-2]
        key = my_last + opp_before
        if key not in transition_table:
            transition_table[key] = {"R": 0, "P": 0, "S": 0}
        transition_table[key][prev_play] += 1

    
    if len(my_history) > 0:
        my_last = my_history[-1]
        opp_last = opponent_history[-1]
        key = my_last + opp_last
        if key in transition_table:
            next_counts = transition_table[key]
            predicted_opp = max(next_counts, key=next_counts.get)
        else:
            counts = {"R": 0, "P": 0, "S": 0}
            for m in opponent_history:
                counts[m] += 1
            predicted_opp = max(counts, key=counts.get)
    else:
        predicted_opp = "R"

    my_move = counter(predicted_opp)
    my_history.append(my_move)
    return my_move
