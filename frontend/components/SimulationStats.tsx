import React from 'react';
import { Robot } from '@/lib/api';

interface SimulationStatsProps {
  robots: Robot[];
  turnsElapsed: number;
  trashRemaining: number;
  totalTrash: number;
}

const SimulationStats: React.FC<SimulationStatsProps> = ({
  robots,
  turnsElapsed,
  trashRemaining,
  totalTrash
}) => {
  // Calculer le pourcentage de déchets collectés
  const collectedTrash = totalTrash - trashRemaining;
  const percentCollected = totalTrash > 0
    ? Math.round((collectedTrash / totalTrash) * 100)
    : 0;

  // Compter les robots qui transportent des déchets
  const robotsCarrying = robots.filter(robot => robot.carrying_trash).length;

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="mb-4 text-xl font-bold">Statistiques</h2>

      <div className="space-y-3">
        <div>
          <h3 className="mb-1 font-medium">Progrès de la collecte</h3>
          <div className="w-full h-4 bg-gray-200 rounded-full">
            <div
              className="h-4 bg-green-500 rounded-full"
              style={{ width: `${percentCollected}%` }}
            ></div>
          </div>
          <p className="mt-1 text-sm text-gray-600">
            {collectedTrash} / {totalTrash} déchets collectés ({percentCollected}%)
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="font-medium">Robots actifs</h3>
            <p className="text-lg">{robots.length}</p>
          </div>

          <div>
            <h3 className="font-medium">Robots transportant</h3>
            <p className="text-lg">{robotsCarrying} / {robots.length}</p>
          </div>

          <div>
            <h3 className="font-medium">Tours</h3>
            <p className="text-lg">{turnsElapsed}</p>
          </div>

          <div>
            <h3 className="font-medium">Efficacité</h3>
            <p className="text-lg">
              {turnsElapsed > 0 ? (collectedTrash / turnsElapsed).toFixed(2) : '0'}
              <span className="text-sm text-gray-600"> déchets/tour</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimulationStats;