# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Simulation
from .serializers import SimulationSerializer, SimulationConfigSerializer, GridStateSerializer
from .simulation_engine import SimulationEngine

global_engine = None

class SimulationViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les simulations de robots nettoyeurs
    """
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer

    # Variable pour stocker l'instance du moteur de simulation
    simulation_engine = None

    @action(detail=False, methods=['post'])
    def create_simulation(self, request):
        """Endpoint pour créer une nouvelle simulation"""
        serializer = SimulationConfigSerializer(data=request.data)
        if serializer.is_valid():
            # Créer une nouvelle simulation dans la base de données
            simulation = Simulation.objects.create(
                num_robots=serializer.validated_data['num_robots'],
                num_trash=serializer.validated_data['num_trash'],
                base_x=serializer.validated_data['base_x'],
                base_y=serializer.validated_data['base_y']
            )
            global global_engine
            # Initialiser le moteur de simulation
            global_engine = SimulationEngine(
                grid_size=simulation.grid_size,
                num_robots=simulation.num_robots,
                num_trash=simulation.num_trash,
                base_position=(simulation.base_x, simulation.base_y)
            )

            return Response(SimulationSerializer(simulation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def step(self, request):
        """Endpoint pour avancer d'un tour dans la simulation"""
        global global_engine
        if not global_engine:
            return Response({"error": "Aucune simulation n'est en cours"}, status=status.HTTP_400_BAD_REQUEST)
        """
        # Exécuter un tour de simulation
        is_finished = self.simulation_engine.step()

        # Mettre à jour la simulation en base de données
        simulation = Simulation.objects.latest('created_at')
        simulation.turns_elapsed += 1
        simulation.is_running = not is_finished
        simulation.is_finished = is_finished
        simulation.save()

        # Retourner l'état actuel de la grille
        grid_state = self.simulation_engine.get_grid_state()
        serializer = GridStateSerializer(data={
            "grid": grid_state["grid"],
            "robots": grid_state["robots"],
            "trash_remaining": grid_state["trash_remaining"],
            "turns_elapsed": simulation.turns_elapsed,
            "is_finished": is_finished
        })
        serializer.is_valid()  # On suppose que les données sont valides

        return Response(serializer.data)
        """
        # Exécuter un tour de simulation
        is_finished = global_engine.step()

        # Mettre à jour la simulation en base de données
        simulation = Simulation.objects.latest('created_at')
        simulation.turns_elapsed += 1
        simulation.is_running = not is_finished
        simulation.is_finished = is_finished
        simulation.save()

        # Retourner l'état actuel de la grille
        grid_state = global_engine.get_grid_state()
        serializer = GridStateSerializer(data={
            "grid": grid_state["grid"],
            "robots": grid_state["robots"],
            "trash_remaining": grid_state["trash_remaining"],
            "turns_elapsed": simulation.turns_elapsed,
            "is_finished": is_finished
        })
        serializer.is_valid()  # On suppose que les données sont valides

        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def state(self, request):
        """Endpoint pour obtenir l'état actuel de la simulation"""
        global global_engine
        if not global_engine:
            return Response({"error": "Aucune simulation n'est en cours"}, status=status.HTTP_400_BAD_REQUEST)
        """
        simulation = Simulation.objects.latest('created_at')
        grid_state = self.simulation_engine.get_grid_state()

        serializer = GridStateSerializer(data={
            "grid": grid_state["grid"],
            "robots": grid_state["robots"],
            "trash_remaining": grid_state["trash_remaining"],
            "turns_elapsed": simulation.turns_elapsed,
            "is_finished": simulation.is_finished
        })
        serializer.is_valid()  # On suppose que les données sont valides

        return Response(serializer.data)
        """
        return Response(global_engine.get_grid_state())

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Endpoint pour réinitialiser la simulation"""
        serializer = SimulationConfigSerializer(data=request.data)
        if serializer.is_valid():
            # Créer une nouvelle simulation
            simulation = Simulation.objects.create(
                num_robots=serializer.validated_data['num_robots'],
                num_trash=serializer.validated_data['num_trash'],
                base_x=serializer.validated_data['base_x'],
                base_y=serializer.validated_data['base_y']
            )

            # Réinitialiser le moteur de simulation
            self.simulation_engine = SimulationEngine(
                grid_size=simulation.grid_size,
                num_robots=simulation.num_robots,
                num_trash=simulation.num_trash,
                base_position=(simulation.base_x, simulation.base_y)
            )

            return Response(SimulationSerializer(simulation).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)