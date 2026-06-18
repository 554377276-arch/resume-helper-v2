let chats = [];
let currentChat = [];
let currentChatId = null;

function render() {
    let box = document.getElementById("messages");
    box.innerHTML = "";

    currentChat.forEach(m => {
        let div = document.createElement("div");
        div.className = "msg " + m.role;
        div.innerHTML = `<b>${m.role === "user" ? "你" : "AI"}：</b>${m.text}`;
        box.appendChild(div);
    });

    box.scrollTop = box.scrollHeight;
}

function renderChatList() {
    let list = document.getElementById("chat-list");
    list.innerHTML = "";

    chats.forEach(chat => {
        let item = document.createElement("div");
        item.className = "chat-item";

        if (chat.id === currentChatId) {
            item.className += " active";
        }

        item.innerHTML = `
            <span onclick="loadChat(${chat.id})">${chat.title}</span>
            <button onclick="deleteChat(${chat.id})">删除</button>
        `;

        list.appendChild(item);
    });
}

function loadChatsFromDB() {
    fetch("/chats")
        .then(res => res.json())
        .then(data => {
            chats = data.chats;
            renderChatList();
        });
}

function createChatInDB(title, callback) {
    fetch(`/chats?title=${encodeURIComponent(title)}`, {
        method: "POST"
    })
        .then(res => res.json())
        .then(data => {
            currentChatId = data.id;
            loadChatsFromDB();

            if (callback) {
                callback();
            }
        });
}

function saveMessage(role, text) {
    if (currentChatId === null) return;

    fetch(`/chats/${currentChatId}/messages?role=${encodeURIComponent(role)}&text=${encodeURIComponent(text)}`, {
        method: "POST"
    });
}

function send() {
    let input = document.getElementById("input");
    let text = input.value.trim();

    if (!text) return;

    function realSend() {
        currentChat.push({ role: "user", text: text });
        saveMessage("user", text);
        render();

        let history = JSON.stringify(currentChat);

        fetch(`/rag-qa?query=${encodeURIComponent(text)}&history=${encodeURIComponent(history)}`)
            .then(res => res.json())
            .then(data => {
                currentChat.push({
                    role: "ai",
                    text: data.answer
                });

                saveMessage("ai", data.answer);
                render();
                loadChatsFromDB();
            });

        input.value = "";
        input.focus();
    }

    if (currentChatId === null) {
        createChatInDB(text.slice(0, 12), realSend);
    } else {
        realSend();
    }
}

function newChat() {
    currentChat = [];
    currentChatId = null;
    render();
    renderChatList();
}

function loadChat(chatId) {
    currentChatId = chatId;

    fetch(`/chats/${chatId}/messages`)
        .then(res => res.json())
        .then(data => {
            currentChat = data.messages;
            render();
            renderChatList();
        });
}

function deleteChat(chatId) {
    fetch(`/chats/${chatId}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(() => {
            if (currentChatId === chatId) {
                currentChat = [];
                currentChatId = null;
                render();
            }

            loadChatsFromDB();
        });
}

document.getElementById("input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        send();
    }
});

loadChatsFromDB();
document.getElementById("upload-form").addEventListener("submit", function(event) {
    event.preventDefault();
    

    let fileInput = document.getElementById("file-input");

    if (fileInput.files.length === 0) {
        alert("请先选择一个TXT文件");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
        });
});