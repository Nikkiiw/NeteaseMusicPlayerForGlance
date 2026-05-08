// background.js
// Service Worker — Manifest V3 生命周期下通过 chrome.alarms 保持存活
// 逻辑：全局检测，只要有任何一个"其他"标签页有声音，就暂停网易云

console.log("🎧 后台服务已启动 (全局声音避让模式)");

let isOtherMediaPlaying = false;
let checkInterval = null;

function checkTabs() {
    chrome.tabs.query({ currentWindow: true }, (tabs) => {
        if (chrome.runtime.lastError || !tabs || tabs.length === 0) return;

        let externalAudioFound = false;

        tabs.forEach(tab => {
            if (tab.audible) {
                const isNeteasePage = tab.url && tab.url.includes('192.168.50.5:10001');
                if (!isNeteasePage) {
                    externalAudioFound = true;
                }
            }
        });

        if (externalAudioFound) {
            if (!isOtherMediaPlaying) {
                isOtherMediaPlaying = true;
                console.log("⚠️ 发现外部声音，暂停网易云");
                broadcastCommand('pause');
            }
        } else {
            if (isOtherMediaPlaying) {
                isOtherMediaPlaying = false;
                console.log("✅ 外部声音消失，恢复网易云");
                broadcastCommand('play');
            }
        }
    });
}

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

function startPolling() {
    if (checkInterval) clearInterval(checkInterval);
    checkInterval = setInterval(checkTabs, 1000);
    checkTabs(); // 立即执行一次
}

// chrome.alarms 心跳 — 即便 Worker 被 Chrome 终止，每分钟会唤醒一次重建轮询
chrome.alarms.create('keepalive', { periodInMinutes: 1 });

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'keepalive') {
        startPolling();
    }
});

// 浏览器启动 / 扩展安装时初始化
chrome.runtime.onStartup.addListener(startPolling);
chrome.runtime.onInstalled.addListener(startPolling);

// 首次加载时立即启动
startPolling();
