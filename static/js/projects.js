async function loadProjectColumns() {
    try {
        const response = await fetch("/api/projects/columns");

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const columns = await response.json();

        const tabulatorColumns = columns.map(column => ({
            title: column,
            field: column
        }));

        console.log(tabulatorColumns);

        const table = new Tabulator("#projects-table", {
            layout: "fitData",
            ajaxURL: "/api/projects",
            columns: tabulatorColumns
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