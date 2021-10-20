def direction_to_integer(event_direction: str) -> int:
    if event_direction == 'BUY':
        return 1
    elif event_direction == 'SELL':
        return -1
    else:
        raise ValueError('event direction must be either "BUY" or "SELL"')

def convert_bar(row):
    index, data = row     #* These are the fields the system watches
    output_dict = dict((k, v)
                       for k, v in data.to_dict().items()
                       if k in ['ticker', 'adj_close_price', 'high_price'])
    output_dict['timestamp'] = index
    return output_dict
