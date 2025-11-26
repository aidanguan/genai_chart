import React from 'react';
import { Hexagon, User } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="w-full bg-white shadow-sm border-b border-gray-100 px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg flex items-center justify-center text-white">
          <Hexagon size={20} fill="currentColor" />
        </div>
        <span className="text-xl font-bold tracking-tight text-gray-800">
          GRAPHIC<span className="text-purple-500">MAKER</span>
        </span>
      </div>
      
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-orange-300 to-yellow-300 flex items-center justify-center overflow-hidden border border-gray-200">
           {/* Placeholder Avatar */}
           <img src="https://picsum.photos/100/100" alt="User" className="w-full h-full object-cover opacity-80" />
        </div>
        <span className="text-sm font-medium text-gray-600">Aidan</span>
      </div>
    </header>
  );
};
