"""
生成服务
处理信息图生成相关逻辑（三阶段流程）
支持Dify工作流和系统LLM两种数据生成方式
"""
import logging
import time
from typing import Dict, Any, Optional
from app.services.llm_client import get_llm_client
from app.services.template_service import get_template_service
from app.services.type_classification_service import get_type_classification_service
from app.services.template_selection_service import get_template_selection_service
from app.services.dify_workflow_client import get_dify_workflow_client
from app.services.workflow_mapper import get_workflow_mapper
from app.services.data_validator import get_data_validator
from app.services.config_assembler import get_config_assembler
from app.services.similarity_service import get_similarity_service

logger = logging.getLogger(__name__)

# 结构类型映射表：将不支持的类型映射到可用的模板
STRUCTURE_TYPE_FALLBACK_MAP = {
    # 时间轴类型 -> 横向流程图
    "timeline-horizontal": "list-row-horizontal-icon-arrow",
    # 双栏对比 -> 简单列表（展示两组数据）
    "comparison-column": "list-column-simple",
    # SWOT四象限 -> 金字塔层级图（展示4个维度）
    "quadrant-swot": "pyramid-layer",
    # 放射状思维导图 -> 组织架构树
    "mindmap-radial": "org-tree"
}


class GenerateService:
    """生成服务类"""
    
    def __init__(self):
        """初始化生成服务"""
        self.llm_client = get_llm_client()
        self.template_service = get_template_service()
        self.type_classification_service = get_type_classification_service()
        self.template_selection_service = get_template_selection_service()
        self.dify_client = get_dify_workflow_client()
        self.workflow_mapper = get_workflow_mapper()
        self.data_validator = get_data_validator()
        self.config_assembler = get_config_assembler()
        self.similarity_service = get_similarity_service()
    
    async def generate_smart(
        self,
        user_text: str,
        include_all_templates: bool = False
    ) -> Dict[str, Any]:
        """
        智能生成流程（三阶段）
        1. 类型识别
        2. 模板选择
        3. 数据提取
        
        Args:
            user_text: 用户输入的文本
            include_all_templates: 是否返回所有模板列表（带相似度排序）
        
        Returns:
            Dict: 包含配置对象、分类信息、模板信息、时间统计和allTemplates（可选）
        """
        start_time = time.time()
        
        try:
            logger.info(f"[SmartGenerate] 开始智能生成流程 - 文本长度: {len(user_text)}")
            
            # 阶段1: 类型识别
            phase1_start = time.time()
            classification_result = await self.type_classification_service.classify(user_text)
            content_type = classification_result['type']
            phase1_time = round(time.time() - phase1_start, 2)
            logger.info(f"[SmartGenerate] 阶段1完成 - 类型: {content_type}, 耗时: {phase1_time}s")
            
            # 阶段2: 模板选择
            phase2_start = time.time()
            selection_result = await self.template_selection_service.select(user_text, content_type)
            template_id = selection_result['templateId']
            phase2_time = round(time.time() - phase2_start, 2)
            logger.info(f"[SmartGenerate] 阶段2完成 - 模板: {template_id}, 耗时: {phase2_time}s")
            
            # 阶段3: 数据提取（尝试使用Dify工作流，失败则回退到系统LLM）
            phase3_start = time.time()
            extraction_result = await self.extract_data(user_text, template_id)
            phase3_time = round(time.time() - phase3_start, 2)
            logger.info(f"[SmartGenerate] 阶段3完成 - 耗时: {phase3_time}s")
            
            total_time = round(time.time() - start_time, 2)
            
            # 构建返回结果
            result = {
                "config": extraction_result['config'],
                "classification": {
                    "type": content_type,
                    "confidence": classification_result['confidence'],
                    "reason": classification_result['reason']
                },
                "selection": {
                    "templateId": template_id,
                    "templateName": selection_result['templateName'],
                    "confidence": selection_result['confidence'],
                    "reason": selection_result['reason']
                },
                "timing": {
                    "phase1_classification": phase1_time,
                    "phase2_selection": phase2_time,
                    "phase3_extraction": phase3_time,
                    "total": total_time
                },
                "generation_method": extraction_result.get('generation_method', 'system_llm')
            }
            
            # 如果使用了Dify工作流，添加工作流信息
            if 'workflow_info' in extraction_result:
                result['workflow_info'] = extraction_result['workflow_info']
                result['timing']['dify_call_time'] = extraction_result.get('dify_call_time', 0)
            
            # 如果需要返回所有模板列表
            if include_all_templates:
                all_templates_result = self.template_service.get_all_templates(page=1, page_size=100)
                all_templates = all_templates_result.get("templates", [])
                
                # 计算相似度并排序
                templates_with_similarity = self.similarity_service.calculate_all_templates_similarity(
                    user_text=user_text,
                    templates=all_templates,
                    content_type=content_type,
                    selected_template_id=template_id
                )
                
                result['allTemplates'] = templates_with_similarity
            
            return result
            
        except Exception as e:
            logger.error(f"[SmartGenerate] 智能生成失败: {e}")
            raise
    
    async def recommend_templates(
        self,
        user_text: str,
        max_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        推荐模板
        
        Args:
            user_text: 用户输入的文本
            max_recommendations: 最多推荐数量
        
        Returns:
            Dict: 包含推荐结果和分析时间
        """
        start_time = time.time()
        
        # 获取所有可用模板
        result = self.template_service.get_all_templates(page=1, page_size=100)
        available_templates = result.get("templates", [])
        
        # 调用LLM推荐
        recommendations = await self.llm_client.recommend_templates(
            user_text=user_text,
            available_templates=available_templates,
            max_recommendations=max_recommendations
        )
        
        analysis_time = round(time.time() - start_time, 2)
        
        return {
            "recommendations": recommendations,
            "analysisTime": analysis_time
        }
    
    async def extract_data(
        self,
        user_text: str,
        template_id: str,
        force_provider: Optional[str] = None,
        include_all_templates: bool = False
    ) -> Dict[str, Any]:
        """
        提取结构化数据
        优先尝试使用Dify工作流，失败则回退到系统LLM
        
        Args:
            user_text: 用户输入的文本
            template_id: 模板ID
            force_provider: 强制使用的提供商 ('system' 或 'dify')，None表示自动选择
            include_all_templates: 是否返回所有模板列表（带相似度排序）
        
        Returns:
            Dict: {
                "config": 完整配置对象,
                "extractionTime": 提取耗时,
                "generation_method": "dify_workflow" 或 "system_llm",
                "workflow_info": {...},  # 如果使用Dify
                "selectedTemplate": {...},  # 选中的模板信息
                "allTemplates": [...]  # 所有模板列表（可选）
            }
        """
        start_time = time.time()
        
        # 获取模板信息
        template = self.template_service.get_template_by_id(template_id)
        if not template:
            raise ValueError(f"模板ID不存在: {template_id}")
        
        # 如果强制指定使用系统LLM
        if force_provider == 'system':
            logger.info(f"[ExtractData] 用户强制使用系统LLM - 模板: {template_id}")
            result = await self._extract_data_with_system_llm(
                user_text=user_text,
                template_id=template_id,
                template=template
            )
            extraction_time = round(time.time() - start_time, 2)
            result['extractionTime'] = extraction_time
            return result
        
        # 如果强制指定使用Dify
        if force_provider == 'dify':
            logger.info(f"[ExtractData] 用户强制使用Dify工作流 - 模板: {template_id}")
            try:
                result = await self._extract_data_with_dify(
                    user_text=user_text,
                    template_id=template_id,
                    template=template
                )
                extraction_time = round(time.time() - start_time, 2)
                result['extractionTime'] = extraction_time
                return result
            except Exception as e:
                logger.error(f"[ExtractData] Dify工作流调用失败: {e}")
                # 强制使用Dify时失败则直接抛出异常，不回退
                raise ValueError(f"Dify工作流调用失败: {str(e)}")
        
        # 自动选择：检查是否启用了Dify工作流
        workflow_enabled = self.workflow_mapper.is_workflow_enabled(template_id)
        logger.info(f"[ExtractData] 模板{template_id}工作流启用状态: {workflow_enabled}")
        
        if workflow_enabled:
            logger.info(f"[ExtractData] 模板{template_id}已启用Dify工作流，尝试调用")
            
            try:
                # 尝试使用Dify工作流生成数据
                result = await self._extract_data_with_dify(
                    user_text=user_text,
                    template_id=template_id,
                    template=template
                )
                
                extraction_time = round(time.time() - start_time, 2)
                result['extractionTime'] = extraction_time
                return result
                
            except Exception as e:
                logger.error(f"[ExtractData] Dify工作流调用失败: {e}")
                
                # 检查是否应回退到系统LLM
                if self.workflow_mapper.should_fallback_to_llm(template_id):
                    logger.info(f"[ExtractData] 回退到系统LLM数据提取")
                else:
                    # 不允许回退，直接抛出异常
                    raise
        
        # 使用系统LLM提取数据
        logger.info(f"[ExtractData] 使用系统LLM提取数据 - 模板: {template_id}")
        result = await self._extract_data_with_system_llm(
            user_text=user_text,
            template_id=template_id,
            template=template
        )
        
        extraction_time = round(time.time() - start_time, 2)
        result['extractionTime'] = extraction_time
        
        # 添加选中的模板信息
        result['selectedTemplate'] = {
            "templateId": template_id,
            "templateName": template.get('name', ''),
            "category": template.get('category', '')
        }
        
        # 如果需要返回所有模板列表
        if include_all_templates:
            all_templates_result = self.template_service.get_all_templates(page=1, page_size=100)
            all_templates = all_templates_result.get("templates", [])
            
            # 计算相似度并排序
            templates_with_similarity = self.similarity_service.calculate_all_templates_similarity(
                user_text=user_text,
                templates=all_templates,
                content_type=None,  # 手工选择模式下没有类型识别
                selected_template_id=template_id
            )
            
            result['allTemplates'] = templates_with_similarity
        
        return result
    
    async def _extract_data_with_dify(
        self,
        user_text: str,
        template_id: str,
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        使用Dify工作流提取数据
        
        Args:
            user_text: 用户输入文本
            template_id: 模板ID
            template: 模板对象
        
        Returns:
            Dict: 包含config和workflow_info
        """
        # 调用Dify工作流
        dify_result = await self.dify_client.call_workflow(
            user_text=user_text,
            template_id=template_id
        )
        
        workflow_data = dify_result['data']
        
        # 数据校验
        template_schema = template.get('dataSchema', {})
        validation_result = self.data_validator.validate_against_schema(
            data=workflow_data,
            schema=template_schema,
            template_id=template_id
        )
        
        if not validation_result['valid']:
            errors = validation_result['errors']
            logger.warning(f"[Dify] 数据校验失败: {errors}")
            # 即使校验失败，也尝试使用修复后的数据
            workflow_data = validation_result['data']
        
        # 获取design配置
        design_config = template.get('designConfig', {})
        
        # 拼接完整配置
        config = self.config_assembler.assemble_config(
            data=workflow_data,
            design_config=design_config,
            template_id=template_id
        )
        
        return {
            "config": config,
            "generation_method": "dify_workflow",
            "workflow_info": {
                "workflow_run_id": dify_result.get('workflow_run_id'),
                "workflow_name": self.workflow_mapper.get_workflow_name(template_id)
            },
            "dify_call_time": dify_result.get('response_time', 0)
        }
    
    async def _extract_data_with_system_llm(
        self,
        user_text: str,
        template_id: str,
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        使用系统LLM提取数据（原有逻辑）
        
        Args:
            user_text: 用户输入文本
            template_id: 模板ID
            template: 模板对象
        
        Returns:
            Dict: 包含config
        """
        # 获取模板Schema
        template_schema = template.get("dataSchema", {})
        
        # 调用LLM提取数据
        extracted_data = await self.llm_client.extract_structured_data(
            user_text=user_text,
            template_id=template_id,
            template_schema=template_schema
        )
        
        # 如果是组织架构树,需要将数据转换为树形结构
        if template_id == 'org-tree':
            extracted_data = self._convert_to_tree_data(extracted_data)
        
        # 如果是对比型模板(compare-binary-horizontal),需要将数据转换为两层结构
        if template_id in ['compare-binary-vs', 'compare-binary-horizontal', 'comparison-two-column'] or \
           (template.get('category') == 'comparison' and 'compare' in template_id):
            extracted_data = self._convert_to_comparison_structure(extracted_data)
        
        # 获取AntV模板配置映射
        from app.services.template_service import TEMPLATE_DESIGN_MAP
        template_design = TEMPLATE_DESIGN_MAP.get(template_id)
        
        # 如果映射中不存在，尝试从模板对象中获取
        if not template_design:
            template_design = template.get("designConfig", {})
        
        # 检查是否需要结构类型转换
        final_template_design = self._convert_structure_type(template_design, template_id)
        
        # 构建完整的AntV Infographic配置
        config = {
            **final_template_design,
            "data": extracted_data.get("data", {}),
            "themeConfig": extracted_data.get("themeConfig", {"palette": "antv"})
        }
        
        logger.info(f"Generated config for template {template_id}: {config}")
        
        return {
            "config": config,
            "generation_method": "system_llm"
        }
    
    def _convert_structure_type(self, template_design: Dict[str, Any], template_id: str) -> Dict[str, Any]:
        """
        转换不支持的结构类型到可用的模板
        
        Args:
            template_design: 原始模板设计配置
            template_id: 模板ID
        
        Returns:
            Dict: 转换后的设计配置
        """
        # 如果已经是template格式，直接返回
        if "template" in template_design:
            return template_design
        
        # 检查是否有design.structure.type
        if "design" in template_design and "structure" in template_design["design"]:
            structure_type = template_design["design"]["structure"].get("type")
            
            # 如果结构类型在fallback映射中，进行转换
            if structure_type in STRUCTURE_TYPE_FALLBACK_MAP:
                fallback_template = STRUCTURE_TYPE_FALLBACK_MAP[structure_type]
                logger.info(f"结构类型 '{structure_type}' 不支持，转换为模板 '{fallback_template}'")
                return {"template": fallback_template}
        
        # 如果没有找到需要转换的情况，返回原配置
        return template_design
    
    def _convert_to_tree_data(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将扫平的items数组转换为树形结构
        
        Args:
            extracted_data: 原始提取数据，包含 items 数组
        
        Returns:
            Dict: 转换为树形结构的数据
        """
        data = extracted_data.get('data', {})
        items = data.get('items', [])
        
        if not items:
            return extracted_data
        
        # 简单的层级关系转换：将第一个作为根节点，其余作为子节点
        # 更复杂的层级关系需要更高级的解析
        root_item = items[0]
        children_items = items[1:] if len(items) > 1 else []
        
        # 转换子节点 - 使用 label 和 desc 字段（AntV Infographic 标准字段）
        children = []
        for item in children_items:
            child_node = {
                "label": item.get('label', ''),
                "desc": item.get('desc', ''),
            }
            # 如果有icon，保留
            if 'icon' in item:
                child_node['icon'] = item['icon']
            children.append(child_node)
        
        # 构建树形结构 - 使用 label 和 desc 字段
        tree_data = {
            "title": data.get('title', ''),
            "desc": data.get('desc', ''),
            "items": [
                {
                    "label": root_item.get('label', ''),
                    "desc": root_item.get('desc', ''),
                    "icon": root_item.get('icon'),
                    "children": children
                }
            ]
        }
        
        return {
            "data": tree_data,
            "themeConfig": extracted_data.get('themeConfig', {})
        }
    
    def _convert_to_comparison_structure(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将扫平的items数组转换为对比型所需的两层结构
        
        对比型需要的数据结构：
        {
          "items": [
            {
              "label": "左侧标题",
              "children": [{"label": "...", "desc": "...", "icon": "..."}]
            },
            {
              "label": "右侧标题",
              "children": [{"label": "...", "desc": "...", "icon": "..."}]
            }
          ]
        }
        
        Args:
            extracted_data: 原始提取数据，包含扫平的 items 数组
        
        Returns:
            Dict: 转换为两层结构的数据
        """
        data = extracted_data.get('data', {})
        items = data.get('items', [])
        
        if not items or len(items) < 2:
            # 如果没有足够的数据，直接返回
            return extracted_data
        
        # 尝试智能分组：将items分为左右两组
        # 策略：前半部分为左侧，后半部分为右侧
        mid_index = len(items) // 2
        left_items = items[:mid_index]
        right_items = items[mid_index:]
        
        # 尝试从 items 中提取左右标题
        # 如果 label 包含“方案A”、“iPhone”等，可以作为标题
        left_label = "左侧"
        right_label = "右侧"
        
        # 尝试从第一个 item 的 label 中提取标题
        if left_items:
            first_label = left_items[0].get('label', '')
            # 尝试提取“方案A”、“iPhone”等实体名
            for keyword in ['方案A', 'iPhone', '优势', '左', 'A']:
                if keyword in first_label:
                    left_label = keyword
                    break
        
        if right_items:
            first_label = right_items[0].get('label', '')
            for keyword in ['方案B', 'Android', '劣势', '右', 'B']:
                if keyword in first_label:
                    right_label = keyword
                    break
        
        # 构建两层结构
        comparison_data = {
            "title": data.get('title', ''),
            "desc": data.get('desc', ''),
            "items": [
                {
                    "label": left_label,
                    "children": [
                        {
                            "label": item.get('label', ''),
                            "desc": item.get('desc', ''),
                            "icon": item.get('icon', '')
                        }
                        for item in left_items
                    ]
                },
                {
                    "label": right_label,
                    "children": [
                        {
                            "label": item.get('label', ''),
                            "desc": item.get('desc', ''),
                            "icon": item.get('icon', '')
                        }
                        for item in right_items
                    ]
                }
            ]
        }
        
        logger.info(f"[对比型转换] 将{len(items)}个项转换为左({len(left_items)})右({len(right_items)})两组")
        
        return {
            "data": comparison_data,
            "themeConfig": extracted_data.get('themeConfig', {})
        }


# 全局生成服务实例
_generate_service = None


def get_generate_service() -> GenerateService:
    """获取生成服务单例"""
    global _generate_service
    if _generate_service is None:
        _generate_service = GenerateService()
    return _generate_service
