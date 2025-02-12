const socket = new WebSocket("ws://localhost:8000/ws");
socket.onmessage = (event) => console.log("Translated:", event.data);
