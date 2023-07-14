


function toggleMenu() {
    var menu = document.getElementById("mobile-nav-panel-id")
    var mobileNav = document.getElementById("mobile-nav")
    if (menu.style.display === "none") {
        menu.style.display = 'flex'
        mobileNav.style.display = "none"
    } else {
        menu.style.display = 'none'
        mobileNav.style.display = "flex"
    }
}
  


