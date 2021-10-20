from ljwtrader.events import Event

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

def calculate_slippage(self, order_event: Event, fill_event: Event) -> float:

    # TODO There needs to be a way to match order events and fill events to compare the assumptions

    order_value = order_event.quantity * order_event.price
    fill_value = fill_event.quantity * fill_event.price
    slippage = fill_value - order_value
    logger.info("Slippage: %f", slippage)
    return slippage