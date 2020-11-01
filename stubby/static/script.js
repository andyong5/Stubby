console.log("This works")
google_btn = document.getElementById('google_btn')
logout = document.getElementById("logout")

if(google_btn != null)
    google_btn.addEventListener('click', () => {
        location.href = 'http://findmystubby.com/login'
    })

if(logout != null){
    logout.addEventListener('click', () => {
    location.href = 'http://findmystubby.com/logout'
    })
}
