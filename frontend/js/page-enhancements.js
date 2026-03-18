const pageMenuButton = document.querySelector(".menu-button");
const pageSiteNav = document.querySelector(".site-nav");
const pageNavLinks = document.querySelectorAll(".site-nav a");
const pageReveals = document.querySelectorAll(".reveal");
const pageScrollTopButton = document.querySelector(".scroll-top-button");

const pageObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        pageObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

pageReveals.forEach((node) => pageObserver.observe(node));

if (pageMenuButton && pageSiteNav) {
  pageMenuButton.addEventListener("click", () => {
    const isOpen = pageSiteNav.classList.toggle("is-open");
    pageMenuButton.setAttribute("aria-expanded", String(isOpen));
  });
}

pageNavLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (pageSiteNav?.classList.contains("is-open")) {
      pageSiteNav.classList.remove("is-open");
      pageMenuButton?.setAttribute("aria-expanded", "false");
    }
  });
});

function updatePageScrollTopButton() {
  if (!pageScrollTopButton) return;
  pageScrollTopButton.classList.toggle("is-visible", window.scrollY > 520);
}

pageScrollTopButton?.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

window.addEventListener("scroll", updatePageScrollTopButton, { passive: true });
updatePageScrollTopButton();
