class CreditManagement extends HTMLElement {
  constructor() {
    super();
    this.bindClick();
    this.applyCreditApprove();
  }
  bindClick() {
    const targetElement = this.querySelector('.credit--container');
    const manageCustomerCreditBtns = document.querySelectorAll('.cta-manage-customer-credit');
    if (targetElement) {
      manageCustomerCreditBtns.forEach(btn => {
        btn.addEventListener('click', event => {
          event.preventDefault();
          targetElement.classList.add('active');
          const currentTarget = event.target;
          const {
            userId,
            userName,
            creditLimit,
            creditRemaining,
            creditApply
          } = currentTarget.dataset;

          this.userId = userId;
          this.creditApply = creditApply;
          this.creditLimit = creditLimit;
          this.creditRemaining = creditRemaining;

          const popupCustomerName = targetElement.querySelector('#customer-name');
          const popupCustomerCurrentLimit = targetElement.querySelector('#customer-current-credit-limit');
          const popupCustomerRemainingLimit = targetElement.querySelector('#customer-remaining-credit');
          const popupCustomerApplyCredit = targetElement.querySelector('#customer-apply-credit');
          const popupInputApplyCredit = targetElement.querySelector('#input-for-apply-credit');

          const formatCreditLimit = parseFloat(creditLimit) || 0;
          const formatCreditRemaining = parseFloat(creditRemaining) || 0;
          const formatCreditApply = parseFloat(creditApply) || 0;

          const applyCreditWrapper = this.querySelector('.credit-content--item-wrapper.apply-credit');
          
          if (formatCreditApply) {
            applyCreditWrapper.classList.remove('displayNone');
          } else {
            applyCreditWrapper.classList.add('displayNone');
          }
          if (formatCreditApply == -1) {
            applyCreditWrapper.classList.add('displayNone');
          }

          if (popupCustomerName) popupCustomerName.innerHTML = userName;
          if (popupCustomerCurrentLimit) {
            popupCustomerCurrentLimit.innerHTML = `$${formatCreditLimit.toFixed(2)}`;
            popupCustomerCurrentLimit.setAttribute('data-current-limit', formatCreditLimit);
          }
          if (popupCustomerRemainingLimit) popupCustomerRemainingLimit.innerHTML = `$${formatCreditRemaining.toFixed(2)}`;
          if (creditApply == 'None' || creditApply == 0) {
            if (popupInputApplyCredit) popupInputApplyCredit.value = formatCreditLimit;
          } else if (formatCreditApply == -1) {
            if (popupCustomerApplyCredit) popupCustomerApplyCredit.innerHTML = `$${formatCreditLimit.toFixed(2)}`;
            if (popupInputApplyCredit) popupInputApplyCredit.value = formatCreditLimit;
          } else {
            if (popupCustomerApplyCredit) popupCustomerApplyCredit.innerHTML = `$${formatCreditApply.toFixed(2)}`;
            if (popupInputApplyCredit) popupInputApplyCredit.value = parseFloat(formatCreditApply);
          }
        })
      })

      const creditPopOverlay = this.querySelector('.credit--overlay');
      if (creditPopOverlay) {
        creditPopOverlay.addEventListener('click', () => {
          targetElement.classList.remove('active');
        })
      }
    }
  }
  applyCreditApprove() {
    const ctaCreditApply = this.querySelector('#cta-credit-apply');
    if (ctaCreditApply) {
      ctaCreditApply.addEventListener('click', event => {
        event.preventDefault();
        const loadingTarget = this.querySelector('.loading-container');
        if (loadingTarget) loadingTarget.classList.remove('displayNone');

        const popupCustomerCurrentLimit = this.querySelector('#customer-current-credit-limit');
        const creditLimit = popupCustomerCurrentLimit.getAttribute('data-current-limit');
        const popupInputApplyCredit = this.querySelector('#input-for-apply-credit');
        const creditApply = popupInputApplyCredit.value;

        const data = {
          user_id: this.userId,
          credit_limit: creditLimit,
          credit_remaining: this.creditRemaining,
          credit_apply: creditApply
        }

        fetch('/manager/update_credit_apply', {
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
            title: "Credit Limit Increasement Application Approved!",
            html: `The customer will receive the noficiation on the dashboard now!`,
            showConfirmButton: true
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.href = '/manager/credit_management';
            }
          });
        })
        .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
        });
      })
    }
  }
}

customElements.define('credit-management', CreditManagement);