const elementCancel = document.getElementById("cancel");
elementCancel.addEventListener("click", closeModal);
const elementRegist = document.getElementById("project-create-form");
elementRegist.addEventListener("submit", registProject);


// キャンセルボタン押下処理
function closeModal() {
    const dialog = document.getElementById("create-dialog");
    dialog.close();
}

// 登録ボタン押下処理
function registProject(event) {
    // 各要素の取得 + 入力値の格納
    const projectNm = document.getElementById("project-name").value;
    const summary = document.getElementById("summary").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const status = document.getElementById("status").value;

    const project = {
        name: projectNm,
        summary: summary,
        str_date: startDate || null,
        end_date: endDate || null,
        status: status,
    }

    const json = JSON.stringify(project)

    event.preventDefault();

    // 非同期

    fetch("/api/projects", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: json
    })
        .then(async (response) => {
            console.log("HTTPステータス:", response.status);

            const json = await response.json();

            if (response.status == 400) {
                alert(json.detail);
                return;
            }

            if (!response.ok) {
                // 登録失敗
                alert("プロジェクト登録に失敗しました。");
                return;
            }

            window.location.reload();
        })
        .catch((error) => {
            // 例外発生
        });
}