// background.js
// 运行在后台
// 逻辑：全局检测，只要有任何一个“其他”标签页有声音，就暂停网易云

console.log("🎧 后台服务已启动 (全局声音避让模式)");

let isOtherMediaPlaying = false;
let checkInterval = null;

function startMonitoring() {
    if (checkInterval) clearInterval(checkInterval);
    
    checkInterval = setInterval(() => {
        // 1. 获取当前窗口所有的标签页
        chrome.tabs.query({ currentWindow: true }, (tabs) => {
            if (!tabs || tabs.length === 0) return;

            let externalAudioFound = false;

            // 2. 遍历所有标签页，寻找“有声音”且“不是网易云”的页面
            tabs.forEach(tab => {
                // 只有 audible 为 true 的标签页才有声音
                if (tab.audible) {
                    // 判断是否是网易云页面 (根据你的实际地址调整)
                    const isNeteasePage = tab.url && tab.url.includes('192.168.50.5:10001');
                    
                    // 如果有声音 且 不是网易云 -> 标记为发现外部声音
                    if (!isNeteasePage) {
                        externalAudioFound = true;
                    }
                }
            });

            // --- 核心逻辑 ---

            // 情况A：发现了外部声音 -> 暂停网易云
            if (externalAudioFound) {
                if (!isOtherMediaPlaying) {
                    isOtherMediaPlaying = true;
                    console.log("⚠️ 发现外部声音，暂停网易云");
                    broadcastCommand('pause');
                }
            } 
            // 情况B：外部没声音了（不管是关了还是静音了）-> 恢复网易云
            else {
                if (isOtherMediaPlaying) {
                    isOtherMediaPlaying = false;
                    console.log("✅ 外部声音消失，恢复网易云");
                    broadcastCommand('play');
                }
            }
        });
    }, 1000); // 每秒检查一次
}

// 广播指令给所有页面
function broadcastCommand(action) {
    chrome.tabs.query({}, (tabs) => {
        if (!tabs) return;
        tabs.forEach((tab) => {
            if (!tab.url || (!tab.url.startsWith('http') && !tab.url.startsWith('file'))) return;
            
            chrome.tabs.sendMessage(tab.id, {
                type: 'SMART_CONTROL_COMMAND',
                action: action
            }).catch(() => {});
        });
    });
}

// 启动监控
startMonitoring();