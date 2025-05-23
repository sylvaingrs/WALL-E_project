import random
from typing import List, Tuple, Dict, Set
from queue import PriorityQueue


def a_star(start, goal, grid, obstacles):
    def manhattanDistance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # distance de Manhattan

    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        _, current = frontier.get()

        if current == goal:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_node = (current[0] + dx, current[1] + dy)
            if (0 <= next_node[0] < len(grid) and
                0 <= next_node[1] < len(grid[0]) and
                next_node not in obstacles and
                grid[next_node[0]][next_node[1]] != "B"):  # on peut ignorer B ici si on vise B
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + manhattanDistance(goal, next_node)
                    frontier.put((priority, next_node))
                    came_from[next_node] = current

    # Reconstituer le chemin
    if goal not in came_from:
        return None  # Pas de chemin

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

class Robot:
    def __init__(self, x: int, y: int, robot_id: int):
        self.x = x
        self.y = y
        self.id = robot_id
        self.carrying_trash = False
        self.vision_radius = 5
        self.known_trash: Set[Tuple[int, int]] = set()
        self.visited_cells: Set[Tuple[int, int]] = {(x, y)}
        self.random_direction: Tuple[int, int] = {0, 0}
        self.steps_in_direction: int = 0

    def move(self, dx: int, dy: int, grid_size: int, obstacles: List[Tuple[int, int]]) -> bool:
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifier si la nouvelle position est valide
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size and (new_x, new_y) not in obstacles:
            self.x = new_x
            self.y = new_y
            self.visited_cells.add((new_x, new_y))
            return True
        return False

    def pickup_trash(self) -> bool:
        if not self.carrying_trash:
            # print(f"Robot {self.id} picked up trash")
            self.carrying_trash = True
            return True
        return False

    def deposit_trash(self) -> bool:
        if self.carrying_trash:
            self.carrying_trash = False
            return True
        return False

    def see_around(self, grid: List[List[str]]) -> List[Tuple[int, int, str]]:
        visible_cells = []
        for i in range(-self.vision_radius, self.vision_radius + 1):
            for j in range(-self.vision_radius, self.vision_radius + 1):
                x, y = self.x + i, self.y + j
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    visible_cells.append((x, y, grid[x][y]))
        return visible_cells

    def decide_action(self, grid: List[List[str]], base_position: Tuple[int, int],
                      robots_positions: List[Tuple[int, int]]) -> str:
        if self.carrying_trash:
            # Si on porte un déchet, essayer d'aller vers la base
            base_x, base_y = base_position
            if self.x == base_x and self.y == base_y:
                return "deposit"

            # Sinon se déplacer vers la base

            dx = 1 if base_x > self.x else (-1 if base_x < self.x else 0)
            dy = 1 if base_y > self.y else (-1 if base_y < self.y else 0)

            # Si on peut se déplacer horizontalement
            if dx != 0 and (self.x + dx, self.y) not in robots_positions and 0 <= self.x + dx < len(grid):
                return f"move:{dx}:0"

            # Si on peut se déplacer verticalement
            if dy != 0 and (self.x, self.y + dy) not in robots_positions and 0 <= self.y + dy < len(grid[0]):
                return f"move:0:{dy}"

        # Si on est sur un déchet et qu'on n'en porte pas, le ramasser
        if grid[self.x][self.y] == "T" or grid[self.x][self.y] == "RT" and not self.carrying_trash:
            return "pickup"
        # Voir autour
        visible_cells = self.see_around(grid)
        visible_trash = [(x, y) for x, y, v in visible_cells if v == "T"]

        if visible_trash:
            # Aller vers le déchet le plus proche
            target = min(visible_trash, key=lambda t: abs(t[0] - self.x) + abs(t[1] - self.y))
            path = a_star((self.x, self.y), target, grid, set(robots_positions))
            if path:
                next_x, next_y = path[0]
                dx, dy = next_x - self.x, next_y - self.y
                return f"move:{dx}:{dy}"

        # Déplacements aléatoires
        if self.steps_in_direction <= 0 or self.random_direction == {0, 0}:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = self.x + dx, self.y + dy
                if (0 <= new_x < len(grid) and 0 <= new_y < len(grid[0])
                        and (new_x, new_y) not in robots_positions):
                    self.random_direction = (dx, dy)
                    self.steps_in_direction = 10  # Par exemple 10 déplacements
                    break

        # Tenter d'avancer dans la direction actuelle
        dx, dy = self.random_direction
        new_x, new_y = self.x + dx, self.y + dy
        if (0 <= new_x < len(grid) and 0 <= new_y < len(grid[0])
                and (new_x, new_y) not in robots_positions):
            self.steps_in_direction -= 1
            return f"move:{dx}:{dy}"
        else:
            # Si bloqué, on reset pour choisir une nouvelle direction au prochain tour
            self.random_direction = (0, 0)
            self.steps_in_direction = 0
            return "wait"


class SimulationEngine:
    def __init__(self, grid_size: int, num_robots: int, num_trash: int, base_position: Tuple[int, int]):
        self.grid_size = grid_size
        self.num_robots = num_robots
        self.num_trash = num_trash
        self.base_position = base_position
        self.deposited_trash = 0

        # Initialiser la grille (vide)
        self.grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

        # Placer la base
        base_x, base_y = base_position
        self.grid[base_x][base_y] = "B"

        # Initialiser les robots
        self.robots = []
        self._place_robots()

        # Placer les déchets
        self.trash_positions = set()
        self._place_trash()

    def _place_robots(self):
        positions = []

        # S'assurer que les robots ne sont pas placés sur la base
        while len(positions) < self.num_robots:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) != self.base_position and (x, y) not in positions:
                positions.append((x, y))
                self.robots.append(Robot(x, y, len(self.robots)))
                self.grid[x][y] = "R"

    def _place_trash(self):
        # Obtenir les positions occupées (base + robots)
        occupied = {self.base_position} | {(robot.x, robot.y) for robot in self.robots}

        # Placer les déchets
        while len(self.trash_positions) < self.num_trash:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in occupied and (x, y) not in self.trash_positions:
                self.trash_positions.add((x, y))
                self.grid[x][y] = "T"

    def step(self) -> bool:
        # Si plus de déchets, la simulation est terminée
        if self.deposited_trash >= self.num_trash:
            return True

        # Positions actuelles des robots pour éviter les collisions
        robot_positions = {(robot.x, robot.y) for robot in self.robots}

        for robot in self.robots:
            # Mettre à jour la connaissance du robot sur son environnement
            visible_cells = robot.see_around(self.grid)
            for x, y, cell_type in visible_cells:
                if cell_type == "T":
                    robot.known_trash.add((x, y))

            # Retirer les déchets ramassés de la connaissance du robot
            robot.known_trash -= self.trash_positions

            # Décider de l'action
            action = robot.decide_action(self.grid, self.base_position, robot_positions)

            # Exécuter l'action
            if action.startswith("move"):
                _, dx, dy = action.split(":")
                dx, dy = int(dx), int(dy)

                # Mettre à jour la grille et la position du robot
                if robot.move(dx, dy, self.grid_size, list(robot_positions - {(robot.x, robot.y)})):
                    # Enlever le robot de son ancienne position
                    # self.grid[robot.x - dx][robot.y - dy] = "."
                    old_x, old_y = robot.x - dx, robot.y - dy
                    if (old_x, old_y) == self.base_position:
                        self.grid[old_x][old_y] = "B"
                    else:
                        self.grid[old_x][old_y] = "."

                    # Si la nouvelle position contient un déchet et que le robot porte déjà un déchet,
                    # remettre le déchet sur la case
                    if (robot.x, robot.y) in self.trash_positions:
                        self.grid[robot.x][robot.y] = "RT"  # Indique qu’un robot est sur un déchet
                    else:
                        self.grid[robot.x][robot.y] = "R"

                    # Mettre à jour les positions des robots
                    robot_positions.remove((robot.x - dx, robot.y - dy))
                    robot_positions.add((robot.x, robot.y))

            elif action == "pickup":
                if (robot.x, robot.y) in self.trash_positions and robot.pickup_trash():
                    self.trash_positions.remove((robot.x, robot.y))
                    self.grid[robot.x][robot.y] = "R"  # Le robot est maintenant sur la case (sans déchet)
                    # Informer les autres robots que ce déchet a été ramassé
                    for other_robot in self.robots:
                        if (robot.x, robot.y) in other_robot.known_trash:
                            other_robot.known_trash.remove((robot.x, robot.y))

            elif action == "deposit":
                if (robot.x, robot.y) == self.base_position and robot.deposit_trash():
                    self.deposited_trash += 1

            # Pour "wait", aucune action à effectuer

        return False

    def get_grid_state(self) -> Dict:
        return {
            "grid": [row[:] for row in self.grid],
            "robots": [
                {"id": robot.id, "x": robot.x, "y": robot.y, "carrying_trash": robot.carrying_trash}
                for robot in self.robots
            ],
            "trash_remaining": self.num_trash - self.deposited_trash,
        }
