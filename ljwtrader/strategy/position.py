from dataclasses import dataclass
from ljwtrader.data import DataHandler

class Position:

    def __init__(self, ticker, indicator, direction, exit_when=None):
        self.ticker = ticker
        self.indicator = indicator
        self.direction = direction
        self.current_direction = 'OUT'
        self.exit_when = exit_when

    def translate_direction(self, direction) -> str:
        DIRECTION_ERROR = ValueError("Class direction and contextual directions must be either LONG or SHORT")
        # TODO: Should change this string return to an enumeration

        if self.direction == 'LONG':
            if direction == 'IN':
                return "BUY"
            elif direction == 'OUT':
                return "SELL"
            else:
                raise DIRECTION_ERROR
        elif self.direction == 'SHORT':
            if direction == 'IN':
                return "SELL"
            elif direction == 'OUT':
                return "BUY"
            else:
                raise DIRECTION_ERROR
        else:
            raise DIRECTION_ERROR

    def enter_position(self, data_handler: DataHandler) -> str:
        result = self.indicator(data_handler=data_handler)
        if self.current_direction == 'OUT' and result:
            self.current_direction = 'IN'
            return self.translate_direction(self.current_direction)   
        return

    def exit_position(self, data_handler: DataHandler) -> str:
        # * Defaults to whenever the indicator is false, but a separate indicator can be supplied as the exit condition
        exit_condition = self.exit_when(data_handler) if self.exit_when else not self.indicator(data_handler=data_handler)
        if self.current_direction == 'IN' and exit_condition:
            self.current_direction = 'OUT'
            return self.translate_direction(self.current_direction)
        return