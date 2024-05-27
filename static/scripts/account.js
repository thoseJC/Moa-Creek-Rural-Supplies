class CreditPop extends HTMLElement {
  constructor() {
    super();
    this.bindClick();
    this.draggableLine();
    this.applyIncreasingCredit();
  }
  bindClick() {
    const creditPopCTA = document.querySelector('#cta-credit-pop');
    if (creditPopCTA) {
      creditPopCTA.addEventListener('click', () => {
        this.classList.add('active')
      })
    }

    const creditPopOverlay = this.querySelector('.credit--overlay');
    if (creditPopOverlay) {
      creditPopOverlay.addEventListener('click', () => {
        this.classList.remove('active')
      })
    }
  }
  draggableLine() {
    const compareCurrentNewValues = () => {
      const targetElement = document.querySelector('#rangeValue');
      const applyIncreasingCreditBtn = document.querySelector('#cta-apply-credit');
      if (targetElement) {
        const currentLimit = parseFloat(targetElement.dataset.currentLimit);
        const newLimit = parseFloat(targetElement.dataset.newLimit);
        if (currentLimit == newLimit) {
          applyIncreasingCreditBtn.classList.add('disabled');
        } else {
          applyIncreasingCreditBtn.classList.remove('disabled');
        }
      }
    }
    const rangeSlider = event => {
      compareCurrentNewValues();
      const newValue = event.target.value;
      const targetElement = document.querySelector('#rangeValue');
      if (targetElement) {
        targetElement.innerHTML = newValue;
        targetElement.setAttribute('data-new-limit', newValue);
      }
    }
    const line = document.querySelector('#credit-range');
    if (line) {
      line.addEventListener('change', event => {
        rangeSlider(event);
      })
      line.addEventListener('mousemove', event => {
        rangeSlider(event);
      })
    }
  }
  applyIncreasingCredit() {
    const applyIncreasingCreditBtn = document.querySelector('#cta-apply-credit');
    if (applyIncreasingCreditBtn) {
      applyIncreasingCreditBtn.addEventListener('click', event => {
        if (applyIncreasingCreditBtn.classList.contains('disabled')) return;
        event.preventDefault();
        const parentElement = document.querySelector('.credit--container');
        const loadingTarget = parentElement.querySelector('.loading-container');
        if (loadingTarget) {
          loadingTarget.classList.remove('displayNone');
        }

        const targetElement = document.querySelector('#rangeValue');
        if (targetElement) {
          const new_limit = parseFloat(targetElement.dataset.newLimit);
          const data = {
            new_limit
          }

          setTimeout(() => {
            fetch('/customer/credit_apply', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(data => {
              Swal.fire({
                icon: "success",
                title: "Credit Limit Increasement Application submitted successfully!",
                html: `The administrator will review your application ang get back to you soon!`,
                showConfirmButton: true
              }).then((result) => {
                if (result.isConfirmed) {
                  window.location.href = '/customer/credit';
                }
              });
            })
            .catch((error) => {
              console.error('Error:', error);
            })
            .finally(() => {
              if (parentElement) parentElement.classList.remove('active');
            })
          }, 2000);
        }

      })
    }
  }
}

customElements.define('credit-pop', CreditPop);