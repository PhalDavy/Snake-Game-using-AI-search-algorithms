from game import Game


class BestFS(Game):
    def __init__(self, game_has_obstacles):
        Game.__init__(self, game_has_obstacles)
        self.open = [self.head]
        self.closed = []
        self.generate_path()

    def calculate_h(self, point):
        """
        Calculates heuristic i.e the Manhatten distance between selected node and goal state
        """
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """
        Implements Best First Search algorithm for snake traversal
        """
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            # select start node as the node with lowest h value
            current = min(self.open, key=lambda x: x.h)
            # remove selected node from self.open
            self.open = [
                self.open[i]
                for i in range(len(self.open))
                if not self.open[i] == current
            ]
            # append selected node to closed_points
            self.closed.append(current)
            # check if snake has reached the goal state
            if current == self.food:
                # based on its origin determine the direction in which the snake will move
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                return
            # explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if (
                    neighbor not in self.closed
                    and neighbor not in self.obstacles
                    and neighbor not in self.snake
                ):
                    # if neighbor is not in self.open increase the cost of path and append neighbor to self.open
                    if neighbor not in self.open:
                        neighbor.h = self.calculate_h(neighbor)
                        neighbor.origin = current
                        self.open.append(neighbor)
        self.path = []

    def main(self):
        self.multi_step_traversal()
