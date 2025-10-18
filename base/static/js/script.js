const loginBtn = document.getElementById("login-btn");
const loginMsg = document.getElementById("login-msg");
const inventorySection = document.getElementById("inventory-section");
const inventoryList = document.getElementById("inventory-list");

let token = "";

loginBtn.addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        loginMsg.textContent = "Username and password are required.";
        return;
    }

    try {
        // Login and get JWT token
        const response = await fetch("/api/auth/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            loginMsg.textContent = "Invalid credentials!";
            return;
        }

        const data = await response.json();
        token = data.access;

        loginMsg.textContent = "";
        document.getElementById("login-section").classList.add("hidden");
        inventorySection.classList.remove("hidden");

        // Fetch inventory
        fetchInventory();
    } catch (error) {
        loginMsg.textContent = "Login failed!";
        console.error(error);
    }
});

async function fetchInventory() {
    try {
        const response = await fetch("/api/inventory/", {
            headers: {
                "Authorization": "Bearer " + token,
            },
        });

        if (!response.ok) {
            inventoryList.innerHTML = "<li>Failed to fetch inventory.</li>";
            return;
        }

        const data = await response.json();
        inventoryList.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.name} - ${item.quantity} pcs - $${item.price}`;
            inventoryList.appendChild(li);
        });
    } catch (error) {
        console.error(error);
        inventoryList.innerHTML = "<li>Error fetching inventory.</li>";
    }
}
