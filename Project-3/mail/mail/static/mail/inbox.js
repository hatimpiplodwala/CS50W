document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inboxfdfdfdfdf');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => {
      clone = response.clone();
      if (response.status === 400 || response.status === 404){
        clone.json()
        .then(error => compose_error(error))
      }
      else{
        localStorage.clear();
        load_mailbox('inbox');
      }
    })

    return false;
  }
}

function compose_error(error){
  const errorblock = document.querySelector('#compose-error');
  errorblock.replaceChildren();
  const element = document.createElement('div');
  element.classList.add("alert", "alert-danger");
  element.innerHTML = `${error.error}`;
  errorblock.append(element);
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.body.scrollTop = document.documentElement.scrollTop = 0;
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => {
    clone = response.clone();
    if (response.status === 400 || response.status === 404){
      clone.json()
      .then(error => {
        const errorblock = document.querySelector('#emails-view');
        const element = document.createElement('div');
        element.classList.add("alert", "alert-danger");
        element.innerHTML = `${error.error}`;
        errorblock.append(element);
        document.body.scrollTop = document.documentElement.scrollTop = 0;
      })
    }
    else{
      clone.json()
      .then(emails => emails.forEach(email => {
        const element=document.createElement('div');
        if (email.read){
          element.className = "readbox";
        }
        else{
          element.className = "unreadbox";
        }
        element.innerHTML = `${email.subject} ${email.body} ${email.timestamp}`;
        document.querySelector("#emails-view").append(element);
      }))
  }})
}