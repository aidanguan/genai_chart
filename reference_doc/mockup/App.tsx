import React, { useState } from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { InputPanel } from './components/InputPanel';
import { PreviewPanel } from './components/PreviewPanel';
import { generateInfographic } from './services/geminiService';
import { InfographicData } from './types';

// Default mock data matching the screenshot for initial state
const DEFAULT_DATA: InfographicData = {
  title: "产品生命周期与市场份额变化",
  subtitle: "通过不同阶段的策略调整，实现市场份额的稳步增长与平稳过渡。",
  stages: [
    {
      name: "导入期",
      description: "产品刚进入市场，销量较低",
      value: "市场份额约 5%",
      color: "#6aa84f" // Green
    },
    {
      name: "成长期",
      description: "销量快速攀升，加大营销投入",
      value: "份额增长至 25%",
      color: "#f1c232" // Yellow
    },
    {
      name: "成熟期",
      description: "市场份额达到峰值，优化成本结构",
      value: "份额高达 40%",
      color: "#e69138" // Orange
    },
    {
      name: "衰退期",
      description: "市场份额下滑，及时推出升级产品",
      value: "下滑至 15%",
      color: "#cc4125" // Red
    }
  ]
};

const App: React.FC = () => {
  const [inputText, setInputText] = useState("");
  const [chartData, setChartData] = useState<InfographicData | null>(DEFAULT_DATA);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;

    setIsAnalyzing(true);
    try {
      const data = await generateInfographic(inputText);
      if (data) {
        setChartData(data);
      }
    } catch (error) {
      console.error("Failed to generate infographic", error);
      alert("Analysis failed. Please try again with a valid API Key.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="h-full flex flex-col bg-[#f3f6fc] text-gray-800 font-sans overflow-hidden">
      <Header />
      
      {/* Main Content Area - Flex 1 to take remaining height */}
      <main className="flex-1 flex flex-col min-h-0 w-full max-w-[1600px] mx-auto p-3 md:p-4 gap-3">
        
        {/* Compact Hero that doesn't take too much vertical space */}
        <div className="flex-shrink-0">
          <Hero />
        </div>
        
        {/* Workspace Grid - Takes remaining height with flex-1 */}
        <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-12 gap-3 md:gap-4 h-full">
          {/* Left Panel - Input */}
          <div className="lg:col-span-4 xl:col-span-3 h-full min-h-0">
             <InputPanel 
                inputText={inputText}
                setInputText={setInputText}
                onAnalyze={handleAnalyze}
                isAnalyzing={isAnalyzing}
             />
          </div>

          {/* Right Panel - Preview */}
          <div className="lg:col-span-8 xl:col-span-9 h-full min-h-0">
            <PreviewPanel data={chartData} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;