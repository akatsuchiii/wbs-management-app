const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");

// トグルボタン押下処理(開閉機能)
menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});