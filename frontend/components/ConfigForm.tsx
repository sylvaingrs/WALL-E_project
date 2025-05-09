import React, { useState } from 'react';
import { SimulationConfig } from '@/lib/api';

interface ConfigFormProps {
  onSubmit: (config: SimulationConfig) => void;
  isRunning: boolean;
}

const ConfigForm: React.FC<ConfigFormProps> = ({ onSubmit, isRunning }) => {
  const [config, setConfig] = useState<SimulationConfig>({
    num_robots: 4,
    num_trash: 20,
    base_x: 0,
    base_y: 0
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: parseInt(value)
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(config);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white rounded shadow">
      <h2 className="mb-4 text-xl font-bold">Configuration de la simulation</h2>

      <div className="mb-4">
        <label className="block mb-2 text-sm font-medium">
          Nombre de robots:
          <input
            type="number"
            name="num_robots"
            min="1"
            max="20"
            value={config.num_robots}
            onChange={handleChange}
            className="w-full p-2 mt-1 border rounded"
            disabled={isRunning}
          />
        </label>
      </div>

      <div className="mb-4">
        <label className="block mb-2 text-sm font-medium">
          Nombre de déchets:
          <input
            type="number"
            name="num_trash"
            min="1"
            max="400"
            value={config.num_trash}
            onChange={handleChange}
            className="w-full p-2 mt-1 border rounded"
            disabled={isRunning}
          />
        </label>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <label className="block mb-2 text-sm font-medium">
          Position X de la base:
          <input
            type="number"
            name="base_x"
            min="0"
            max="31"
            value={config.base_x}
            onChange={handleChange}
            className="w-full p-2 mt-1 border rounded"
            disabled={isRunning}
          />
        </label>

        <label className="block mb-2 text-sm font-medium">
          Position Y de la base:
          <input
            type="number"
            name="base_y"
            min="0"
            max="31"
            value={config.base_y}
            onChange={handleChange}
            className="w-full p-2 mt-1 border rounded"
            disabled={isRunning}
          />
        </label>
      </div>

      <button
        type="submit"
        className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600 disabled:bg-gray-400"
        disabled={isRunning}
      >
        {isRunning ? 'Simulation en cours...' : 'Démarrer la simulation'}
      </button>
    </form>
  );
};

export default ConfigForm;