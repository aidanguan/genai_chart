import { GoogleGenAI, Type, Schema } from "@google/genai";
import { InfographicData } from "../types";

const apiKey = process.env.API_KEY || '';

// Initialize Gemini Client
const ai = new GoogleGenAI({ apiKey });

const infographicSchema: Schema = {
  type: Type.OBJECT,
  properties: {
    title: { type: Type.STRING, description: "A catchy title for the infographic based on the content." },
    subtitle: { type: Type.STRING, description: "A one-sentence summary or subtitle." },
    stages: {
      type: Type.ARRAY,
      description: "Array of 4 to 5 distinct stages/steps identified in the text.",
      items: {
        type: Type.OBJECT,
        properties: {
          name: { type: Type.STRING, description: "Name of the stage (e.g., Introduction, Growth)." },
          description: { type: Type.STRING, description: "Short description of what happens in this stage (max 15 words)." },
          value: { type: Type.STRING, description: "A quantitative or qualitative metric mentioned (e.g. '15% share', 'High cost')." },
          color: { type: Type.STRING, description: "A hex color code suitable for this stage (use a gradient from green to red or distinct colors)." }
        },
        required: ["name", "description", "value", "color"]
      }
    }
  },
  required: ["title", "subtitle", "stages"]
};

export const generateInfographic = async (text: string): Promise<InfographicData | null> => {
  try {
    const prompt = `
      Analyze the following text and structure it into a "Product Lifecycle" or "Process Timeline" visualization data.
      The output must be in Chinese (Simplified) if the input is Chinese.
      Identify 4 to 5 key stages.
      
      Input Text:
      ${text}
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: infographicSchema,
        systemInstruction: "You are an expert data visualization assistant. You extract structured data from unstructured text to build beautiful timeline infographics."
      }
    });

    if (response.text) {
      return JSON.parse(response.text) as InfographicData;
    }
    return null;
  } catch (error) {
    console.error("Gemini API Error:", error);
    throw error;
  }
};
