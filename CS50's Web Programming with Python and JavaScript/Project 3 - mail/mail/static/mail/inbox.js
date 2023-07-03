document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function update_read_status(mail_element){
  if (!mail_element.read){
    fetch(`/emails/${mail_element.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }
}

function update_archive_status(mail_element){
  fetch(`/emails/${mail_element.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !mail_element.archived
    })
  }).then(() => {load_mailbox('archive')})
};

function reply_mail(mail_element){
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  let subject = mail_element.subject;
  if (!subject.startsWith("Re:")){
    subject = "Re: " + subject;
  }
  
  let body = `On ${mail_element.timestamp} ${mail_element.sender} wrote: ${mail_element.body}`;

  document.querySelector('#compose-recipients').value = mail_element.sender;
  document.querySelector('#compose-subject').value = subject
  document.querySelector('#compose-body').value = body;
}

function display_mail(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Show email details view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-detail-view').style.display = 'block';
      document.querySelector('#compose-view').style.display = 'none';
      
      // Fill the div with email data
      document.querySelector('#email-detail-view').innerHTML = `
        <h6><strong>From: </strong>${email.sender}</h6>
        <h6><strong>To: </strong>${email.recipients}</h6>
        <h6><strong>Subject: </strong>${email.subject}</h6>
        <h6><strong>Timestamp: </strong>${email.timestamp}</h6>
        <p>${email.body}</p>
      `;

      // Update read status
      update_read_status(email);

      // Archive button
      const btn_archived = document.createElement('button');
      btn_archived.innerHTML = email.archived ? "Unarchive" : "Archive";
      btn_archived.className = email.archived ? "btn btn-danger" : "btn btn-success";
      btn_archived.addEventListener('click',  () => update_archive_status(email));
      document.querySelector('#email-detail-view').append(btn_archived);

      // Reply button
      const btn_reply = document.createElement('button');
      btn_reply.innerHTML = "Reply";
      btn_reply.className = "btn btn-primary"
      btn_reply.style = "margin: 5px;"
      btn_reply.addEventListener('click',  () => reply_mail(email));
      document.querySelector('#email-detail-view').append(btn_reply);
      
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // API request to get mails for related inbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Loop thorugh emails and create a div for each email
      emails.forEach(email => {
        // Create div for each element
        const email_element = document.createElement('li');
        email_element.className = "list-group-item";
        
        // Create inner content
        email_element.innerHTML = `
          <h6><strong>From: </strong>${email.sender}</h6>
          <h6><strong>To: </strong>${email.recipients}</h6>
          <h6><strong>Subject: </strong>${email.subject}</h6>
          <h6><strong>Timestamp: </strong>${email.timestamp}</h6>
        `;
        
        // Change background color to be read or not
        email_element.style.backgroundColor = email.read ? '#ECECEC': 'white';
        email_element.addEventListener('click',  () => display_mail(email.id));
        document.querySelector('#emails-view').append(email_element);
      });
  });
}

function send_email() {
  event.preventDefault();
  // Get data from form
  const receipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // API request to send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: receipient,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  // Redirect Sent page
  load_mailbox('sent')
}
