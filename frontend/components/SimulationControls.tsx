import React from 'react';

interface SimulationControlsProps {
  isRunning: boolean;
  isFinished: boolean;
  onStep: () => void;
  onAutoRun: () => void;
  onPause: () => void;
  onReset: () => void;
  turnsElapsed: number;
  trashRemaining: number;
}

const SimulationControls: React.FC<SimulationControlsProps> = ({
  isRunning,
  isFinished,
  onStep,
  onAutoRun,
  onPause,
  onReset,
  turnsElapsed,
  trashRemaining
}) => {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="mb-4 text-xl font-bold">Contrôles de simulation</h2>

      <div className="mb-4 space-y-2">
        <div className="flex items-center justify-between">
          <span className="font-medium">Tours écoulés:</span>
          <span className="text-blue-600">{turnsElapsed}</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="font-medium">Déchets restants:</span>
          <span className="text-yellow-600">{trashRemaining}</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="font-medium">État:</span>
          <span className={isFinished ? 'text-green-600' : isRunning ? 'text-blue-600' : 'text-gray-600'}>
            {isFinished ? 'Terminé' : isRunning ? 'En cours' : 'En attente'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={onStep}
          disabled={isFinished}
          className="px-3 py-2 text-white bg-blue-500 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          Étape suivante
        </button>

        {isRunning ? (
          <button
            onClick={onPause}
            disabled={isFinished}
            className="px-3 py-2 text-white bg-yellow-500 rounded hover:bg-yellow-600 disabled:bg-gray-400"
          >
            Pause
          </button>
        ) : (
          <button
            onClick={onAutoRun}
            disabled={isFinished}
            className="px-3 py-2 text-white bg-green-500 rounded hover:bg-green-600 disabled:bg-gray-400"
          >
            Exécution auto
          </button>
        )}

        <button
          onClick={onReset}
          className="col-span-2 px-3 py-2 text-white bg-red-500 rounded hover:bg-red-600"
        >
          Réinitialiser
        </button>
      </div>
    </div>
  );
};

export default SimulationControls;