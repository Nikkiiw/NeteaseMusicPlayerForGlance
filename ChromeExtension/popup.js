// 发送指令的函数
function sendCommand(actionName) {
    const statusDiv = document.getElementById('status');
    statusDiv.innerText = "正在发送...";
    statusDiv.style.color = "blue";

    // 获取当前激活的标签页
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        if (!tabs || tabs.length === 0) {
            statusDiv.innerText = "❌ 找不到页面";
            return;
        }

        const tabId = tabs[0].id;

        // 向页面注入脚本
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: function(action) {
                // --- 下面这段代码会在网页里运行 ---
                console.log("🚀 插件尝试发送指令:", action);
                
                window.postMessage({
                    type: 'NETEASE_PLAYER_CONTROL',
                    action: action
                }, '*');
                // --- 注入结束 ---
            },
            args: [actionName] // 把 actionName 传给上面的 function(action)
        }, function() {
            // 注入成功后的回调（不管网页里有没有报错，这里都会执行）
            statusDiv.innerText = "✅ 指令已发出 (请检查网页控制台)";
            statusDiv.style.color = "green";
        });
    });
}

// 绑定按钮事件
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('play').addEventListener('click', () => sendCommand('togglePlay'));
    document.getElementById('prev').addEventListener('click', () => sendCommand('previousSong'));
    document.getElementById('next').addEventListener('click', () => sendCommand('nextSong'));
    document.getElementById('lyrics').addEventListener('click', () => sendCommand('toggleLyrics'));
    document.getElementById('mini').addEventListener('click', () => sendCommand('toggleMinimize'));
});