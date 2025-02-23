// Handle Sign Up
function signUp(event) {
    event.preventDefault(); // Prevent form from submitting

    let username = document.getElementById("signup-username").value;
    let password = document.getElementById("signup-password").value;

    if (username && password) {
        localStorage.setItem("username", username);
        localStorage.setItem("password", password);
        alert("Sign Up Successful! Now Sign In.");
        window.location.href = "index.html"; // Reload page to switch to sign-in
    } else {
        alert("Please enter a username and password.");
    }
}

// Handle Sign In
function signIn(event) {
    event.preventDefault(); // Prevent form from submitting

    let loginUsername = document.getElementById("login-username").value;
    let loginPassword = document.getElementById("login-password").value;

    let storedUsername = localStorage.getItem("username");
    let storedPassword = localStorage.getItem("password");

    if (loginUsername === storedUsername && loginPassword === storedPassword) {
        alert("Login Successful!");
        window.location.href = "dashboard.html"; // Redirect to second page
    } else {
        alert("Invalid Username or Password!");
    }
}

// Toggle Between Sign Up & Sign In
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("container");
    document.getElementById("register").addEventListener("click", () => {
        container.classList.add("active");
    });
    document.getElementById("login").addEventListener("click", () => {
        container.classList.remove("active");
    });
});
