"""
相似度计算服务
计算用户文本与模板的匹配度，用于模板排序
"""
import logging
from typing import List, Dict, Any
import re

logger = logging.getLogger(__name__)


class SimilarityService:
    """相似度计算服务"""
    
    def __init__(self):
        """初始化相似度计算服务"""
        # 分类权重映射
        self.category_keywords = {
            'chart': ['数据', '统计', '图表', '增长', '百分比', '比例', '指标', 'KPI'],
            'comparison': ['对比', '比较', '优劣', 'SWOT', '优势', '劣势', '差异'],
            'hierarchy': ['层级', '组织', '架构', '分类', '等级', '结构'],
            'list': ['列表', '步骤', '清单', '要点', '特点', '功能'],
            'quadrant': ['四象限', '矩阵', '定位', '分布', '维度'],
            'relation': ['关系', '网络', '关联', '连接', '因果', '流程'],
            'sequence': ['时间', '流程', '步骤', '阶段', '顺序', '递进']
        }
    
    def calculate_all_templates_similarity(
        self,
        user_text: str,
        templates: List[Dict[str, Any]],
        content_type: str = None,
        selected_template_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        计算所有模板的相似度并排序
        
        Args:
            user_text: 用户输入文本
            templates: 模板列表
            content_type: 识别的内容类型（可选）
            selected_template_id: 选中的模板ID（该模板相似度自动设为100%）
        
        Returns:
            List[Dict]: 带相似度的模板列表，按相似度降序排列
        """
        template_scores = []
        
        for template in templates:
            template_id = template.get('id')
            
            # 选中的模板相似度固定为100%
            if template_id == selected_template_id:
                similarity_score = 1.0
                reason = "AI推荐模板" if content_type else "用户选择的模板"
            else:
                # 计算相似度
                similarity_score = self._calculate_similarity(
                    user_text=user_text,
                    template=template,
                    content_type=content_type
                )
                reason = self._generate_reason(
                    template=template,
                    similarity_score=similarity_score,
                    content_type=content_type
                )
            
            template_scores.append({
                'templateId': template_id,
                'templateName': template.get('name', ''),
                'category': template.get('category', ''),
                'similarityScore': round(similarity_score, 2),
                'reason': reason
            })
        
        # 排序：相似度降序
        template_scores.sort(key=lambda x: x['similarityScore'], reverse=True)
        
        return template_scores
    
    def _calculate_similarity(
        self,
        user_text: str,
        template: Dict[str, Any],
        content_type: str = None
    ) -> float:
        """
        计算单个模板的相似度
        
        维度：
        - 类型匹配度：30%
        - 关键词相似度：25%
        - 语义相似度：25%
        - 结构匹配度：20%
        """
        # 1. 类型匹配度（30%）
        type_score = self._calculate_type_match(template, content_type)
        
        # 2. 关键词相似度（25%）
        keyword_score = self._calculate_keyword_similarity(user_text, template)
        
        # 3. 语义相似度（25%）
        semantic_score = self._calculate_semantic_similarity(user_text, template)
        
        # 4. 结构匹配度（20%）
        structure_score = self._calculate_structure_match(user_text, template)
        
        # 综合得分
        final_score = (
            type_score * 0.3 +
            keyword_score * 0.25 +
            semantic_score * 0.25 +
            structure_score * 0.2
        )
        
        return min(final_score, 1.0)
    
    def _calculate_type_match(
        self,
        template: Dict[str, Any],
        content_type: str = None
    ) -> float:
        """计算类型匹配度"""
        if not content_type:
            return 0.5  # 无类型信息时返回中等分数
        
        template_category = template.get('category', '')
        
        # 完全匹配
        if template_category == content_type:
            return 1.0
        
        # 部分匹配（相关分类）
        related_types = {
            'list': ['sequence', 'hierarchy'],
            'sequence': ['list', 'relation'],
            'hierarchy': ['list', 'relation'],
            'comparison': ['quadrant'],
            'quadrant': ['comparison'],
            'relation': ['sequence', 'hierarchy'],
            'chart': []
        }
        
        if template_category in related_types.get(content_type, []):
            return 0.6
        
        return 0.3
    
    def _calculate_keyword_similarity(
        self,
        user_text: str,
        template: Dict[str, Any]
    ) -> float:
        """计算关键词相似度"""
        user_text_lower = user_text.lower()
        
        # 模板标签
        template_tags = template.get('tags', [])
        if not template_tags:
            template_tags = []
        
        # 模板分类关键词
        category = template.get('category', '')
        category_keywords = self.category_keywords.get(category, [])
        
        # 计算命中的关键词数量
        matched_count = 0
        total_keywords = len(template_tags) + len(category_keywords)
        
        if total_keywords == 0:
            return 0.5
        
        for tag in template_tags:
            if tag.lower() in user_text_lower:
                matched_count += 1
        
        for keyword in category_keywords:
            if keyword in user_text:
                matched_count += 1
        
        return min(matched_count / total_keywords, 1.0)
    
    def _calculate_semantic_similarity(
        self,
        user_text: str,
        template: Dict[str, Any]
    ) -> float:
        """
        计算语义相似度
        基于模板描述和适用场景与用户文本的匹配
        """
        description = template.get('description', '')
        use_cases = template.get('useCases', '')
        
        # 简单基于关键词重合的语义相似度
        template_text = f"{description} {use_cases}".lower()
        user_text_lower = user_text.lower()
        
        # 提取用户文本中的关键词（简单分词）
        user_words = set(re.findall(r'\w+', user_text_lower))
        template_words = set(re.findall(r'\w+', template_text))
        
        if not template_words:
            return 0.5
        
        # 计算交集
        common_words = user_words & template_words
        similarity = len(common_words) / max(len(template_words), 1)
        
        return min(similarity * 2, 1.0)  # 放大系数
    
    def _calculate_structure_match(
        self,
        user_text: str,
        template: Dict[str, Any]
    ) -> float:
        """
        计算结构匹配度
        基于文本中的数据项数量与模板适合的数据规模
        """
        # 检测文本中的数据项数量
        item_count = self._estimate_item_count(user_text)
        
        # 根据模板ID判断适合的数据规模
        template_id = template.get('id', '')
        
        # 定义模板适合的数据项范围
        if 'row' in template_id or 'column' in template_id:
            ideal_range = (2, 4)
        elif 'grid' in template_id:
            ideal_range = (4, 9)
        elif 'list' in template_id:
            ideal_range = (3, 10)
        elif 'steps' in template_id or 'timeline' in template_id:
            ideal_range = (3, 7)
        elif 'pyramid' in template_id or 'hierarchy' in template_id:
            ideal_range = (3, 6)
        else:
            ideal_range = (2, 8)
        
        # 计算匹配度
        min_items, max_items = ideal_range
        
        if min_items <= item_count <= max_items:
            return 1.0
        elif item_count < min_items:
            return 0.5 + (item_count / min_items) * 0.5
        else:
            return 0.5 + (max_items / item_count) * 0.5
    
    def _estimate_item_count(self, user_text: str) -> int:
        """估计文本中的数据项数量"""
        # 检测常见的列表标识符
        patterns = [
            r'\d+[.、．]',  # 1. 2. 3. 或 1、2、3、
            r'[一二三四五六七八九十]+[.、．]',  # 一、二、三、
            r'第[一二三四五六七八九十\d]+',  # 第一、第二
            r'[\n；;]+',  # 换行或分号分隔
        ]
        
        max_count = 0
        for pattern in patterns:
            matches = re.findall(pattern, user_text)
            max_count = max(max_count, len(matches))
        
        # 如果没有明显的列表标识，按逗号、顿号分割
        if max_count == 0:
            separators = user_text.count('、') + user_text.count('，')
            max_count = max(separators + 1, 3)
        
        return min(max_count, 20)  # 限制最大值
    
    def _generate_reason(
        self,
        template: Dict[str, Any],
        similarity_score: float,
        content_type: str = None
    ) -> str:
        """生成推荐理由"""
        template_name = template.get('name', '')
        category = template.get('category', '')
        
        if similarity_score >= 0.8:
            return f"与{content_type if content_type else '输入内容'}高度匹配，适合{category}类型展示"
        elif similarity_score >= 0.6:
            return f"较适合展示{category}类型内容"
        elif similarity_score >= 0.4:
            return f"可用于展示{category}类型内容"
        else:
            return f"{template_name}可作为备选"


# 全局实例
_similarity_service_instance = None


def get_similarity_service() -> SimilarityService:
    """获取相似度计算服务单例"""
    global _similarity_service_instance
    if _similarity_service_instance is None:
        _similarity_service_instance = SimilarityService()
    return _similarity_service_instance
