import React from 'react';
import { Bot } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <div className="w-full flex flex-col md:flex-row items-center justify-between py-2 px-2">
      <div className="flex-1 space-y-2">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800 flex items-center gap-3">
            <div className="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center shadow-lg text-white">
                 <span className="text-xl font-bold">G</span>
            </div>
            GRAPHIC<span className="text-purple-500">MAKER</span>
        </h1>
        <p className="text-gray-500 text-xs md:text-sm max-w-xl leading-relaxed">
          将你在日常写作、汇报或其他文字工作中遇到的内容粘贴到这里，AI 会理解语境并为你生成相匹配的信息图方案
        </p>
      </div>
      
      {/* Decorative Robot/AI Illustration placeholder */}
      <div className="hidden md:flex items-center justify-center relative w-48 h-20 opacity-80">
         <div className="absolute inset-0 bg-blue-100 rounded-full blur-3xl opacity-40"></div>
         <Bot size={50} className="text-blue-500 relative z-10" />
         <div className="absolute top-0 right-10 w-3 h-3 bg-purple-400 rounded-full animate-bounce"></div>
         <div className="absolute bottom-4 left-10 w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
      </div>
    </div>
  );
};