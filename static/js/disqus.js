var disqus_shortname = "{{ disqus_shortname }}";
var disqus_observer = new IntersectionObserver(function (entries) {
    // comments section reached
    // start loading Disqus now
    if (entries[0].isIntersecting) {
        var disqus_config = function () {
            this.page.url = window.location.origin + "{{object.get_absolute_url}}";
            this.page.identifier = window.location.origin + "_{{object.slug}}_{{object.id}}";
        };
        (function () {
            var d = document, s = d.createElement('script');
            s.src = `https://${disqus_shortname}.disqus.com/embed.js`;
            s.setAttribute('data-timestamp', +new Date());
            (d.head || d.body).appendChild(s);
        })();

        // once executed, stop observing
        disqus_observer.disconnect();
    }
}, { threshold: [0] });
disqus_observer.observe(document.querySelector("#disqus_thread"));