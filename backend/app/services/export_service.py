"""
导出服务 - 支持SVG、PNG、PDF、PPTX格式导出
"""
import os
import base64
from io import BytesIO
from typing import Optional
from pathlib import Path

# 导出格式常量
EXPORT_FORMAT_SVG = "svg"
EXPORT_FORMAT_PNG = "png"
EXPORT_FORMAT_PDF = "pdf"
EXPORT_FORMAT_PPTX = "pptx"

SUPPORTED_FORMATS = [EXPORT_FORMAT_SVG, EXPORT_FORMAT_PNG, EXPORT_FORMAT_PDF, EXPORT_FORMAT_PPTX]


class ExportService:
    """导出服务类"""
    
    def __init__(self):
        self.temp_dir = Path("temp/exports")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def export_svg(self, svg_content: str, filename: Optional[str] = None) -> dict:
        """
        导出SVG格式
        
        Args:
            svg_content: SVG内容字符串
            filename: 可选的文件名
            
        Returns:
            包含文件信息的字典
        """
        if not filename:
            filename = "infographic.svg"
        
        filepath = self.temp_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return {
            "format": EXPORT_FORMAT_SVG,
            "filename": filename,
            "filepath": str(filepath),
            "size": os.path.getsize(filepath)
        }
    
    def export_png(self, svg_content: str, filename: Optional[str] = None, 
                   width: int = 800, height: int = 600, scale: int = 2) -> dict:
        """
        导出PNG格式
        需要安装: pip install cairosvg
        
        Args:
            svg_content: SVG内容字符串
            filename: 可选的文件名
            width: 输出宽度
            height: 输出高度
            scale: 缩放比例(用于高清输出)
            
        Returns:
            包含文件信息的字典
        """
        try:
            import cairosvg
        except ImportError:
            raise ImportError("PNG导出需要安装cairosvg: pip install cairosvg")
        
        if not filename:
            filename = "infographic.png"
        
        filepath = self.temp_dir / filename
        
        # 转换SVG到PNG
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=str(filepath),
            output_width=width * scale,
            output_height=height * scale
        )
        
        return {
            "format": EXPORT_FORMAT_PNG,
            "filename": filename,
            "filepath": str(filepath),
            "size": os.path.getsize(filepath),
            "width": width * scale,
            "height": height * scale
        }
    
    def export_pdf(self, svg_content: str, filename: Optional[str] = None) -> dict:
        """
        导出PDF格式
        需要安装: pip install cairosvg
        
        Args:
            svg_content: SVG内容字符串
            filename: 可选的文件名
            
        Returns:
            包含文件信息的字典
        """
        try:
            import cairosvg
        except ImportError:
            raise ImportError("PDF导出需要安装cairosvg: pip install cairosvg")
        
        if not filename:
            filename = "infographic.pdf"
        
        filepath = self.temp_dir / filename
        
        # 转换SVG到PDF
        cairosvg.svg2pdf(
            bytestring=svg_content.encode('utf-8'),
            write_to=str(filepath)
        )
        
        return {
            "format": EXPORT_FORMAT_PDF,
            "filename": filename,
            "filepath": str(filepath),
            "size": os.path.getsize(filepath)
        }
    
    def export_pptx(self, svg_content: str, title: str = "信息图", 
                    filename: Optional[str] = None) -> dict:
        """
        导出PPTX格式
        需要安装: pip install python-pptx cairosvg
        
        Args:
            svg_content: SVG内容字符串
            title: 幻灯片标题
            filename: 可选的文件名
            
        Returns:
            包含文件信息的字典
        """
        try:
            from pptx import Presentation
            from pptx.util import Inches
            import cairosvg
        except ImportError:
            raise ImportError("PPTX导出需要安装: pip install python-pptx cairosvg")
        
        if not filename:
            filename = "infographic.pptx"
        
        # 首先将SVG转换为PNG
        png_buffer = BytesIO()
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=png_buffer,
            output_width=1920,  # 高清输出
            output_height=1080
        )
        png_buffer.seek(0)
        
        # 创建PowerPoint演示文稿
        prs = Presentation()
        
        # 设置幻灯片尺寸为16:9
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # 添加空白幻灯片
        blank_slide_layout = prs.slide_layouts[6]  # 空白布局
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # 添加标题
        if title:
            txBox = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.3), 
                Inches(9), Inches(0.5)
            )
            tf = txBox.text_frame
            tf.text = title
            p = tf.paragraphs[0]
            p.font.size = Inches(0.3)
            p.font.bold = True
        
        # 添加图片
        left = Inches(0.5)
        top = Inches(1)
        width = Inches(9)
        slide.shapes.add_picture(png_buffer, left, top, width=width)
        
        # 保存文件
        filepath = self.temp_dir / filename
        prs.save(str(filepath))
        
        return {
            "format": EXPORT_FORMAT_PPTX,
            "filename": filename,
            "filepath": str(filepath),
            "size": os.path.getsize(filepath)
        }
    
    def export(self, svg_content: str, format: str, **kwargs) -> dict:
        """
        统一导出接口
        
        Args:
            svg_content: SVG内容字符串
            format: 导出格式 (svg/png/pdf/pptx)
            **kwargs: 格式特定的参数
            
        Returns:
            包含文件信息的字典
        """
        if format not in SUPPORTED_FORMATS:
            raise ValueError(f"不支持的导出格式: {format}. 支持的格式: {SUPPORTED_FORMATS}")
        
        if format == EXPORT_FORMAT_SVG:
            return self.export_svg(svg_content, **kwargs)
        elif format == EXPORT_FORMAT_PNG:
            return self.export_png(svg_content, **kwargs)
        elif format == EXPORT_FORMAT_PDF:
            return self.export_pdf(svg_content, **kwargs)
        elif format == EXPORT_FORMAT_PPTX:
            return self.export_pptx(svg_content, **kwargs)
    
    def get_base64(self, filepath: str) -> str:
        """
        将文件转换为base64编码
        
        Args:
            filepath: 文件路径
            
        Returns:
            base64编码的字符串
        """
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def cleanup(self, filepath: str):
        """
        清理临时文件
        
        Args:
            filepath: 要删除的文件路径
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"清理文件失败: {e}")


# 单例实例
_export_service = None


def get_export_service() -> ExportService:
    """获取导出服务实例"""
    global _export_service
    if _export_service is None:
        _export_service = ExportService()
    return _export_service
