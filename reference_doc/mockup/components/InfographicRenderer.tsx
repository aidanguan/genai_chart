import React from 'react';
import { InfographicData } from '../types';

interface Props {
  data: InfographicData;
  type?: string;
}

export const InfographicRenderer: React.FC<Props> = ({ data, type = '横向时间轴' }) => {
  const isVertical = type === '垂直步骤图' || type === '组织架构图';

  return (
    <div className="w-full h-full flex flex-col items-center">
      {/* Title Section */}
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-800 mb-2 tracking-tight">
          {data.title}
        </h2>
        <p className="text-gray-500 font-medium">
          {data.subtitle}
        </p>
      </div>

      {/* Chart Visualization */}
      <div className={`w-full flex ${isVertical ? 'flex-col items-center gap-8' : 'flex-col md:flex-row items-end justify-center gap-4'} relative mt-6`}>
        
        {data.stages.map((stage, index) => {
          
          // Different layout for vertical mode
          if (isVertical) {
             return (
               <div key={index} className="flex items-center gap-6 w-full max-w-2xl relative">
                  {/* Vertical Connector Line */}
                  {index < data.stages.length - 1 && (
                    <div 
                      className="absolute left-[24px] top-12 bottom-[-32px] w-1 bg-gray-200"
                    ></div>
                  )}

                  <div 
                    className="w-12 h-12 rounded-full flex items-center justify-center shrink-0 z-10 shadow-md text-white font-bold"
                    style={{ backgroundColor: stage.color }}
                  >
                    {index + 1}
                  </div>
                  
                  <div className="flex-1 bg-gray-50 p-4 rounded-xl border border-gray-100 hover:shadow-md transition-shadow">
                     <div className="flex justify-between items-center mb-1">
                        <h3 className="text-lg font-bold text-gray-800">{stage.name}</h3>
                        <span className="text-sm font-bold px-2 py-1 rounded bg-white text-gray-600">{stage.value}</span>
                     </div>
                     <p className="text-sm text-gray-500">{stage.description}</p>
                  </div>
               </div>
             );
          }

          // Default Horizontal Layout
          return (
            <div key={index} className="flex-1 min-w-[150px] relative group">
              
              {/* Top Text (Description) */}
              <div className={`mb-4 px-2 ${index > 0 ? 'md:mt-[-20px]' : ''}`}>
                 <h4 className="text-gray-500 text-sm font-medium leading-snug mb-1">{stage.description}</h4>
                 <div className="font-bold text-2xl text-gray-800">{stage.value}</div>
              </div>

              {/* The "Bar" / Visual Element */}
              <div className="relative">
                 {/* Connection Triangle (Arrow head effect) */}
                 {index < data.stages.length - 1 && (
                     <div 
                        className="hidden md:block absolute -right-6 top-0 z-10 w-0 h-0 border-t-[12px] border-t-transparent border-l-[16px] border-b-[12px] border-b-transparent"
                        style={{ borderLeftColor: stage.color }}
                     />
                 )}
                 
                 {/* Main Color Block */}
                 <div 
                    className="h-3 w-full rounded-sm shadow-sm transition-all duration-500 hover:h-4"
                    style={{ backgroundColor: stage.color }}
                 ></div>

                 {/* Vertical Connector Line (Design choice from screenshot) */}
                 <div 
                    className="absolute left-0 bottom-3 w-2 bg-gradient-to-t from-gray-100 to-transparent"
                    style={{ 
                        height: `${(index + 1) * 40}px`, 
                        backgroundColor: stage.color,
                        opacity: 0.2
                    }}
                 ></div>
                 
                 {/* Main Stage Label Block (Bottom) */}
                 <div className="mt-4">
                     <h3 className="text-xl font-bold text-gray-800">{stage.name}</h3>
                 </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};