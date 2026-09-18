const STORAGE_KEY = "hogar.expenses.v1";
const today = new Date().toISOString().slice(0, 10);
let activeFilter = "all";

const seed = [
  { id: "seed-1", concept: "Carrefour Market", amount: 142.30, category: "Alimentación", date: today },
  { id: "seed-2", concept: "Hnos. Gómez Carnicería", amount: 38.40, category: "Alimentación", date: today },
  { id: "seed-3", concept: "Glovo / Tokyo Sushi House", amount: 34.50, category: "Ocio", date: today },
];

function readExpenses() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved ? JSON.parse(saved) : seed;
}
function saveExpenses(expenses) { localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses)); }
function money(value) { return `${value.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €`; }
function dateParts(date) {
  const local = new Date(`${date}T12:00:00`);
  return { day: local.getDate(), month: local.toLocaleDateString("es-ES", { month: "short" }).replace(".", "") };
}
function iconFor(category) {
  return ({ "Alimentación": "shopping_cart", "Transporte": "directions_car", "Vivienda": "home", "Salud": "medical_services", "Ocio": "local_activity" })[category] || "payments";
}
function getExpenses() { return readExpenses().sort((a, b) => b.date.localeCompare(a.date)); }

function render() {
  const all = getExpenses();
  const visible = activeFilter === "all" ? all : all.filter((item) => item.category === activeFilter);
  const total = all.reduce((sum, item) => sum + Number(item.amount), 0);
  document.querySelector("#monthTotal").textContent = money(total);
  document.querySelector("#transactionCount").textContent = `${all.length} movimiento${all.length === 1 ? "" : "s"}`;
  const list = document.querySelector("#expenseList");
  const empty = document.querySelector("#emptyState");
  list.innerHTML = "";
  empty.hidden = visible.length > 0;
  visible.forEach((item) => {
    const parts = dateParts(item.date);
    const entry = document.createElement("article");
    entry.className = "expense-entry panel";
    entry.innerHTML = `<span class="date-box"><b>${parts.day}</b><small>${parts.month}</small></span><span class="expense-icon cyan"><span class="material-symbols-outlined"></span></span><div class="entry-copy"><strong></strong><span></span><em>Salida registrada</em></div><div class="entry-side"><b></b><button class="delete-expense" aria-label="Borrar salida"><span class="material-symbols-outlined">delete</span></button></div>`;
    entry.querySelector(".expense-icon span").textContent = iconFor(item.category);
    entry.querySelector(".entry-copy strong").textContent = item.concept;
    entry.querySelector(".entry-copy > span").textContent = item.category;
    entry.querySelector(".entry-side b").textContent = `-${money(Number(item.amount))}`;
    entry.querySelector(".delete-expense").addEventListener("click", () => {
      const remaining = getExpenses().filter((expense) => expense.id !== item.id);
      saveExpenses(remaining);
      render();
    });
    list.append(entry);
  });
}

const dialog = document.querySelector("#expenseDialog");
document.querySelector("#openExpense").addEventListener("click", () => { document.querySelector('[name="date"]').value = today; dialog.showModal(); });
document.querySelector("#closeDialog").addEventListener("click", () => dialog.close());
document.querySelector("#expenseForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const amount = Number(data.get("amount"));
  if (!Number.isFinite(amount) || amount <= 0) return;
  const expenses = getExpenses();
  expenses.push({ id: crypto.randomUUID(), concept: data.get("concept").trim(), amount, category: data.get("category"), date: data.get("date") });
  saveExpenses(expenses);
  dialog.close();
  event.currentTarget.reset();
  render();
});
document.querySelector("#filterButton").addEventListener("click", () => {
  const filters = document.querySelector("#filters");
  filters.hidden = !filters.hidden;
});
document.querySelector("#filters").addEventListener("click", (event) => {
  if (event.target.tagName !== "BUTTON") return;
  activeFilter = event.target.dataset.filter;
  document.querySelectorAll("#filters button").forEach((button) => button.classList.toggle("active", button === event.target));
  render();
});
document.querySelector("#clearAll").addEventListener("click", () => {
  if (window.confirm("¿Quieres borrar todos los gastos guardados en este navegador?")) { saveExpenses([]); render(); }
});
render();
