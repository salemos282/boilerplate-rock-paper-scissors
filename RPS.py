def player(prev_play, state=[None]):
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}

    if prev_play == '' or state[0] is None:
        state[0] = {
            'opp': [],
            'mine': [],
            'orders': {2: {}, 3: {}, 4: {}, 5: {}},
            'scores': {'m2': 0, 'm3': 0, 'm4': 0, 'm5': 0, 'ak': 0, 'anti_abbey': 0},
            'last_preds': {},
            'abbey_sim': {
                'opp_hist': [],
                'po': {"RR":0,"RP":0,"RS":0,"PR":0,"PP":0,"PS":0,"SR":0,"SP":0,"SS":0}
            },
        }
        state[0]['mine'].append('R')
        return 'R'

    s = state[0]

    if s['last_preds']:
        for k, predicted_opp_move in s['last_preds'].items():
            if predicted_opp_move == prev_play:
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

    raw_preds = {}

    for length in [2, 3, 4, 5]:
        mk = f'm{length}'
        if n >= length:
            pattern = ''.join(history[-(length-1):])
            candidates = {pattern + c: s['orders'][length].get(pattern + c, 0) for c in 'RPS'}
            raw_preds[mk] = max(candidates, key=candidates.get)[-1]
        else:
            raw_preds[mk] = prev_play

    my_last = s['mine'][-1]
    raw_preds['ak'] = beat[my_last]

    ab = s['abbey_sim']
    ab['opp_hist'].append(my_last)
    ab_hist = ab['opp_hist']
    if len(ab_hist) >= 2:
        bigram = ab_hist[-2] + ab_hist[-1]
        ab['po'][bigram] = ab['po'].get(bigram, 0) + 1
    ab_potential = [my_last + c for c in 'RPS']
    ab_sub = {k: ab['po'].get(k, 0) for k in ab_potential}
    abbey_predicts_we_play = max(ab_sub, key=ab_sub.get)[-1]
    abbey_will_play = beat[abbey_predicts_we_play]
    raw_preds['anti_abbey'] = abbey_will_play

    s['last_preds'] = raw_preds

    best = max(s['scores'], key=s['scores'].get)
    guess = beat[raw_preds[best]]

    s['mine'].append(guess)
    return guess
