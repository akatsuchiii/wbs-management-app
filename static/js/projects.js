async function loadProjectColumns() {
    try {
        const response = await fetch("/api/projects/columns");

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const columns = await response.json();
        let editingProjectId = null;
        const tabulatorColumns = columns.map(column => ({
            title: column,
            field: column,
            editor: column == "name" ? "input" : false
        }));

        console.log(tabulatorColumns);

        const table = new Tabulator("#projects-table", {
            layout: "fitData",
            ajaxURL: "/api/projects",
            columns: tabulatorColumns,
            // 複数行選択を有効化
            selectableRows: true,
            selectableRowsRangeMode: "click"
        });
        // 行選択が変更された際の処理
        table.on("rowSelectionChanged", function (data, rows) {

            // 選択したプロジェクトのIDを取得
            const projectIds = data.map(project => project.id);

            console.log("選択中のプロジェクトID:", projectIds);
        });

        // 削除ボタン押下処理
        // 削除ボタンの要素取得
        const deleteBrnElement = document.getElementById("delete-btn");

        deleteBrnElement.addEventListener("click", async () => {
            const selectedTable = table.getSelectedData();

            // 0件の場合
            if (selectedTable.length === 0) {
                alert("データが選択されていません。");
                return;
            }

            const result = confirm(`${selectedTable.length}行選択されています。削除しますか？`);
            if (!result) {
                return;
            }


            // 選択したプロジェクトのIDを取得
            const projectIds = selectedTable.map(project => project.id);

            try{
                // python側へ
                const response = await fetch("/api/projects/bulk", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "projectId": projectIds
                    })
                });

                if (response.ok) {
                    const json = await response.json();
                    console.log(json.deleted_ids);
                    await table.replaceData();
                }
                else{
                    throw new Error(`HTTP Error: ${response.status}`);
                }
            } catch(error) {
                console.error(error);
            }
        });

    } catch (error) {
        // memo: 後ほどエラー表示処理を追加予定
        console.error(error);
    }
}

loadProjectColumns();


// 新規登録ボタンの要素を取得
const createBtnElement = document.getElementById("create-Btn");
createBtnElement.addEventListener("click", clickCreateBtn);
// 新規登録ボタン押下処理
function clickCreateBtn() {
    // ダイアログのHTML要素取得
    const element = document.getElementById("create-dialog");
    showCreateDialog(element);
}
// ダイアログ表示_本処理
function showCreateDialog(element) {
    element.showModal();
}
