from abc import ABC, abstractmethod


class Card:
    def __init__(self, init_state: bool = True):
        if init_state:
            self.state = ActiveCard()
        else:
            self.state = InactiveCard()

    def setState(self, state):
        self.state = state

    def status(self):
        return self.state.status()

    def change(self):
        self.state.change_state(self)


class State(ABC):
    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def change_state(self, card_state: Card):
        pass


class ActiveCard(State):
    def status(self):
        return True

    def change_state(self, card_state: Card):
        card_state.setState(InactiveCard())


class InactiveCard(State):
    def status(self):
        return False

    def change_state(self, card_state: Card):
        card_state.setState(ActiveCard())
