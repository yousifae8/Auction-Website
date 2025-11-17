const login = document.getElementById("login");
const username = document.getElementById("username")
const password = document.getElementById("password")

username.value = localStorage.getItem("username")
password.value = localStorage.getItem("password")

const saveUserAndPass = () => {
    localStorage.setItem("username", username.value)
    localStorage.setItem("password", password.value)
}

login.addEventListener("click", saveUserAndPass)
