import random
from typing import List, Tuple, Dict, Set


class Robot:
    """Classe représentant un robot"""

    def __init__(self, x: int, y: int, robot_id: int):
        self.x = x
        self.y = y
        self.id = robot_id
        self.carrying_trash = False
        self.vision_radius = 5
        self.known_trash: Set[Tuple[int, int]] = set()
        self.visited_cells: Set[Tuple[int, int]] = {(x, y)}

    def move(self, dx: int, dy: int, grid_size: int, obstacles: List[Tuple[int, int]]) -> bool:
        """Déplace le robot dans la direction spécifiée si possible"""
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
        """Le robot ramasse un déchet s'il n'en transporte pas déjà un"""
        if not self.carrying_trash:
            self.carrying_trash = True
            return True
        return False

    def deposit_trash(self) -> bool:
        """Le robot dépose un déchet s'il en transporte un"""
        if self.carrying_trash:
            self.carrying_trash = False
            return True
        return False

    def see_around(self, grid: List[List[str]]) -> List[Tuple[int, int, str]]:
        """Retourne les cellules visibles autour du robot dans un rayon de 5"""
        visible_cells = []
        for i in range(-self.vision_radius, self.vision_radius + 1):
            for j in range(-self.vision_radius, self.vision_radius + 1):
                x, y = self.x + i, self.y + j
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    visible_cells.append((x, y, grid[x][y]))
        return visible_cells

    def decide_action(self, grid: List[List[str]], base_position: Tuple[int, int],
                      robots_positions: List[Tuple[int, int]]) -> str:
        """Décide de l'action à effectuer (version de base: mouvement aléatoire)"""
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
        if grid[self.x][self.y] == "T" and not self.carrying_trash:
            return "pickup"

        # Sinon, mouvement aléatoire
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # haut, droite, bas, gauche
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if (0 <= new_x < len(grid) and
                    0 <= new_y < len(grid[0]) and
                    (new_x, new_y) not in robots_positions):
                return f"move:{dx}:{dy}"

        # Si aucun mouvement n'est possible
        return "wait"


class SimulationEngine:
    """Moteur de simulation pour les robots nettoyeurs"""

    def __init__(self, grid_size: int, num_robots: int, num_trash: int, base_position: Tuple[int, int]):
        self.grid_size = grid_size
        self.num_robots = num_robots
        self.num_trash = num_trash
        self.base_position = base_position

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
        """Place les robots aléatoirement sur la grille"""
        positions = []

        # S'assurer que les robots ne sont pas placés sur la base
        while len(positions) < self.num_robots:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) != self.base_position and (x, y) not in positions:
                positions.append((x, y))
                self.robots.append(Robot(x, y, len(self.robots)))
                self.grid[x][y] = "R"  # R pour Robot

    def _place_trash(self):
        """Place les déchets aléatoirement sur la grille"""
        # Obtenir les positions occupées (base + robots)
        occupied = {self.base_position} | {(robot.x, robot.y) for robot in self.robots}

        # Placer les déchets
        while len(self.trash_positions) < self.num_trash:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in occupied and (x, y) not in self.trash_positions:
                self.trash_positions.add((x, y))
                self.grid[x][y] = "T"  # T pour Trash (déchet)

    def step(self) -> bool:
        """Exécute un tour de simulation. Retourne True si la simulation est terminée."""
        # Si plus de déchets, la simulation est terminée
        if not self.trash_positions and all(not robot.carrying_trash for robot in self.robots):
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
                    self.grid[robot.x - dx][robot.y - dy] = "."

                    # Si la nouvelle position contient un déchet et que le robot porte déjà un déchet,
                    # remettre le déchet sur la case
                    if (robot.x, robot.y) in self.trash_positions:
                        self.grid[robot.x][robot.y] = "R"  # Le robot est prioritaire sur l'affichage
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
                    # Le déchet est déposé à la base (et disparaît du jeu)
                    pass

            # Pour "wait", aucune action à effectuer

        return False  # La simulation continue

    def get_grid_state(self) -> Dict:
        """Retourne l'état actuel de la grille pour l'API"""
        return {
            "grid": [row[:] for row in self.grid],  # Copie profonde de la grille
            "robots": [
                {"id": robot.id, "x": robot.x, "y": robot.y, "carrying_trash": robot.carrying_trash}
                for robot in self.robots
            ],
            "trash_remaining": len(self.trash_positions)
        }
