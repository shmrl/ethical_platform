// ********** MANAGER LOGIN CREDENTIALS **********
const MANAGER_USERNAME = "manager1";
const MANAGER_PASSWORD = "company2025";
function managerLogin(event) {
    event.preventDefault();

    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (username === MANAGER_USERNAME && password === MANAGER_PASSWORD) {
        // Save login state
        localStorage.setItem("managerLoggedIn", "true");

        // Redirect to edit page
        window.location.href = "edit-standards.html";
    } else {
        alert("Incorrect username or password.");
    }
}
