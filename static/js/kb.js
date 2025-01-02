const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadBtn = document.getElementById('uploadBtn');
const fileListContainer = document.getElementById('uploadFolderFiles');

// 用来存储文件对象的数组
let selectedFiles = [];

// 获取上传文件夹中的文件
async function getUploadedFiles() {
    try {
        const response = await fetch('/getUploadedFiles'); // 假设你的后端有这个接口
        if (!response.ok) throw new Error('无法获取文件列表');

        const files = await response.json();

        // 清空文件列表
        fileListContainer.innerHTML = '';
        var file_list = files['names']
        // 渲染文件列表
        file_list.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');
            fileItem.innerHTML = `
                <span>${file}</span>
            `;
            fileListContainer.appendChild(fileItem);
        });
    } catch (error) {
        fileListContainer.innerHTML = '加载文件失败: ' + error.message;
    }
}

// 监听文件选择变化
fileInput.addEventListener('change', function(event) {
    const files = event.target.files;

    // 将新选择的文件添加到 selectedFiles 数组中
    selectedFiles = [...selectedFiles, ...Array.from(files)];

    // 更新显示的文件列表
    displayFiles();
});

// 显示文件名列表
function displayFiles() {
    fileList.innerHTML = '';

    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        const fileName = document.createElement('span');
        fileName.textContent = file.name;
        const removeBtn = document.createElement('span');
        removeBtn.textContent = '❌';
        removeBtn.classList.add('remove-btn');
        removeBtn.onclick = () => removeFile(index);

        fileItem.appendChild(fileName);
        fileItem.appendChild(removeBtn);

        fileList.appendChild(fileItem);
    });
}

// 删除文件的函数
function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFiles();
}

// 上传文件的函数
uploadBtn.addEventListener('click', async function() {
    if (selectedFiles.length === 0) {
        alert('请先选择文件!');
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files[]', file);
    });

    try {
        const response = await fetch('/LoadFile', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('文件上传失败!');
        }

        alert('文件上传成功！' + selectedFiles.map(file => file.name).join(', '));

        selectedFiles = [];
        displayFiles();
        getUploadedFiles(); // 上传成功后刷新文件列表
    } catch (error) {
        alert('上传失败: ' + error.message);
    }
});

// 初始化页面时加载文件夹内容
getUploadedFiles();