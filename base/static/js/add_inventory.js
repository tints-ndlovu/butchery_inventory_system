document.getElementById("inventoryForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const quantity = document.getElementById("quantity").value;
  const price = document.getElementById("price").value;
  const message = document.getElementById("message");

  // Replace this with your real token from login
  const token = localStorage.getItem("access_token");

  if (!token) {
    message.textContent = "No token found. Please log in first.";
    return;
  }

  const response = await fetch("http://127.0.0.1:8000/api/inventory/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ name, quantity, price })
  });

  if (response.status === 201) {
    message.textContent = "Item added successfully!";
    message.style.color = "lightgreen";
    document.getElementById("inventoryForm").reset();
  } else {
    const error = await response.json();
    message.textContent = "Error: " + JSON.stringify(error);
    message.style.color = "red";
  }
});
