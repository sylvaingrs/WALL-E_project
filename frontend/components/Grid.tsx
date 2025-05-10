import React from 'react';
import { Robot } from '@/lib/api';

interface GridProps {
  grid: string[][];
  robots: Robot[];
}

const Grid: React.FC<GridProps> = ({ grid, robots }) => {
  const cellSize = 20; // taille d'une cellule en pixels

  // Calculer la taille totale de la grille
  const gridSize = grid.length * cellSize;

  // Fonction pour obtenir la couleur d'une cellule en fonction de son contenu
  const getCellColor = (cellContent: string, robot: Robot | undefined): string => {

      if (robot) {
        return robot.carrying_trash ? 'bg-orange-500' : 'bg-blue-500'
    }

      switch (cellContent) {
      // case 'R': return 'bg-blue-500'; // Robot
      case 'T': return 'bg-yellow-500'; // Déchet
      case 'B': return 'bg-green-500'; // Base
      // case 'RT': return 'bg-orange-500'; // Robot qui prend un déchet
      default: return 'bg-gray-200'; // Cellule vide
    }
  };

  // Fonction pour obtenir un texte pour la cellule en fonction de son contenu
  const getCellText = (cellContent: string): string => {

      switch (cellContent) {
      case 'R': return 'R';
      case 'T': return 'T';
      case 'B': return 'B';
      case 'RT': return 'R';
      default: return '';
    }
  };

  // Rendu de la grille
  return (
    <div className="overflow-auto border border-gray-300 rounded">
      <div
        className="grid"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${grid.length}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${grid.length}, ${cellSize}px)`,
          width: `${gridSize}px`,
          height: `${gridSize}px`,
        }}
      >
        {grid.map((row, rowIndex) =>
          row.map((cell, colIndex) => {
            // Trouver si un robot est sur cette cellule (pour afficher s'il porte un déchet)
            const robot = robots.find(r => r.x === rowIndex && r.y === colIndex);
            const isCarryingTrash = robot?.carrying_trash;

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`flex items-center justify-center border border-gray-300 ${getCellColor(cell, robot)}`}
                style={{ width: `${cellSize}px`, height: `${cellSize}px` }}
              >
                {getCellText(cell)}
                {isCarryingTrash && (
                  <span className="ml-1 text-xs text-red-500">*</span>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Grid;