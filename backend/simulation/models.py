from django.db import models

# Create your models here.

class Simulation(models.Model):
    num_robots = models.IntegerField(default=4)
    num_trash = models.IntegerField(default=20)
    grid_size = models.IntegerField(default=32)
    base_x = models.IntegerField(default=0)
    base_y = models.IntegerField(default=0)
    turns_elapsed = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Simulation {self.id} - {self.num_robots} robots, {self.num_trash} déchets"