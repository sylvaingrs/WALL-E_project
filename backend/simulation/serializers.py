from rest_framework import serializers
from .models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'

class SimulationConfigSerializer(serializers.Serializer):
    num_robots = serializers.IntegerField(min_value=1, max_value=20, default=4)
    num_trash = serializers.IntegerField(min_value=1, max_value=400, default=20)
    base_x = serializers.IntegerField(min_value=0, max_value=31, default=0)
    base_y = serializers.IntegerField(min_value=0, max_value=31, default=0)

class GridStateSerializer(serializers.Serializer):
    grid = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(max_length=10)
        )
    )
    robots = serializers.ListField(
        child=serializers.DictField()
    )
    trash_remaining = serializers.IntegerField()
    turns_elapsed = serializers.IntegerField()
    is_finished = serializers.BooleanField()
