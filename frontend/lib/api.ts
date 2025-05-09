// API service pour communiquer avec le backend
import axios from 'axios';

// Configuration de base d'axios
const API = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Types pour les données de l'API
export interface SimulationConfig {
  num_robots: number;
  num_trash: number;
  base_x: number;
  base_y: number;
}

export interface Robot {
  id: number;
  x: number;
  y: number;
  carrying_trash: boolean;
}

export interface GridState {
  grid: string[][];
  robots: Robot[];
  trash_remaining: number;
  turns_elapsed: number;
  is_finished: boolean;
}

export interface Simulation {
  id: number;
  num_robots: number;
  num_trash: number;
  grid_size: number;
  base_x: number;
  base_y: number;
  turns_elapsed: number;
  is_running: boolean;
  is_finished: boolean;
  created_at: string;
  updated_at: string;
}

// Service API
export default {
  // Créer une nouvelle simulation
  createSimulation: async (config: SimulationConfig): Promise<Simulation> => {
    const response = await API.post('/simulations/create_simulation/', config);
    return response.data;
  },

  // Avancer d'un pas dans la simulation
  stepSimulation: async (): Promise<GridState> => {
    const response = await API.post('/simulations/step/');
    return response.data;
  },

  // Obtenir l'état actuel de la grille
  getGridState: async (): Promise<GridState> => {
    const response = await API.get('/simulations/state/');
    // console.log('Response', response);
    return response.data;
  },

  // Réinitialiser la simulation
  resetSimulation: async (config: SimulationConfig): Promise<Simulation> => {
    const response = await API.post('/simulations/reset/', config);
    return response.data;
  }
};
