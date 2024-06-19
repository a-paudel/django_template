import "unpoly/unpoly"
import "unpoly/unpoly.css"


up.compiler("[up-infinite]", function (element) {
    let loadMoreObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                up.follow(entry.target)
            }
        })
    }, {
        root: null,
        rootMargin: "50%",
        threshold: 0
    })

    loadMoreObserver.observe(element)

    return function () {
        loadMoreObserver.disconnect()
    }
})