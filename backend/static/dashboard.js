const checklist = document.querySelector("#checklist");
const pendingCount = document.querySelector("#pendingCount");
const dialog = document.querySelector("#expenseDialog");
const form = document.querySelector("#expenseForm");

function updatePendingCount() {
  const pending = [...checklist.querySelectorAll('.grocery input:not(:checked)')].length;
  pendingCount.textContent = `${pending} pendiente${pending === 1 ? "" : "s"}`;
}

checklist.addEventListener("change", updatePendingCount);

document.querySelector("#addItem").addEventListener("click", () => {
  const name = window.prompt("¿Qué necesitas comprar?");
  if (!name?.trim()) return;
  const item = document.createElement("label");
  item.className = "grocery";
  item.innerHTML = `<input type="checkbox"><span class="check"><span class="material-symbols-outlined">check</span></span><span class="grocery-copy"><strong></strong><small>Lista personal · Pendiente</small></span><em>Pendiente</em>`;
  item.querySelector("strong").textContent = name.trim();
  checklist.insertBefore(item, document.querySelector("#addItem"));
  updatePendingCount();
});

document.querySelector("#openExpense").addEventListener("click", () => dialog.showModal());

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const values = new FormData(form);
  const concept = values.get("concept").trim();
  const amount = Number(values.get("amount"));
  if (!concept || !Number.isFinite(amount) || amount <= 0) return;

  const expense = document.createElement("article");
  expense.className = "expense panel";
  expense.innerHTML = `<span class="expense-icon cyan"><span class="material-symbols-outlined">receipt_long</span></span><div><strong></strong><small>Ahora · Gasto añadido manualmente</small><em></em></div><aside><b></b><small></small></aside>`;
  expense.querySelector("strong").textContent = concept;
  expense.querySelector("em").textContent = "Pendiente de sincronizar";
  expense.querySelector("b").textContent = `-${amount.toLocaleString("es-ES", {minimumFractionDigits: 2, maximumFractionDigits: 2})} €`;
  expense.querySelector("aside small").textContent = values.get("category");
  document.querySelector("#expenses").prepend(expense);
  dialog.close();
  form.reset();
});
