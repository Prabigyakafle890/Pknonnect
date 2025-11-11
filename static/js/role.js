document.addEventListener('DOMContentLoaded', function(){
  const cards = document.querySelectorAll('.role-card');
  const form = document.getElementById('roleForm');
  const submitBtn = document.getElementById('roleSubmit');
  const errorEl = document.getElementById('roleError');

  cards.forEach(card => {
    card.addEventListener('click', function(){
      cards.forEach(c=>c.classList.remove('selected'));
      this.classList.add('selected');
      const radio = this.querySelector('input[type="radio"][name="role"]');
      if (radio) radio.checked = true;
      if (errorEl) errorEl.style.display = 'none';
    });
  });

  if (submitBtn && form) {
    submitBtn.addEventListener('click', function(e){
      const checked = form.querySelector('input[name="role"]:checked');
      if (!checked) {
        e.preventDefault();
        if (errorEl) {
          errorEl.style.display = 'block';
          errorEl.innerText = 'Please select a role to continue.';
        }
        form.classList.add('needs-select');
        setTimeout(()=>form.classList.remove('needs-select'), 500);
        return;
      }
    });
  }
});