// 获取元素
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginFormContainer = document.getElementById('loginFormContainer');
const registerFormContainer = document.getElementById('registerFormContainer');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const registerUsernameInput = document.getElementById('registerUsername');
const registerPasswordInput = document.getElementById('registerPassword');
const confirmPasswordInput = document.getElementById('confirmPassword');
const errorMessage = document.getElementById('errorMessage');
const registerErrorMessage = document.getElementById('registerErrorMessage');
const showRegisterFormBtn = document.getElementById('showRegisterForm');
const showLoginFormBtn = document.getElementById('showLoginForm');

// 显示注册表单
showRegisterFormBtn.addEventListener('click', () => {
    loginFormContainer.style.display = 'none';
    registerFormContainer.style.display = 'block';
});

// 显示登录表单
showLoginFormBtn.addEventListener('click', () => {
    registerFormContainer.style.display = 'none';
    loginFormContainer.style.display = 'block';
});

// 登录表单提交事件
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = usernameInput.value;
    const password = passwordInput.value;
    errorMessage.textContent = '';

    const data = { username, password };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = 0;
            setTimeout(() => {
                window.location.href = '/chat';
            }, 500);
        } else {
            const errorData = await response.json();
            errorMessage.textContent = errorData.message || '登录失败，请检查用户名或密码。';
        }
    } catch (error) {
        errorMessage.textContent = '网络错误，请稍后再试。';
    }
});

// 注册表单提交事件
registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = registerUsernameInput.value;
    const password = registerPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    registerErrorMessage.textContent = '';

    // 检查密码是否匹配
    if (password !== confirmPassword) {
        registerErrorMessage.textContent = '密码和确认密码不一致';
        return;
    }

    const data = { username, password };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // 注册成功，自动跳转到登录界面
            registerErrorMessage.textContent = '注册成功，请登录';
            // 可以加一个定时器，在提示后自动跳转
            setTimeout(() => {
                loginFormContainer.style.display = 'block';
                registerFormContainer.style.display = 'none';
            }, 2000);
        } else {
            const errorData = await response.json();
            registerErrorMessage.textContent = errorData.message || '注册失败，请重试。';
        }
    } catch (error) {
        registerErrorMessage.textContent = '网络错误，请稍后再试。';
    }
});
