
// 提交问题并更新聊天记录
function submitQuestion(event) {
    event.preventDefault(); // 防止表单自动提交
    
    const userInput = document.getElementById('user-input').value;
    // 清空输入框
    document.getElementById('user-input').value = '';
    // 获取历史聊天记录区域
    const conversation = document.getElementById('conversation');
    
    // 用户的问题
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput;
    conversation.appendChild(userMessage);

    // 机器人的答案的占位符（转圈效果）
    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('message', 'bot-message');
    const loadingSpinner = document.createElement('div');
    loadingSpinner.classList.add('loading');
    loadingMessage.appendChild(loadingSpinner);
    conversation.appendChild(loadingMessage);
    
    // 滚动到最新的消息
    conversation.scrollTop = conversation.scrollHeight;

    // 提交问题到后端
    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // 找到最新的转圈占位符并替换为机器人的回答
        const lastBotMessage = conversation.querySelector('.bot-message:last-of-type');
        lastBotMessage.innerHTML = data.ans;  // 用机器人的回答替换占位符内容
        
        // 滚动到最新的消息
        conversation.scrollTop = conversation.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}