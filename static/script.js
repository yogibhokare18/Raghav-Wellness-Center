document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }
  document.querySelectorAll(".flash-close").forEach((button) => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
  });
  const dob = document.querySelector("#dob");
  if (dob) dob.max = new Date().toISOString().split("T")[0];
  const appointmentDate = document.querySelector("#appointment_date");
  if (appointmentDate) {
    const localDate = new Date();
    const offset = localDate.getTimezoneOffset();
    appointmentDate.min = new Date(localDate.getTime() - offset * 60000).toISOString().split("T")[0];
  }
});
