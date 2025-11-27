"""
Dify工作流客户端
封装Dify API调用逻辑，支持阻塞和流式两种模式
"""
import logging
import time
import json
from typing import Dict, Any, Optional
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)


class DifyWorkflowClient:
    """Dify工作流API客户端"""
    
    def __init__(self):
        """初始化客户端"""
        settings = get_settings()
        self.base_url = settings.DIFY_API_BASE_URL
        self.api_key = settings.DIFY_API_KEY
        self.timeout = settings.DIFY_API_TIMEOUT
        self.response_mode = settings.DIFY_RESPONSE_MODE
        
        logger.info(f"[DifyWorkflowClient.__init__] 初始化 - base_url: {self.base_url}, api_key: {self.api_key[:20] if self.api_key else 'None'}...")
        
        if not self.api_key:
            logger.warning("[DifyWorkflowClient] DIFY_API_KEY未配置")
    
    async def call_workflow(
        self,
        user_text: str,
        template_id: Optional[str] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        调用Dify工作流生成数据
        
        Args:
            user_text: 用户输入的文本
            template_id: 模板ID（可选，帮助工作流理解目标结构）
            max_retries: 最大重试次数
        
        Returns:
            Dict: {
                "data": 符合模板schema的数据对象,
                "workflow_run_id": 工作流运行ID,
                "status": "success",
                "response_time": 响应耗时（秒）
            }
        
        Raises:
            Exception: 调用失败或超过重试次数时抛出异常
        """
        start_time = time.time()
        
        # 准备请求数据（根据Dify工作流的输入变量配置）
        inputs = {
            "content": user_text  # Dify工作流要求的content字段
        }
        if template_id:
            inputs["template"] = template_id  # Dify工作流要求的template字段
        
        # Dify工作流API参数格式
        payload = {
            "inputs": inputs,
            "response_mode": self.response_mode,
            "user": "system-user"
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/workflows/run"
        
        # 重试逻辑
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"[DifyWorkflowClient] 调用工作流 (尝试 {attempt}/{max_retries}) - "
                          f"模板: {template_id}, 文本长度: {len(user_text)}")
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    
                    logger.info(f"[DifyWorkflowClient] HTTP状态码: {response.status_code}")
                    logger.info(f"[DifyWorkflowClient] 响应内容: {response.text[:500]}")
                    
                    if response.status_code != 200:
                        error_msg = f"Dify API返回错误状态码: {response.status_code}"
                        logger.error(f"[DifyWorkflowClient] {error_msg}, 响应: {response.text[:200]}")
                        raise Exception(error_msg)
                    
                    result = response.json()
                    
                    # 解析响应
                    if self.response_mode == 'blocking':
                        parsed_result = self._parse_blocking_response(result)
                    else:
                        # 流式模式暂不实现，后续扩展
                        raise NotImplementedError("流式模式暂未实现")
                    
                    response_time = round(time.time() - start_time, 2)
                    parsed_result["response_time"] = response_time
                    
                    logger.info(f"[DifyWorkflowClient] 调用成功 - "
                              f"工作流ID: {parsed_result.get('workflow_run_id')}, "
                              f"耗时: {response_time}s")
                    
                    return parsed_result
                    
            except httpx.TimeoutException as e:
                last_error = f"请求超时: {str(e)}"
                logger.warning(f"[DifyWorkflowClient] {last_error} (尝试 {attempt}/{max_retries})")
            except httpx.RequestError as e:
                last_error = f"网络请求失败: {str(e)}"
                logger.warning(f"[DifyWorkflowClient] {last_error} (尝试 {attempt}/{max_retries})")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"[DifyWorkflowClient] 调用失败: {last_error} (尝试 {attempt}/{max_retries})")
            
            # 如果还有重试次数，等待后重试
            if attempt < max_retries:
                await self._async_sleep(1)
        
        # 所有重试都失败
        error_msg = f"Dify工作流调用失败（已重试{max_retries}次）: {last_error}"
        logger.error(f"[DifyWorkflowClient] {error_msg}")
        raise Exception(error_msg)
    
    def _parse_blocking_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析阻塞模式的响应
        
        Args:
            response: Dify API原始响应
        
        Returns:
            Dict: 解析后的结果
        """
        # 打印原始响应用于调试
        logger.info(f"[DifyWorkflowClient] 原始响应: {json.dumps(response, ensure_ascii=False, indent=2)[:1000]}")
        
        data = response.get("data", {})
        
        # 检查执行状态
        status = data.get("status", "unknown")
        if status == "failed":
            error = data.get("error", "未知错误")
            raise Exception(f"工作流执行失败: {error}")
        
        if status != "succeeded":
            raise Exception(f"工作流执行状态异常: {status}")
        
        # 提取输出数据（Dify工作流的输出变量名为"output"）
        outputs = data.get("outputs", {})
        
        # Dify工作流返回的output字段就是AntV Infographic的data部分
        workflow_data = outputs.get("output")
        
        # 如果返回的是JSON字符串，需要解析
        if isinstance(workflow_data, str):
            try:
                workflow_data = json.loads(workflow_data)
            except json.JSONDecodeError:
                logger.warning("[DifyWorkflowClient] 工作流返回的output不是有效JSON，尝试使用原始字符串")
        
        if not workflow_data:
            raise Exception("工作流未返回output字段")
        
        return {
            "data": workflow_data,
            "workflow_run_id": data.get("id"),
            "status": "success"
        }
    
    async def _async_sleep(self, seconds: float):
        """异步等待"""
        import asyncio
        await asyncio.sleep(seconds)


# 单例模式
_dify_workflow_client = None


def get_dify_workflow_client() -> DifyWorkflowClient:
    """获取Dify工作流客户端单例"""
    global _dify_workflow_client
    if _dify_workflow_client is None:
        _dify_workflow_client = DifyWorkflowClient()
    return _dify_workflow_client
