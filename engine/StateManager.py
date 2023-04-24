class stateManager:
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
    
    def deleteState(self, index):
        """Delete a state from the history by index."""
        if 0 <= index < len(self.history) and index != self.current_state:
            del self.history[index]
            if index < self.current_state:
                self.current_state -= 1
            # Check if current state needs to be updated
            elif index == self.current_state:
                self.current_state = -1
            else:
                # self.current_state remains unchanged
                pass
            
    def deleteCurrentState(self):
        """Delete the current state from the history."""
        if self.current_state != -1:
            del self.history[self.current_state]
            if self.current_state > 0:
                self.current_state -= 1
            else:
                self.current_state = -1

    def clearHistory(self):
        """Clear the history."""
        self.history = []
        self.current_state = -1
