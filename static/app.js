let chats = [];
let currentChat = [];

function render() {
    let box = document.getElementById("messages");
    box.innerHTML = "";

    currentChat.forEach(m => {
        let div = document.createElement("div");
        div.className = "msg " + m.role;
        div.innerHTML = `<b>${m.role}:</b> ${m.text}`;
        box.appendChild(div);
    });
}

function send() {
    let input = document.getElementById("input");
    let text = input.value.trim();

    if (!text) return;

    currentChat.push({ role: "user", text });
    render();

    fetch(`/rag-qa?query=${encodeURIComponent(text)}`)
        .then(res => res.json())
        .then(data => {
            currentChat.push({
                role: "ai",
                text: data.answer
            });
            render();
        });

    input.value = "";
}

function newChat() {
    if (currentChat.length > 0) {
        chats.push([...currentChat]);
    }
    currentChat = [];
    render();
}