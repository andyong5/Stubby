console.log("This works")
google_btn = document.getElementById('google_btn')
logout = document.getElementById("logout")

if(google_btn != null)
    google_btn.addEventListener('click', () => {
        location.href = 'http://127.0.0.1:5000/login'
    })

if(logout != null){
    logout.addEventListener('click', () => {
    location.href = 'http://127.0.0.1:5000/logout'
    })
}
