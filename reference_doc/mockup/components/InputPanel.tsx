import React from 'react';
import { FileText, Sparkles, Eraser } from 'lucide-react';

interface InputPanelProps {
  inputText: string;
  setInputText: (text: string) => void;
  onAnalyze: () => void;
  isAnalyzing: boolean;
}

export const InputPanel: React.FC<InputPanelProps> = ({ 
  inputText, 
  setInputText, 
  onAnalyze,
  isAnalyzing 
}) => {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-gray-100 flex justify-between items-center flex-shrink-0">
        <div className="flex items-center gap-2 text-gray-700 font-semibold">
          <FileText size={18} className="text-blue-500" />
          <span>输入内容</span>
        </div>
        <button 
            onClick={() => setInputText('')}
            className="p-2 hover:bg-gray-100 rounded-full text-gray-400 transition-colors"
            title="清空内容"
        >
          <Eraser size={16} />
        </button>
      </div>

      {/* Text Area */}
      <div className="flex-1 p-4 relative flex flex-col min-h-0">
        <textarea
          className="w-full h-full resize-none outline-none text-gray-600 leading-relaxed placeholder-gray-300 text-sm md:text-base bg-transparent p-1"
          placeholder={`输入您想要的可视化内容，可以是步骤说明、对比分析、组织架构等。AI会自动分析并推荐最合适的信息图模板。\n\n例如：\n这里有一个四个阶段的产品开发流程。第一阶段是概念验证，通过率10%；第二阶段是原型开发，通过率30%；第三阶段是市场测试...`}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        
        {/* Floating Action Button */}
        <div className="absolute bottom-6 left-0 right-0 px-6 flex justify-center">
            <button
                onClick={onAnalyze}
                disabled={isAnalyzing || !inputText.trim()}
                className={`
                    flex items-center gap-2 px-6 py-3 rounded-full shadow-lg text-white font-medium transition-all transform hover:scale-105 active:scale-95
                    ${isAnalyzing || !inputText.trim() 
                        ? 'bg-gray-300 cursor-not-allowed' 
                        : 'bg-gradient-to-r from-blue-500 to-purple-500 hover:shadow-blue-200'}
                `}
            >
                {isAnalyzing ? (
                     <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                    <Sparkles size={18} />
                )}
                <span>{isAnalyzing ? '分析中...' : '分析并推荐模版'}</span>
            </button>
        </div>
      </div>
    </div>
  );
};