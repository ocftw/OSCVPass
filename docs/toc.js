// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded affix "><a href="index.html">OSCVPass 計畫簡介</a></li><li class="chapter-item expanded "><a href="apply-for.html"><strong aria-hidden="true">1.</strong> 申請</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="apply-for-oscvpass.html"><strong aria-hidden="true">1.1.</strong> 如何提出申請</a></li><li class="chapter-item expanded "><a href="apply-for-qa.html"><strong aria-hidden="true">1.2.</strong> 申請時常見問題</a></li><li class="chapter-item expanded "><div><strong aria-hidden="true">1.3.</strong> 教學</div></li><li><ol class="section"><li class="chapter-item expanded "><div><strong aria-hidden="true">1.3.1.</strong> 如何使用授權條款</div></li><li class="chapter-item expanded "><div><strong aria-hidden="true">1.3.2.</strong> 如何貢獻開源專案</div></li><li class="chapter-item expanded "><div><strong aria-hidden="true">1.3.3.</strong> 如何推廣開源</div></li></ol></li></ol></li><li class="chapter-item expanded "><a href="community.html"><strong aria-hidden="true">2.</strong> 社群</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="community-contribute.html"><strong aria-hidden="true">2.1.</strong> 如何參與</a></li><li class="chapter-item expanded "><a href="roadmap.html"><strong aria-hidden="true">2.2.</strong> 計畫藍圖</a></li><li class="chapter-item expanded "><a href="development.html"><strong aria-hidden="true">2.3.</strong> 參與開發</a></li><li class="chapter-item expanded "><a href="intern.html"><strong aria-hidden="true">2.4.</strong> 實習紀錄</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="intern_ChAoS-UnItY.html"><strong aria-hidden="true">2.4.1.</strong> 2023 intern</a></li><li class="chapter-item expanded "><a href="intern_Ayu_kevin.html"><strong aria-hidden="true">2.4.2.</strong> 2024 intern</a></li></ol></li></ol></li><li class="chapter-item expanded "><div><strong aria-hidden="true">3.</strong> 推薦專案</div></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
