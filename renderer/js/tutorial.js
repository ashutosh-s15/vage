const sections = document.querySelectorAll(".section");
const tocLinks = document.querySelectorAll("#toc a");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        const tocLink = document.querySelector(`#toc a[href="#${id}"]`);
        tocLinks.forEach((link) => link.classList.remove("active"));
        tocLink.classList.add("active");
      }
    });
  },
  { rootMargin: "-50% 0px -50% 0px" }
);

sections.forEach((section) => {
  observer.observe(section);
});

const btn = document.querySelector('#cta-start');
btn.addEventListener('click', function () {
  // Navigate to the index page
  window.location.href = 'index.html';
});