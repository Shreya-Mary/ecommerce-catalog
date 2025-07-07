const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/";
}

let currentPage = 1;
const itemsPerPage = 5;
let currentSearch = "";
let currentStatus = "";

window.onload = () => {
  loadCatalogs();
};

function showForm(formId) {
  document.querySelectorAll('.form-section').forEach(sec => sec.style.display = 'none');
  document.getElementById(`${formId}Form`).style.display = 'block';
}


function hideSections() {
  document.querySelectorAll('.form-section').forEach(sec => sec.style.display = 'none');
}

async function handleCreate(event) {
  event.preventDefault();
  const data = {
    name: document.getElementById("createName").value,
    description: document.getElementById("createDesc").value,
    start_date: document.getElementById("createStart").value,
    end_date: document.getElementById("createEnd").value,
    status: document.getElementById("createStatus").value
  };

  try {
    const response = await fetch("/catalogs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(result.message || "Catalog created");

    if (response.ok) {
      hideSections();
      loadCatalogs();
    }
  } catch (error) {
    alert("Error creating catalog");
    console.error(error);
  }
}

async function handleUpdate(event) {
  event.preventDefault();
  const catalogId = document.getElementById("updateId").value;
  const data = {
    name: document.getElementById("updateName").value,
    description: document.getElementById("updateDesc").value,
    start_date: document.getElementById("updateStart").value,
    end_date: document.getElementById("updateEnd").value,
    status: document.getElementById("updateStatus").value
  };

  try {
    const response = await fetch(`/catalogs/${catalogId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(result.message || "Catalog updated");

    if (response.ok) {
      hideSections();
      loadCatalogs();
    }
  } catch (error) {
    alert("Error updating catalog");
    console.error(error);
  }
}

async function handleDelete(catalogId) {
  if (!confirm("Are you sure you want to delete this catalog?")) return;

  try {
    const response = await fetch(`/catalogs/${catalogId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const result = await response.json();
    alert(result.message || "Catalog deleted");

    if (response.ok) {
      loadCatalogs();
    }
  } catch (error) {
    alert("Error deleting catalog");
    console.error(error);
  }
}

async function loadCatalogs(page = 1) {
  currentPage = page;
  const params = new URLSearchParams({
    page,
    size: itemsPerPage,
    status: currentStatus,
    sort_by: "start_date",
    search: currentSearch
  });

  try {
    const response = await fetch(`/catalogs?${params.toString()}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const result = await response.json();

    if (response.ok && result.data?.length > 0) {
      renderTable(result.data);
      renderPagination(result.total_count || result.data.length);
    } else {
      document.getElementById("catalogTableBody").innerHTML = `<tr><td colspan="7">No catalogs found</td></tr>`;
      document.getElementById("paginationControls").innerHTML = "";
    }

  } catch (error) {
    alert("Error loading catalogs");
    console.error(error);
  }
}

function renderTable(catalogs) {
  const tbody = document.getElementById("catalogTableBody");
  tbody.innerHTML = "";

  catalogs.forEach(c => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${c.catalog_id}</td>
      <td>${c.catalog_name}</td>
      <td>${c.catalog_description}</td>
      <td>${c.start_date}</td>
      <td>${c.end_date}</td>
      <td>${c.status}</td>
      <td>
        <button class="update-button" onclick="fillUpdateForm(${c.catalog_id}, '${c.catalog_name}', '${c.catalog_description}', '${c.start_date}', '${c.end_date}', '${c.status}')">Update</button>
        <button class="delete-button" onclick="handleDelete(${c.catalog_id})">Delete</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}


function renderPagination(totalItems) {
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const container = document.getElementById("paginationControls");
  container.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.classList.toggle("active", i === currentPage);
    btn.onclick = () => loadCatalogs(i);
    container.appendChild(btn);
  }
}

function applyFilter() {
  currentSearch = document.getElementById("searchInput").value.trim();
  currentStatus = document.getElementById("statusFilter").value.trim();
  loadCatalogs(1);
}

function fillUpdateForm(id, name, desc, start, end, status) {
  showForm("update");
  document.getElementById("updateId").value = id;
  document.getElementById("updateName").value = name;
  document.getElementById("updateDesc").value = desc;
  document.getElementById("updateStart").value = start.replace(" ", "T");
  document.getElementById("updateEnd").value = end.replace(" ", "T");
  document.getElementById("updateStatus").value = status;
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}
