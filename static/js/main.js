// 全域通用 JS

// 刪除 Task
async function deleteTask(id) {
  if (!confirm("確定刪除？")) return;
  const res = await fetch(`/tasks/${id}`, { method: "DELETE" });
  if (res.ok) location.reload();
}

// 新增 Task (for both page form and FAB modal)
async function createTask(e, isFabModal) {
  e.preventDefault();
  const form = e.target;
  const title = form.title.value.trim();
  const est_hours = form.est_hours.value;
  const due_date = form.due_date ? form.due_date.value : "";
  const color = form.color ? form.color.value : "#2196f3";
  const res = await fetch("/tasks/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, est_hours, due_date, color }),
  });
  if (res.ok) {
    if (isFabModal) {
      // 關閉 modal
      const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('addTaskModal'));
      modal.hide();
    }
    // schedule頁面用ajax刷新，其他頁直接reload
    if (window.location.pathname.startsWith('/schedule')) {
      // 若有/refresh API則用ajax刷新
      fetch('/schedule/refresh').then(r=>r.json()).then(()=>location.reload());
    } else {
      location.reload();
    }
  }
  return false;
}
