def player(prev_play, state=[None]):
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}

    if state[0] is None:
        state[0] = {
            'opp': [],
            'mine': [],
            'orders': {2: {}, 3: {}, 4: {}, 5: {}},
            'scores': {'m2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'ak': 0, 'anti_abbey': 0},
            'last_preds': {'m2': 'R', 'm3': 'R', 'm4': 'R', 'm5': 'R', 'ak': 'R', 'anti_abbey': 'R'},
            'abbey_sim': {'opp_hist': [], 'po': {"RR":0,"RP":0,"RS":0,"PR":0,"PP":0,"PS":0,"SR":0,"SP":0,"SS":0}},
        }

    s = state[0]
    if prev_play == '':
        prev_play = 'R'

    if s['mine']:
        for k in list(s['last_preds']):
            if s['last_preds'][k] == prev_play:
                s['scores'][k] += 3
            else:
                s['scores'][k] -= 1

    s['opp'].append(prev_play)
    history = s['opp']
    n = len(history)

    for length in [2, 3, 4, 5]:
        if n >= length:
            key = ''.join(history[-length:])
            s['orders'][length][key] = s['orders'][length].get(key, 0) + 1

    preds = {}
    for length in [2, 3, 4, 5]:
        mk = f'm{length}'
        if n >= length:
            pattern = ''.join(history[-(length-1):])
            candidates = {pattern + c: s['orders'][length].get(pattern + c, 0) for c in 'RPS'}
            predicted = max(candidates, key=candidates.get)[-1]
            preds[mk] = beat[predicted]
        else:
            preds[mk] = beat[prev_play]

    if s['mine']:
        ak_pred = beat[s['mine'][-1]]
        preds['ak'] = beat[ak_pred]
    else:
        preds['ak'] = 'P'

    ab = s['abbey_sim']
    my_last = s['mine'][-1] if s['mine'] else 'R'
    ab['opp_hist'].append(my_last)
    ab_hist = ab['opp_hist']
    ab_last_two = ''.join(ab_hist[-2:])
    if len(ab_last_two) == 2:
        ab['po'][ab_last_two] = ab['po'].get(ab_last_two, 0) + 1
    ab_potential = [my_last + c for c in 'RPS']
    ab_sub = {k: ab['po'].get(k, 0) for k in ab_potential}
    ab_prediction = max(ab_sub, key=ab_sub.get)[-1]
    abbey_will_play = beat[ab_prediction]
    preds['anti_abbey'] = beat[abbey_will_play]

    s['last_preds'] = preds
    best = max(s['scores'], key=s['scores'].get)
    guess = preds[best]
    s['mine'].append(guess)
    return guess
