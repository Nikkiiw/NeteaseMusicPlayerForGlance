// content.js
// 运行在父页面 (10001端口)

console.log("🔌 智能避让中转脚本已加载");

// 监听来自后台 (background.js) 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // 检查消息类型
    if (message.type === 'SMART_CONTROL_COMMAND') {
        console.log("📩 收到后台广播:", message.action);
        
        // 找到所有的 iframe
        const iframes = document.querySelectorAll('iframe');
        
        for (let i = 0; i < iframes.length; i++) {
            const iframe = iframes[i];
            
            // 找到目标 iframe
            if (iframe.src && iframe.src.includes('192.168.50.5:55566')) {
                console.log("🎯 向播放器转发指令:", message.action);
                
                // 转发给 iframe
                iframe.contentWindow.postMessage({
                    type: 'NETEASE_PLAYER_CONTROL',
                    action: message.action
                }, '*');
                
                break; 
            }
        }
    }
});