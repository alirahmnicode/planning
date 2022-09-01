$(".menu-toggle-btn").click(function () {
    $(this).toggleClass("fa-times");
    $(".navigation-menu").toggleClass("active");
});


var moreBtn = $('.more-habit')
var habitList = $('.habit-list')
var open = false
if (habitList.children().length > 5) {
    habitList.css('height', '130px')
}
moreBtn.click(function() {
    if(!open) {
        habitList.css('height', '100%')
        moreBtn.css('rotate', '180deg')
        open = true
    } else {
        habitList.css('height', '130px')
        moreBtn.css('rotate', '0deg')
        open = false
    }
})

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


// message
$(".close-message").click(function () {
    $(this)
        .parent(".alert")
        .fadeOut();
});