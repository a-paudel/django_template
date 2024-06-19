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

up.compiler("[up-replace-url]", function (element) {
    function formHandler() {
        let method = element.getAttribute("method") ?? "get"
        if (method.toLowerCase() !== "get") return

        let path = element.getAttribute("action") ?? location.pathname
        let params = new URLSearchParams(new FormData(element))
        let url = path + "?" + params.toString()

        history.replaceState(null, "", url)
    }

    function linkHandler() {
        let url = element.getAttribute("href")
        if (!url) return

        history.replaceState(null, "", url)
    }

    up.on(element, "up:form:submit", formHandler)
    up.on(element, "up:link:click", linkHandler)

    return function () {
        up.off(element, "up:form:submit", formHandler)
        up.off(element, "up:link:click", linkHandler)
    }
})