from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import socket
def get_global_ipv6_address():
    """获取本机有效的全局IPv6地址"""
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET6):
            addr = info[4][0]
            # 过滤本地链路地址和回环地址
            if not addr.startswith('fe80') and addr != '::1':
                # 移除可能的接口后缀（如%eth0）
                return addr.split('%')[0]
        return None
    except Exception as e:
        print(f"Error fetching IPv6: {e}")
        return None

def build_http_url():
    """构建包含IPv6地址的HTTP URL字符串"""
    ipv6 = get_global_ipv6_address()
    return f"http://[{ipv6}]:8000" if ipv6 else "No valid IPv6 address found"


@register("SillyTavernAddress(IPV6)", "Lynn", "返回本机的IPV6地址并加上酒馆的端口号", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("酒馆地址")
    async def helloworld(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(build_http_url()) # 发送一条纯文本消息

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
