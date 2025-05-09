'use client';

import React, { useState, useEffect, useRef } from 'react';
import Grid from '@/components/Grid';
import ConfigForm from '@/components/ConfigForm';
import SimulationControls from '@/components/SimulationControls';
import SimulationStats from '@/components/SimulationStats';
import API, { GridState, SimulationConfig } from '@/lib/api';

export default function Home() {
  // États pour gérer la simulation
  const [gridState, setGridState] = useState<GridState | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [autoRunInterval, setAutoRunInterval] = useState<NodeJS.Timeout | null>(null);
  const [totalTrash, setTotalTrash] = useState(0);

  // Référence pour stocker la configuration actuelle
  const currentConfigRef = useRef<SimulationConfig>({
    num_robots: 4,
    num_trash: 20,
    base_x: 0,
    base_y: 0
  });

  // Démarrer une nouvelle simulation
  const startSimulation = async (config: SimulationConfig) => {
    try {
      // Mettre à jour la référence de configuration
      // console.log("test 1");
      currentConfigRef.current = config;
      // console.log("test 2");
      setTotalTrash(config.num_trash);
      // console.log("test 3");
      // Créer une nouvelle simulation
      await API.createSimulation(config);
      // console.log("test 4");

      // Obtenir l'état initial de la grille
      const initialState = await API.getGridState();
      // console.log("test 5");
      setGridState(initialState);
      // console.log("test 6");

      // Arrêter l'auto-run précédent si existant
      if (autoRunInterval) {
        clearInterval(autoRunInterval);
        setAutoRunInterval(null);
      }

      setIsRunning(false);
    } catch (error) {
      console.error('Erreur lors du démarrage de la simulation:', error);
    }
  };

  // Avancer d'un pas dans la simulation  
  const stepSimulation = async () => {
    if (!gridState || gridState.is_finished) return;

    try {
      const newState = await API.stepSimulation();
      setGridState(newState);
    } catch (error) {
      console.error('Erreur lors de l\'avancement de la simulation:', error);
    }
  };

  // Démarrer l'exécution automatique
  const startAutoRun = () => {
    if (autoRunInterval || !gridState || gridState.is_finished) return;

    setIsRunning(true);
    const interval = setInterval(async () => {
      try {
        const newState = await API.stepSimulation();
        setGridState(newState);

        // Arrêter l'auto-run si la simulation est terminée
        if (newState.is_finished) {
          clearInterval(interval);
          setAutoRunInterval(null);
          setIsRunning(false);
        }
      } catch (error) {
        console.error('Erreur lors de l\'auto-run:', error);
        clearInterval(interval);
        setAutoRunInterval(null);
        setIsRunning(false);
      }
    }, 500); // Intervalle de 500ms entre chaque étape

    setAutoRunInterval(interval);
  };

  // Mettre en pause l'exécution automatique
  const pauseAutoRun = () => {
    if (!autoRunInterval) return;

    clearInterval(autoRunInterval);
    setAutoRunInterval(null);
    setIsRunning(false);
  };

  // Réinitialiser la simulation
  const resetSimulation = async () => {
    try {
      // Arrêter l'auto-run
      if (autoRunInterval) {
        clearInterval(autoRunInterval);
        setAutoRunInterval(null);
      }

      setIsRunning(false);

      // Redémarrer avec la configuration actuelle
      await startSimulation(currentConfigRef.current);
    } catch (error) {
      console.error('Erreur lors de la réinitialisation:', error);
    }
  };

  // Nettoyage lors du démontage du composant
  useEffect(() => {
    return () => {
      if (autoRunInterval) {
        clearInterval(autoRunInterval);
      }
    };
  }, [autoRunInterval]);

  return (
    <main className="min-h-screen p-8 bg-gray-100">
      <h1 className="mb-8 text-3xl font-bold text-center">Simulation WALL-E</h1>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Panneau de configuration */}
        <div className="space-y-6">
          <ConfigForm
            onSubmit={startSimulation}
            isRunning={isRunning}
          />

          {gridState && (
            <SimulationControls
              isRunning={isRunning}
              isFinished={gridState.is_finished}
              onStep={stepSimulation}
              onAutoRun={startAutoRun}
              onPause={pauseAutoRun}
              onReset={resetSimulation}
              turnsElapsed={gridState.turns_elapsed}
              trashRemaining={gridState.trash_remaining}
            />
          )}

          {gridState && (
            <SimulationStats
              robots={gridState.robots}
              turnsElapsed={gridState.turns_elapsed}
              trashRemaining={gridState.trash_remaining}
              totalTrash={totalTrash}
            />
          )}
        </div>

        {/* Grille de simulation */}
        <div className="col-span-2">
          {gridState ? (
            <div className="p-4 bg-white rounded shadow">
              <h2 className="mb-4 text-xl font-bold">Environnement de simulation</h2>
              <div className="flex items-center justify-center">
                <Grid grid={gridState.grid} robots={gridState.robots} />
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full p-4 bg-white rounded shadow">
              <p className="text-xl text-gray-500">
                Configurez et démarrez une simulation pour voir la grille
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}