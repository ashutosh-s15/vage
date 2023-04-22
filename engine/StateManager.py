class StateManager:
    def __init__(self):
        self.history = [] # List to store state history
        self.current_state = -1 # Variable to store the current state

    def addState(self, state):
        """Add a state to the history."""
        if self.current_state < len(self.history) - 1:
            # If we undid before, remove redo states
            self.history = self.history[:self.current_state+1]
        self.history.append(state)
        self.current_state = len(self.history) - 1

    def prevState(self):
        """Undo the previous state."""
        if self.current_state > 0:
            self.current_state -= 1
            return self.history[self.current_state]
        return None

    def nextState(self):
        """Redo the next state."""
        if self.current_state < len(self.history) - 1:
            self.current_state += 1
            return self.history[self.current_state]
        return None

    def clearHistory(self):
        """Clear the history."""
        self.history = []
        self.current_state = -1
