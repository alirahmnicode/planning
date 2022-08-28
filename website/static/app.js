$(".menu-toggle-btn").click(function () {
    $(this).toggleClass("fa-times");
    $(".navigation-menu").toggleClass("active");
});

function request(url, method) {
    url = url
    $.ajax({
        url: url,
        type: method,
        success: (res) => {
            console.log(res)
        }
    })
}


$('.done-plan').change(function () {
    var url = `http://${window.location.host}/plan/done/${this.value}/`
    request(url, 'post')
})

$('.active-habit').change(function () {
    var url = `http://${window.location.host}/habit/active/${this.value}/`
    request(url, 'post')
})
