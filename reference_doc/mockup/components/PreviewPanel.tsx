import React, { useState, useRef, useEffect } from 'react';
import { CheckCircle2, Download, Save, ZoomIn, ZoomOut, Maximize, ChevronDown, Check } from 'lucide-react';
import { InfographicData } from '../types';
import { InfographicRenderer } from './InfographicRenderer';

interface PreviewPanelProps {
  data: InfographicData | null;
}

export const PreviewPanel: React.FC<PreviewPanelProps> = ({ data }) => {
  const [zoom, setZoom] = useState(100);
  const [selectedType, setSelectedType] = useState('横向时间轴');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const chartTypes = [
    '横向时间轴',
    '垂直步骤图',
    'SWOT分析',
    '漏斗图',
    '组织架构图'
  ];

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 10, 200));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 10, 50));
  const handleFit = () => setZoom(100);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 flex flex-col h-full overflow-hidden">
      {/* Header Toolbar */}
      <div className="p-4 border-b border-gray-100 flex flex-col sm:flex-row justify-between items-center gap-4 bg-white z-20 relative flex-shrink-0">
        <div className="flex items-center gap-2 text-gray-700 font-semibold w-full sm:w-auto">
          <CheckCircle2 size={18} className="text-blue-500" />
          <span>信息图预览</span>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
            {/* Interactive Dropdown */}
            <div className="relative" ref={dropdownRef}>
                <button 
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className={`flex items-center gap-2 px-3 py-1.5 text-sm bg-gray-50 border rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-blue-100
                    ${isDropdownOpen ? 'border-blue-400 ring-2 ring-blue-100' : 'border-gray-200 hover:bg-gray-100'}
                  `}
                >
                    <span className="text-gray-500">信息图类型:</span>
                    <span className="text-gray-900 font-medium min-w-[5rem] text-left">{selectedType}</span>
                    <ChevronDown size={14} className={`text-gray-500 transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} />
                </button>
                
                {/* Dropdown Menu */}
                {isDropdownOpen && (
                  <div className="absolute top-full right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50 animate-in fade-in zoom-in-95 duration-100 origin-top-right">
                    <div className="py-1">
                      {chartTypes.map((type) => (
                        <button
                          key={type}
                          onClick={() => {
                            setSelectedType(type);
                            setIsDropdownOpen(false);
                          }}
                          className={`w-full text-left px-4 py-2.5 text-sm flex items-center justify-between hover:bg-gray-50 transition-colors
                            ${selectedType === type ? 'text-blue-600 bg-blue-50 font-medium' : 'text-gray-700'}
                          `}
                        >
                          {type}
                          {selectedType === type && <Check size={14} />}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
            </div>
            
            <button className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 hover:text-blue-600 transition-colors">
                <Download size={14} />
                <span className="hidden sm:inline">导出</span>
            </button>
            <button className="flex items-center gap-1 px-4 py-1.5 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600 shadow-sm shadow-blue-200 transition-colors">
                <Save size={14} />
                <span className="hidden sm:inline">保存</span>
            </button>
        </div>
      </div>

      {/* Canvas Area */}
      <div className="flex-1 bg-gray-50 relative overflow-hidden flex items-center justify-center p-4 md:p-8 min-h-0">
          
          {/* Main Content Container */}
          <div 
            className="transition-transform duration-300 ease-out origin-center bg-white shadow-xl shadow-gray-200/50 rounded-xl p-8 md:p-12 w-full max-w-5xl min-h-[400px] flex items-center justify-center"
            style={{ transform: `scale(${zoom / 100})` }}
          >
              {data ? (
                 <InfographicRenderer data={data} type={selectedType} />
              ) : (
                  <div className="text-center text-gray-400">
                      <div className="w-24 h-24 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                          <Maximize size={32} className="opacity-20" />
                      </div>
                      <p>在左侧输入内容并点击分析<br/>即可生成预览</p>
                  </div>
              )}
          </div>

          {/* Zoom Controls */}
          <div className="absolute bottom-6 right-6 bg-white rounded-full shadow-lg border border-gray-100 p-1 flex items-center gap-1 z-10">
              <button onClick={handleZoomOut} className="p-2 hover:bg-gray-100 rounded-full text-gray-500" title="Zoom Out">
                  <ZoomOut size={16} />
              </button>
              <div className="w-px h-4 bg-gray-200"></div>
              <button onClick={handleFit} className="flex items-center gap-1 px-2 py-1 hover:bg-gray-100 rounded text-xs font-medium text-gray-600" title="Fit to Screen">
                  <Maximize size={12} />
                  <span>适应</span>
              </button>
              <div className="w-px h-4 bg-gray-200"></div>
              <button onClick={handleZoomIn} className="p-2 hover:bg-gray-100 rounded-full text-gray-500" title="Zoom In">
                  <ZoomIn size={16} />
              </button>
          </div>
      </div>
    </div>
  );
};