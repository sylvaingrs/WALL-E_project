from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimulationViewSet

router = DefaultRouter()
router.register(r'simulations', SimulationViewSet, basename='simulation')

urlpatterns = [
    path('', include(router.urls)),
    #path('simulations/create_simulation/', views.SimulationViewSet.create_simulation, name='create_simulation'),
    #path('simulations/step/', views.SimulationViewSet.step, name='step'),
    #path('simulations/state/', views.SimulationViewSet.state, name='state'),
]