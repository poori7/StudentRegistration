function editStudent(id, name, age, address, email) {
  document.getElementById("edit-id").value = id;
  document.getElementById("edit-name").value = name;
  document.getElementById("edit-age").value = age;
  document.getElementById("edit-address").value = address;
  document.getElementById("edit-email").value = email;
  document.getElementById("edit-form-container").style.display = "block";
}

function closeEditForm() {
  document.getElementById("edit-form-container").style.display = "none";
}
