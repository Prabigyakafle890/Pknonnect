document.addEventListener('DOMContentLoaded', function(){
  const cards = document.querySelectorAll('.dept-card');
  const form = document.getElementById('deptForm');
  const submitBtn = document.getElementById('deptSubmit');
  const errorEl = document.getElementById('deptError');

  // when a card is clicked, check the corresponding radio input
  cards.forEach(card => {
    card.addEventListener('click', function(){
      // remove previous selection
      cards.forEach(c=>c.classList.remove('selected'));
      this.classList.add('selected');
      const val = this.dataset.value;
      // set the radio input with the matching value
      const radio = this.querySelector('input[type="radio"][name="department"]');
      if (radio) radio.checked = true;
      if (errorEl) errorEl.style.display = 'none';
    });
  });

  if (submitBtn && form) {
    submitBtn.addEventListener('click', function(e){
      const checked = form.querySelector('input[name="department"]:checked');
      if (!checked) {
        e.preventDefault();
        if (errorEl) {
          errorEl.style.display = 'block';
          errorEl.innerText = 'Please select a department to continue.';
        }
        // small visual shake to draw attention
        form.classList.add('needs-select');
        setTimeout(()=>form.classList.remove('needs-select'), 500);
        return;
      }
      // otherwise, allow normal submit
    });
  }
});
