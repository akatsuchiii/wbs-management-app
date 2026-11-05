const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");

// トグルボタン押下処理(開閉機能)
menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

// ログアウトボタンを取得
const logoutBtn = document.getElementById("logout");

// ログアウトボタン押下処理
logoutBtn.addEventListener("click", async () => {

    // FastAPIにログアウトを依頼
    const response = await fetch("/logout", {
        method: "POST"
    });

    // ログアウト成功時
    if (response.ok) {
        window.location.href = "/login";
    } else {
        console.error("ログアウトに失敗しました");
    }
});
